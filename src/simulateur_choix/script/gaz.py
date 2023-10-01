import pandas as pd
from importlib.resources import path
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from statsmodels.tsa.arima.model import ARIMA
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
import pmdarima as pm
import matplotlib.pyplot as plt
import numpy as np

class Gaz():
    def __init__(self) -> None:
        with path('simulateur_choix.data', 'gaz.xlsx') as p:
            self.file_path = str(p)
        self.df = pd.DataFrame()
        self.stable_model = LinearRegression()
        self.medium_model = None
        self.advanced_model = None

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

    def get_train_test_set(self):
        X_train, X_test, y_train, y_test = train_test_split(self.df.month_int, self.df.price, test_size=0.2, random_state=42)
        return X_train.values.reshape(-1, 1), X_test.values.reshape(-1, 1), y_train.values.reshape(-1, 1), y_test.values.reshape(-1, 1)

    def timestamp_to_int(self, ts):
        return (ts.year - 1993) * 12 + ts.month - 1

    def train_stable_model(self):

        self.stable_model.fit(self.X_train, self.y_train)
        y_pred = self.stable_model.predict(self.X_test)
        mse = mean_squared_error(self.y_test, y_pred)
        print(f'Mean Squared Error: {mse}')

    def train_medium_model(self):

        # Définir les paramètres pour la recherche de grille
        parameters = {'degree': [2, 3, 4, 5, 6, 7, 8, 9, 10],
                      'normalize': [True, False]
                      }

        # Transformer les données d'entraînement
        best_score = float('inf')
        best_degree = None
        best_model = None

        for degree in parameters['degree']:
            poly = PolynomialFeatures(degree=degree)
            X_poly_train = poly.fit_transform(self.X_train)
            model = LinearRegression()

            # Former le modèle avec les données transformées
            model.fit(X_poly_train, self.y_train)

            # Prédire les valeurs pour l'ensemble de test
            X_poly_test = poly.transform(self.X_test)
            y_pred = model.predict(X_poly_test)
            mse = mean_squared_error(self.y_test, y_pred)

            # Vérifier si c'est le meilleur modèle
            if mse < best_score:
                best_score = mse
                best_degree = degree
                best_model = model

        self.medium_model = best_model

        print(f'Mean Squared Error: {best_score}')
        print(f'Best Polynomial Degree: {best_degree}')


    def train_advanced_model(self):

        # Train ARIMA
        arima_model = ARIMA(self.y_train.ravel(), order=(0, 0, 0)).fit()
        y_pred = arima_model.forecast(steps=len(self.y_test))
        mse_arima = mean_squared_error(self.y_test.ravel(), y_pred)
        print(f'Mean Squared Error: {mse_arima}')

        #LSTM
        scaler = MinMaxScaler()
        y_train_scaled = scaler.fit_transform(self.y_train)
        y_test_scaled = scaler.transform(self.y_test)

        # Remodelage pour LSTM
        X_train_lstm = y_train_scaled[:-1]
        y_train_lstm = y_train_scaled[1:]

        X_train_lstm = X_train_lstm.reshape((X_train_lstm.shape[0], 1, 1))

        # Définition du modèle
        lstm_model = Sequential()
        lstm_model.add(LSTM(50, activation='relu', input_shape=(1, 1)))
        lstm_model.add(Dense(1))
        lstm_model.compile(optimizer='adam', loss='mse')

        # Entrainement
        lstm_model.fit(X_train_lstm, y_train_lstm, epochs=5000, verbose=0)

        # Prédiction
        y_pred_scaled = lstm_model.predict(self.X_test.reshape(self.X_test.shape[0], 1, 1))
        y_pred = scaler.inverse_transform(y_pred_scaled)

        mse_lstm = mean_squared_error(self.y_test, y_pred)
        print(f'Mean Squared Error: {mse_lstm}')

        if mse_arima < mse_lstm:
            print("ARIMA selected as the advanced model")
            self.advanced_model = arima_model
        else:
            print("LSTM selected as the advanced model")
            self.advanced_model = lstm_model

if __name__ == "__main__":
    gaz = Gaz()
    gaz.extract().transform()
    gaz.train_stable_model()
    gaz.train_medium_model()
    gaz.train_advanced_model()
    print("end")
