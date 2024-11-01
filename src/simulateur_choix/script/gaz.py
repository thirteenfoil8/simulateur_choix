import pandas as pd
from importlib.resources import path
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import pickle
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

import os
os.environ['CMDSTAN'] = "C:/Users/flori/anaconda3/envs/simulateur_choix/Lib/site-packages/cmdstanpy"




class Gaz():
    def __init__(self, verbose=False) -> None:
        with path('simulateur_choix.data', 'gaz.xlsx') as p:
            self.file_path = str(p)
        self.df = pd.DataFrame()
        self.linear_model = LinearRegression()
        self.medium_models = []
        self.verbose= verbose

    def extract(self):
        self.df = pd.read_excel(self.file_path, usecols=["Monat / Mois", "Bleifrei 95 / sans plomb 95"], skiprows=4, engine='openpyxl')
        return self

    def transform(self):
        self.df.columns = ["month", "price"]
        self.df.dropna(inplace=True)
        self.df['month_int'] = self.df['month'].apply(self.timestamp_to_int)
        self.df["price"] = self.df["price"].astype('float64')
        self.X_train, self.X_test, self.y_train, self.y_test = self.get_train_test_set()
        return self

    def load(self):
        return self
    
    def get_model(self):
        with path('simulateur_choix.data', 'linear_model.pkl') as p:
            self.store_path = str(p)
        with open(self.store_path, 'rb') as file:
            self.linear_model = pickle.load(file)
        return self.linear_model

    def get_train_test_set(self):
        X_train, X_test, y_train, y_test = train_test_split(self.df.month_int, self.df.price, test_size=0.2, random_state=42)
        return X_train.values.reshape(-1, 1), X_test.values.reshape(-1, 1), y_train.values.reshape(-1, 1), y_test.values.reshape(-1, 1)

    def timestamp_to_int(self, ts):
        return (ts.year - 1993) * 12 + ts.month - 1

    def train_linear_model(self):

        self.linear_model.fit(self.X_train, self.y_train)
        y_pred = self.linear_model.predict(self.X_test)
        mse = mean_squared_error(self.y_test, y_pred)
        if self.verbose:
            print(f'Mean Squared Error: {mse}')

        with path('simulateur_choix.data', 'linear_model.pkl') as p:
            self.store_path = str(p)
        with open(self.store_path, 'wb') as file:
            pickle.dump(self.linear_model, file)

    def train_medium_model(self, alpha=0.01):
        # Définir les paramètres pour la recherche de grille
        parameters = {'degree': [2, 3, 4, 5, 6, 7, 8, 9, 10],
                    'normalize': [True, False]
                    }

        # Transformer les données d'entraînement
        best_score = float('inf')
        best_degree = None
        best_model = None

        # Standardize the data (important for Ridge regression)
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(self.X_train)
        X_test_scaled = scaler.transform(self.X_test)

        for degree in parameters['degree']:
            poly = PolynomialFeatures(degree=degree)
            X_poly_train = poly.fit_transform(X_train_scaled)
            model = Ridge(alpha=alpha)

            # Former le modèle avec les données transformées
            model.fit(X_poly_train, self.y_train)

            # Prédire les valeurs pour l'ensemble de test
            X_poly_test = poly.transform(X_test_scaled)
            y_pred = model.predict(X_poly_test)
            mse = mean_squared_error(self.y_test, y_pred)
            self.medium_models.append(model)

            # Vérifier si c'est le meilleur modèle
            if mse < best_score:
                best_score = mse
                best_degree = degree
                best_model = model

        self.medium_model = best_model
        self.best_degree = best_degree
        self.scaler = scaler  # Store the scaler for later use in prediction
        if self.verbose:
            print(f'Mean Squared Error: {best_score}')
            print(f'Best Polynomial Degree: {best_degree}')

    def grid_search_random_forest(self):
        # Définir les hyperparamètres à tester
        param_grid = {
            'n_estimators': [200, 500, 1000],
            'max_depth': [None, 10, 20, 30, 40],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }

        rf = RandomForestRegressor(random_state=42)
        grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, 
                                cv=3, n_jobs=-1, verbose=2, scoring='neg_mean_squared_error')

        grid_search.fit(self.X_train, self.y_train.ravel())
        self.rf_model = grid_search.best_estimator_
        if self.verbose:
            print(f"Best parameters found: {grid_search.best_params_}")
        y_pred = self.rf_model.predict(self.X_test)
        mse = mean_squared_error(self.y_test, y_pred)
        if self.verbose:
            print(f'Random Forest MSE with Best Parameters: {mse}')

    def train_random_forest(self, n_estimators=100, max_depth=None):
        self.rf_model = RandomForestRegressor(
            n_estimators=500,
            max_depth=None,
            min_samples_split=2,
            min_samples_leaf=1,
            random_state=42
        )
        self.rf_model.fit(self.X_train, self.y_train.ravel())  # ravel() is used to convert y_train to 1D array
        y_pred = self.rf_model.predict(self.X_test)
        mse = mean_squared_error(self.y_test, y_pred)
        if self.verbose:
            print(f'Random Forest MSE: {mse}')

    def predict(self, dates, model_type="linear"):
        # Convert single date to a list for consistency
        if not isinstance(dates, list):
            dates = [dates]

        # Convert dates to integer format
        dates_int = [self.timestamp_to_int(date) for date in dates]
        dates_int = np.array(dates_int).reshape(-1, 1)

        # Predict using the chosen model
        if model_type == "linear":
            return self.linear_model.predict(dates_int)
        elif model_type == "medium":
            poly = PolynomialFeatures(degree=self.best_degree)
            dates_int_scaled = self.scaler.transform(dates_int)
            dates_int_poly = poly.fit_transform(dates_int_scaled)
            return self.medium_model.predict(dates_int_poly)

        elif model_type == "random_forest":
            return self.rf_model.predict(dates_int)

if __name__ == "__main__":
    gaz = Gaz(verbose=True)
    gaz.extract().transform()
    gaz.get_model()

    predicted_prices_linear = [gaz.predict(date, model_type="linear")[0][0] for date in gaz.df.month]

    # Predicting using the linear model
    date_to_predict = datetime(2025, 1, 1)
    predicted_price_linear = gaz.predict(date_to_predict, model_type="linear")
    print(f"Predicted price (linear model) for {date_to_predict}: {predicted_price_linear[0][0]}")


    # Generate a list of dates from 1990 to 2060
    dates_1990_2060 = pd.date_range(start="1990-01-01", end="2060-01-01", freq='M')

    # Predict prices for these dates using both models
    predicted_prices_linear_2023_2060 = [gaz.predict(date, model_type="linear")[0][0] for date in dates_1990_2060]

    # Plotting
    plt.figure(figsize=(14, 7))
    plt.plot(dates_1990_2060, predicted_prices_linear_2023_2060, label="Linear Model", color="blue")
    plt.scatter(gaz.df.month, gaz.df.price, color="red", s=10, label="Actual Prices")
    plt.title("Gas Price Predictions from 2023 to 2060")
    plt.xlabel("Year")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    print("end")
