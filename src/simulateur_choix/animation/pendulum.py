from manim import *
import numpy as np
from scipy.integrate import solve_ivp

class DoubleTriplePendulum(Scene):
    def construct(self):

        # Ajouter un titre
        title = Text("L'impact des choix", color=WHITE, font_size=48)
        self.play(FadeIn(title))
        self.wait(3)
        self.play(title.animate.to_edge(UP), run_time=2)

        # Longueurs, masses et gravité
        L1, L2, L3 = 1.5, 1.2, 1.0
        M1, M2, M3 = 1, 1, 1
        g = 9.8

        # Conditions initiales
        initial_conditions = [np.pi / 2, np.pi / 4, np.pi / 6, 0, 0, 0]
        initial_conditions_perturbed = [np.pi / 2 + 0.2, np.pi / 4, np.pi / 6, 0, 0, 0]

        # Temps pour la simulation
        t_max = 10
        dt = 0.01
        t_eval = np.arange(0, t_max, dt)

        # Fonction décrivant les équations différentielles du triple pendule
        def triple_pendulum_derivatives(t, y):
            θ1, θ2, θ3, ω1, ω2, ω3 = y

            sin = np.sin
            cos = np.cos

            m12 = M1 + M2
            m123 = M1 + M2 + M3

            dω1 = (
                -g * (2 * m12 + M3) * sin(θ1)
                - M3 * g * sin(θ1 - 2 * θ3)
                - 2 * sin(θ1 - θ2) * M2 * (ω2**2 * L2 + ω1**2 * L1 * cos(θ1 - θ2))
            ) / (L1 * (2 * m12 + M3 - M2 * cos(2 * θ1 - 2 * θ2)))

            dω2 = (
                2
                * sin(θ1 - θ2)
                * (
                    ω1**2 * L1 * m12
                    + g * m12 * cos(θ1)
                    + ω2**2 * L2 * M2 * cos(θ1 - θ2)
                )
            ) / (L2 * (m12 - M2 * cos(2 * θ1 - 2 * θ2)))

            dω3 = -g * sin(θ3) / L3

            return [ω1, ω2, ω3, dω1, dω2, dω3]

        # Résoudre les équations différentielles
        solution = solve_ivp(
            triple_pendulum_derivatives,
            [0, t_max],
            initial_conditions,
            t_eval=t_eval,
            method="RK45",
        )
        solution_perturbed = solve_ivp(
            triple_pendulum_derivatives,
            [0, t_max],
            initial_conditions_perturbed,
            t_eval=t_eval,
            method="RK45",
        )

        # Extraire les solutions
        θ1, θ2, θ3 = solution.y[0], solution.y[1], solution.y[2]
        θ1_p, θ2_p, θ3_p = solution_perturbed.y[0], solution_perturbed.y[1], solution_perturbed.y[2]

        # Création des pendules gauche et droit
        pendulum_left = self.create_pendulum(-3, L1, L2, L3, RED, BLUE, GREEN)
        pendulum_right = self.create_pendulum(3, L1, L2, L3, RED, BLUE, GREEN)
        self.update_pendulum(pendulum_left, θ1[0], θ2[0], θ3[0], L1, L2, L3)
        self.update_pendulum(pendulum_right, θ1_p[0], θ2_p[0], θ3_p[0], L1, L2, L3)

        # Apparition progressive du pendule de gauche
        self.play(Create(pendulum_left["rod1"]), FadeIn(pendulum_left["mass1"]), run_time=1)
        label_a = Text("Choix A", font_size=24, color=RED).next_to(pendulum_left["mass1"], RIGHT)
        self.play(FadeIn(label_a))

        self.play(Create(pendulum_left["rod2"]), FadeIn(pendulum_left["mass2"]), run_time=1)
        label_b = Text("Choix B", font_size=24, color=BLUE).next_to(pendulum_left["mass2"], RIGHT)
        self.play(FadeIn(label_b))

        self.play(Create(pendulum_left["rod3"]), FadeIn(pendulum_left["mass3"]), run_time=1)
        label_c = Text("Choix C", font_size=24, color=GREEN).next_to(pendulum_left["mass3"], RIGHT)
        self.play(FadeIn(label_c))

        self.play(
            FadeIn(pendulum_left["group"]),
            run_time=0.001
        )

        # Suppression des étiquettes
        self.wait(1)
        self.play(FadeOut(label_a), FadeOut(label_b), FadeOut(label_c))

        # Apparition du pendule de droite en une fois avec une flèche et sous-titre
        arrow = Arrow(
            start=pendulum_right["mass1"].get_center() + 0.5 * DOWN,
            end=pendulum_right["mass1"].get_center(),
            color=YELLOW,
            buff=0.5,
        )
        label_ap = Text("Choix A'", font_size=24, color=YELLOW).next_to(pendulum_right["mass1"], RIGHT)

        self.play(
            FadeIn(pendulum_right["group"]),
            GrowArrow(arrow),
            FadeIn(label_ap),
            run_time=2
        )
        self.wait(1)
        self.remove(arrow, label_ap)

        # Tracker pour synchroniser le temps
        time_tracker = ValueTracker(0)

        # Mise à jour des pendules
        def update_pendulums(mobject):
            t = time_tracker.get_value()
            idx = min(int(t * len(t_eval) / t_max), len(t_eval) - 1)
            self.update_pendulum(pendulum_left, θ1[idx], θ2[idx], θ3[idx], L1, L2, L3)
            self.update_pendulum(pendulum_right, θ1_p[idx], θ2_p[idx], θ3_p[idx], L1, L2, L3)

        # Ajouter les updaters
        pendulum_left["group"].add_updater(update_pendulums)
        pendulum_right["group"].add_updater(update_pendulums)

        # Ajouter les pendules et leurs traces
        self.add(pendulum_left["trace1"], pendulum_left["trace2"], pendulum_left["trace3"])
        self.add(pendulum_right["trace1"], pendulum_right["trace2"], pendulum_right["trace3"])

        # Lancer la simulation
        self.play(time_tracker.animate.set_value(t_max), run_time=t_max * 1.5, rate_func=linear)
        
        def fade_out_pendulum(pendulum):
            """Anime la disparition fluide d'un pendule."""
            animations = [
                FadeOut(pendulum["rod1"], shift=DOWN),
                FadeOut(pendulum["rod2"], shift=DOWN),
                FadeOut(pendulum["rod3"], shift=DOWN),
                ShrinkToCenter(pendulum["mass1"]),
                ShrinkToCenter(pendulum["mass2"]),
                ShrinkToCenter(pendulum["mass3"]),
            ]
            return animations
        self.play(
        *fade_out_pendulum(pendulum_left),
        *fade_out_pendulum(pendulum_right),
        run_time=2
        )
        self.play(FadeOut(title, shift=UP), run_time=2)
        self.wait(1)

        title = Text("Quel est l'impact de nos choix ?", color=WHITE, font_size=48)
        self.play(FadeIn(title))
        self.wait(3)
        self.play(FadeOut(title), run_time=2)



    def create_pendulum(self, x_shift, L1, L2, L3, color1, color2, color3):
        """Crée un pendule avec des traces."""
        rod1 = Line(ORIGIN, ORIGIN + L1 * DOWN, color=WHITE).shift(x_shift * RIGHT)
        rod2 = Line(rod1.get_end(), rod1.get_end() + L2 * DOWN, color=WHITE)
        rod3 = Line(rod2.get_end(), rod2.get_end() + L3 * DOWN, color=WHITE)

        mass1 = Dot(rod1.get_end(), radius=0.08, color=color1)
        mass2 = Dot(rod2.get_end(), radius=0.08, color=color2)
        mass3 = Dot(rod3.get_end(), radius=0.08, color=color3)

        pendulum_group = VGroup(rod1, rod2, rod3, mass1, mass2, mass3)

        trace1 = TracedPath(mass1.get_center, dissipating_time=0.5, stroke_opacity=[0, 1], stroke_color=color1, stroke_width=2)
        trace2 = TracedPath(mass2.get_center, dissipating_time=0.5, stroke_opacity=[0, 1], stroke_color=color2, stroke_width=2)
        trace3 = TracedPath(mass3.get_center, dissipating_time=0.5, stroke_opacity=[0, 1], stroke_color=color3, stroke_width=2)

        return {
            "rod1": rod1,
            "rod2": rod2,
            "rod3": rod3,
            "mass1": mass1,
            "mass2": mass2,
            "mass3": mass3,
            "group": pendulum_group,
            "trace1": trace1,
            "trace2": trace2,
            "trace3": trace3,
        }

    def update_pendulum(self, pendulum, θ1, θ2, θ3, L1, L2, L3):
        """Met à jour les positions des pendules."""
        x1 = L1 * np.sin(θ1)
        y1 = -L1 * np.cos(θ1)
        x2 = x1 + L2 * np.sin(θ2)
        y2 = y1 - L2 * np.cos(θ2)
        x3 = x2 + L3 * np.sin(θ3)
        y3 = y2 - L3 * np.cos(θ3)

        x_shift = pendulum["rod1"].get_start()[0]
        pendulum["rod1"].put_start_and_end_on(
            [x_shift, 0, 0], [x1 + x_shift, y1, 0]
        )
        pendulum["rod2"].put_start_and_end_on(
            [x1 + x_shift, y1, 0], [x2 + x_shift, y2, 0]
        )
        pendulum["rod3"].put_start_and_end_on(
            [x2 + x_shift, y2, 0], [x3 + x_shift, y3, 0]
        )

        pendulum["mass1"].move_to([x1 + x_shift, y1, 0])
        pendulum["mass2"].move_to([x2 + x_shift, y2, 0])
        pendulum["mass3"].move_to([x3 + x_shift, y3, 0])
