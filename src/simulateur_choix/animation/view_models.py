from manim import *
from simulateur_choix.script.gaz import Gaz
from datetime import datetime, timedelta
import numpy as np
import random

class PlotDataAndPredictions(Scene):
    def construct(self):
        self.gaz = Gaz()
        self.gaz.extract().transform()
        self.gaz.train_linear_model()

        # Convert datetime64[ns] to number of days since the first date
        days_since_start = (self.gaz.df.month - self.gaz.df.month.min()) / np.timedelta64(1, 'D')

        # Define the axes
        axes, x_axis_labels, axes_labels = self.setup_axes(days_since_start=days_since_start)

        # Title
        title = Text("Évolution du prix de l'essence", color=WHITE, font="JetBrains Mono").scale(0.5)
        title.move_to(UP*3)

        # Creating an interpolated line
        line_points = [axes.c2p(x, y) for x, y in zip(days_since_start, self.gaz.df.price)]
        interpolated_line = VMobject().set_points_as_corners(line_points).set_color(YELLOW)
        price_label = Text("Prix", color=YELLOW, font= "JetBrains Mono").scale(0.5).next_to(title, DOWN)

        # Predictions for all dates in df.month
        predicted_prices_linear = [self.gaz.predict(date, model_type="linear")[0][0] for date in self.gaz.df.month]
        line_points_linear = [axes.c2p(x, y) for x, y in zip(days_since_start, predicted_prices_linear)]
        interpolated_line_linear = VMobject().set_points_as_corners(line_points_linear).set_color(GREEN)
        linear_label = Text("Prédiction linéaire", color=GREEN, font= "JetBrains Mono").scale(0.5).next_to(price_label, DOWN)



        # Displaying the axes first
        axes.add(axes_labels)
        self.play(
            Write(title),
            Create(axes),
            Write(x_axis_labels),
            run_time=2
        )
        
        self.wait(1)

        # Drawing the interpolated line and predictions
        self.play(Write(price_label), run_time=2)
        self.play(Create(interpolated_line),run_time=4)
        dots_group = self.add_intersections_and_labels(axes, days_since_start)
        self.play(Write(linear_label), run_time=2)
        self.play(Create(interpolated_line_linear), run_time=4)
        self.wait(2)

        

        # SECOND PART

        # Calculer les prédictions jusqu'en 2060
        end_date = datetime(2060, 1, 1)
        days_until_2060 = (end_date - self.gaz.df.month.min()) / np.timedelta64(1, 'D')
        dates_until_2060 = [self.gaz.df.month.min() + np.timedelta64(int(day), 'D') for day in np.arange(0, days_until_2060, 30)]  # Every month until 2060

        predicted_prices_linear_2060 = [self.gaz.predict(date, model_type="linear")[0][0] for date in dates_until_2060]

        # Étendre dynamiquement le graphe
        num_ticks = 6
        tick_interval = days_until_2060 / (num_ticks - 1)
        new_axes = Axes(
            x_range=[0, days_until_2060, tick_interval],
            y_range=[1, 4, 1],
            axis_config={"color": WHITE},
            y_axis_config={
                "include_numbers": True,
            }
        )
        self.play(
            FadeOut(dots_group),
            FadeOut(interpolated_line),
            FadeOut(interpolated_line_linear),
            run_time=2
        )
        
        self.remove(axes_labels)
        new_x_axis_labels = self.create_x_label(days_until_2060, new_axes)
        self.play(
            FadeOut(axes),
            FadeOut(x_axis_labels),
            run_time=2
        )
        self.play(
            FadeIn(new_axes),
            FadeIn(new_x_axis_labels),
            run_time=2
        )
        axes = new_axes
        x_axis_labels = new_x_axis_labels

        # Dessiner les nouvelles prédictions
        line_points_linear_2060 = [axes.c2p(x, y) for x, y in zip(np.arange(0, days_until_2060, 30), predicted_prices_linear_2060)]
        interpolated_line_linear_2060 = VMobject().set_points_as_corners(line_points_linear_2060).set_color(GREEN)

        self.play(Create(interpolated_line_linear_2060), run_time=4)
        dots_group = self.add_intersections_and_labels(axes, dates_until_2060, predicted_prices_linear_2060)
        self.wait(2)
        self.play(
            *[FadeOut(mob, target_position=Dot(UP * random.randrange(-3,3) + LEFT * random.randrange(-3,3)))for mob in self.mobjects]
        )


    def setup_axes(self, days_since_start):
        # Convert days since start back to datetime
        num_ticks = 6
        tick_interval = max(days_since_start) / (num_ticks - 1)

        axes = Axes(
            x_range=[0, max(days_since_start), tick_interval],
            y_range=[1, 4, 1],  # Setting y-axis range from 1 to 4
            axis_config={"color": WHITE},
            y_axis_config={
                "include_numbers": True,
            }
        )

        axes_labels = axes.get_axis_labels(x_label="temps", y_label="prix")

        x_axis_labels = self.create_x_label(days_since_start, axes)
        return axes, x_axis_labels, axes_labels

    def create_x_label(self, days_since_start, axes):
        if isinstance(days_since_start, float):
            values_x = [(x, self.days_to_date(x)) for x in np.linspace(0, days_since_start, 6)]
        else:
            values_x = [(x, self.days_to_date(x)) for x in np.linspace(0, max(days_since_start), 6)]

        x_axis_labels = VGroup()
        for x_val, x_tex in values_x:
            tex = MathTex(x_tex)
            tex.scale(0.6)  # Increase the scale a bit
            tick_point = axes.c2p(x_val, 1)
            tex.next_to(tick_point, DOWN, buff= 0.2)  # Adjust the position to be clearly below the x-axis
            x_axis_labels.add(tex)
        self.values_x = values_x
        return x_axis_labels

    def days_to_date(self, days: float) -> str:
            date = self.gaz.df.month.min() + timedelta(days=days)
            return date.strftime('%Y-%m')


    def update_axes(self, axes, new_x_range):
        axes.x_range = new_x_range
        axes.clear()
        axes.add_coordinates()
        return axes
    

    def add_intersections_and_labels(self, axes, days_since_start, line=None):

        dots_group = VGroup()

        # Prendre les 5 premières valeurs de days_since_start et line
        indices = np.linspace(100, len(days_since_start) - 1, 5).astype(int)
        
        if line is None:
            x_vals = days_since_start.iloc[indices].values
            y_vals = self.gaz.df.price.iloc[indices]
        else:
            days_since_start = np.array(days_since_start)
            indices = np.array(indices, dtype=int)
            x_vals = days_since_start[indices]
            line = np.array(line)
            y_vals = line[indices]
        for x_val, y_val in zip(x_vals, y_vals):
            # Ajouter un point d'intersection à une position spécifique
            if line is None:
                dot = Dot(axes.c2p(x_val, y_val), color=YELLOW)
            else:
                x_val_days = (x_val - self.gaz.df.month.min()) / np.timedelta64(1, 'D')
                dot = Dot(axes.c2p(x_val_days, y_val), color=GREEN)
            
            # Ajouter une valeur sur l'axe des y pour indiquer cette intersection
            y_label = MathTex(f"{y_val:.2f}").scale(0.5).next_to(dot, UP, buff=0.5)
            dots_group.add(dot, y_label)
            
            self.play(Create(dot), Write(y_label), run_time=0.5)
        return dots_group
