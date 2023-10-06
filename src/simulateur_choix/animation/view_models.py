from manim import *
from simulateur_choix.script.gaz import Gaz
import numpy as np

class PlotDataAndPredictions(Scene):
    def construct(self):
        gaz = Gaz()
        gaz.extract().transform()
        gaz.train_stable_model()

        # Convert datetime64[ns] to number of days since the first date
        days_since_start = (gaz.df.month - gaz.df.month.min()) / np.timedelta64(1, 'D')

        axes = Axes(
            x_range=[0, max(days_since_start) + 10],
            y_range=[min(gaz.df.price) - 1, max(gaz.df.price) + 1],
            axis_config={"color": WHITE},
            y_axis_config={"color": BLUE},
        )

        # Title
        title = Text("Évolution du prix de l'essence", color=WHITE, font= "JetBrains Mono").scale(0.5)
        title.move_to(UP*3)

        # Creating an interpolated line
        line_points = [axes.c2p(x, y) for x, y in zip(days_since_start, gaz.df.price)]
        interpolated_line = VMobject().set_points_as_corners(line_points).set_color(YELLOW)

        # Displaying the axes first
        self.play(
            Write(title),
            Create(axes),
            run_time=2
        )
        self.wait(1)

        # Drawing the interpolated line
        self.play(
            Create(interpolated_line),
            run_time=4
        )
        self.wait(2)