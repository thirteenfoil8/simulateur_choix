from manim import *
import numpy as np

class WavePropagation3D(ThreeDScene):
    def construct(self):
        # Configurer la caméra pour un angle 3D
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)

        # Créer un plan incliné sans grille
        plane = Surface(
            lambda u, v: np.array([u, v, 0.3 * u]),  # Plan incliné : z = 0.3 * x
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(20, 20),
        )
        plane.set_style(fill_opacity=0.2, fill_color=BLUE, stroke_opacity=0)  # Désactiver la grille
        self.add(plane)

        # Goutte tombant sur le plan
        drop_path = ParametricFunction(
            lambda t: np.array([0, 0, 3 * (1 - t)]),  # Descente verticale
            t_range=[0, 1],
            color=YELLOW,
        )
        drop = Sphere(radius=0.1, color=YELLOW).move_to(drop_path.points[0])  # Position initiale
        self.add(drop)

        # Faire tomber la goutte
        self.play(MoveAlongPath(drop, drop_path), run_time=1.5)

        # Paramètres de l'onde
        num_waves = 3  # Nombre total de cercles
        wave_stroke_width = 2  # Épaisseur des cercles
        wave_opacity = 0.8  # Opacité initiale
        propagation_time = 3.0  # Temps total de propagation
        lag_between_waves = 0.5  # Temps entre les cercles

        # Création des cercles concentriques partant du centre
        ripples = VGroup()
        for i in range(num_waves):
            ripple = ParametricFunction(
                lambda t: np.array([
                    0.1 * np.cos(t),  # Rayon initial très petit
                    0.1 * np.sin(t),
                    0.3 * 0.1 * np.cos(t)  # Projection sur z = 0.3x
                ]),
                t_range=[0, TAU],
                color=BLUE,
            )
            ripple.set_stroke(width=wave_stroke_width, opacity=wave_opacity)
            ripple.move_to(np.array([0, 0, 0]))  # Position initiale au centre
            ripples.add(ripple)

        # Animation de la propagation depuis le centre
        propagation_animations = [
            ripple.animate.scale(50).set_opacity(0) for ripple in ripples  # Expansion totale
        ]

        # Combiner disparition de la goutte et début des vagues
        self.play(
            AnimationGroup(
                FadeOut(drop),  # Goutte disparaît
                AnimationGroup(*propagation_animations, lag_ratio=lag_between_waves),  # Propagation
            ),
            run_time=propagation_time
        )

        # Transition finale : rotation vers une vue 2D avec changement de couleur progressif
        self.play(
            plane.animate.set_style(fill_opacity=0, fill_color=BLUE, stroke_opacity=0),  # Changement de couleur
            run_time=3
        )
        self.wait(1)
