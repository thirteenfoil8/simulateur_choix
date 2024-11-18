from manim import * 
import numpy as np
import random
class EquationIllustration(Scene):
     def construct(self):
        # first equation
        equation = MathTex("2x", "-2", "", )
        eq_sign = MathTex("=")
        response = MathTex("0")

        equation.next_to(eq_sign, LEFT) 
        response.next_to(eq_sign, RIGHT)  
        self.play(Write(equation))
        self.play(Write(eq_sign))
        self.play(Write(response))
        self.wait()

        # Add moving frames
        framebox1 = SurroundingRectangle(equation[1], buff=.1)
        framebox2 = SurroundingRectangle(response[0], buff=.1) 
        self.play(Create(framebox1))  # creating the frame 
        self.play(ReplacementTransform(framebox1, framebox2))

        # operation
        operation1 = MathTex("+2").set_color(YELLOW).next_to(response, RIGHT, buff=1.5)
        vertical_bar1 = Line(UP * 3.5, DOWN * 3.5).next_to(response, RIGHT, buff=1)
        self.play(Write(operation1), Create(vertical_bar1))

        # Create animations
        self.play(FadeOut(framebox1))
        self.play(FadeOut(framebox2))

        ##################################################


        equation1 = MathTex("2x")
        eq_sign1 = MathTex("=")
        response1 = MathTex("2")

        # shift for next equation
        eq_sign1.shift(DOWN)
        equation1.shift(DOWN)
        equation1.next_to(eq_sign1, LEFT) 
        response1.next_to(eq_sign1, RIGHT)

        self.play(Write(equation1))
        self.play(Write(eq_sign1))
        self.play(Write(response1))
        self.wait()

        # Add moving frames
        framebox1 = SurroundingRectangle(equation1[0], buff=.1)
        framebox2 = SurroundingRectangle(response1[0], buff=.1) 
        self.play(Create(framebox1))  # creating the frame 
        self.play(ReplacementTransform(framebox1, framebox2))


        # operation
        operation2 = MathTex(":2").set_color(YELLOW).next_to(response1, RIGHT, buff=1.5)
        self.play(Write(operation2))

        # Create animations
        self.play(FadeOut(framebox1))
        self.play(FadeOut(framebox2))

        ##################################################
        self.play(
            *[FadeOut(mob, target_position=Dot(UP * random.randrange(-3,3) + LEFT * random.randrange(-3,3)))for mob in self.mobjects]
        )

        # Equation 2
        equation2 = MathTex("x").scale(2)
        eq_sign2 = MathTex("=").scale(2)
        response2 = MathTex("1").scale(2)

        # shift for next equation
        eq_sign2.shift(UP)
        equation2.shift(UP)
        equation2.next_to(eq_sign2, LEFT) 
        response2.next_to(eq_sign2, RIGHT)


        self.play(Write(equation2))
        self.play(Write(eq_sign2))
        self.play(Write(response2))
        self.wait()

        # Add moving frames
        framebox1 = SurroundingRectangle(response2[0], buff=.1)
        self.play(Create(framebox1))  # creating the frame 
        self.wait()

        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
        )
