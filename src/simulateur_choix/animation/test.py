from manim import *

class Myscene(Scene):
    def construct(self):
        axes = Axes()
        self.play(Create(axes))
        self.wait(5)