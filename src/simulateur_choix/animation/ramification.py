from manim import *
import random

class LuminescentPath(Scene):
    def construct(self):
        # Point de départ (tout à gauche de l'écran)
        start_point = Dot(color=YELLOW, radius=0.15).move_to(LEFT * 6)
        self.play(FadeIn(start_point, scale=0.5))
        self.wait(0.5)

        # Fonction pour créer une branche lumineuse
        def create_branch(start, angle, length, depth=0, max_depth=5):
            if depth > max_depth:  # Limiter la profondeur des ramifications
                return VGroup()

            # Créer une ligne à partir du point de départ
            end_point = start + length * np.array([np.cos(angle), np.sin(angle), 0])
            branch = Line(start, end_point, stroke_color=YELLOW, stroke_width=4)

            # Ajouter des sous-branches
            sub_branches = VGroup()
            if depth < max_depth:  # Générer des ramifications seulement jusqu'à une certaine profondeur
                num_branches = random.randint(2, 4)  # Plus de ramifications par branche
                for _ in range(num_branches):
                    # Contrôler les angles pour éviter les entrechoquements
                    sub_angle = angle + random.uniform(-PI / 5, PI / 5)  
                    sub_length = length * random.uniform(0.5, 0.8)  # Longueur réduite à chaque niveau
                    sub_branches.add(create_branch(end_point, sub_angle, sub_length, depth + 1, max_depth))

            return VGroup(branch, sub_branches)

        # Générer le chemin principal avec ramifications
        main_path = create_branch(start=start_point.get_center(), angle=0, length=3, depth=0, max_depth=5)

        # Animation de chaque segment avec un effet lumineux
        def animate_branch(branch_group):
            animations = []
            for obj in branch_group:
                if isinstance(obj, Line):
                    animations.append(Create(obj))
                elif isinstance(obj, VGroup):
                    animations.extend(animate_branch(obj))
            return animations

        # Exécution de l'animation
        self.play(AnimationGroup(*animate_branch(main_path), lag_ratio=0.05, run_time=12))
        self.wait(1)

        # Dissipation finale
        self.play(FadeOut(main_path, scale=0.8), FadeOut(start_point), run_time=2)
