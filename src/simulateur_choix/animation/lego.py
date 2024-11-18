from manim import *
import random

class BuildingBlocks(Scene):
    def construct(self):
        # Dimensions des blocs
        block_width = 1
        block_height = 0.5
        block_depth = 1

        # Couleurs pour chaque niveau
        level_colors = [BLUE, GREEN, YELLOW, ORANGE, RED]

        # Créer les blocs pour la pyramide
        pyramid = VGroup()
        for level, color in enumerate(level_colors):
            num_blocks = len(level_colors) - level  # Nombre de blocs dans le niveau
            for i in range(num_blocks):
                # Calculer la position pour que les blocs s'alignent en pyramide
                x_offset = (i - (num_blocks - 1) / 2) * block_width
                y_offset = level * block_height -1
                block = Cube(fill_color=GRAY, fill_opacity=0.8)  # Initialement gris
                block.scale([block_width, block_height, block_depth])  # Ajuster les dimensions
                block.target_position = [x_offset, y_offset, 0]  # Sauvegarder la position cible
                pyramid.add(block)

        # Position aléatoire initiale pour désordre
        for block in pyramid:
            block.move_to([random.uniform(-6, 6), random.uniform(-3, 3), 0])  # Position aléatoire

        # Étape 1 : Afficher les blocs gris dispersés
        appear_animations = [FadeIn(block) for block in pyramid]
        self.play(AnimationGroup(*appear_animations, lag_ratio=17 / len(pyramid)))  # Lag ajusté pour 15 sec
        self.wait(1)

        # Étape 2 : Coloration des blocs
        color_animations = []
        idx = 0
        for level, color in enumerate(level_colors):
            num_blocks = len(level_colors) - level
            for i in range(num_blocks):
                color_animations.append(pyramid[idx].animate.set_fill(color))
                idx += 1

        self.play(AnimationGroup(*color_animations, lag_ratio=0.1))  # Appliquer la coloration
        self.wait(3)

        # Étape 3 : Regroupement par couleur (Clustering)
        cluster_positions = [
            [-4, -3.5, 0], [-4, -2, 0], [-4, -0.5, 0], [-4, 1, 0], [-4, 2.5, 0]
        ]  # Positions des clusters
        clustering_animations = []
        idx = 0
        for level, cluster_pos in enumerate(cluster_positions):
            num_blocks = len(level_colors) - level
            for i in range(num_blocks):
                clustering_animations.append(
                    pyramid[idx].animate.move_to(cluster_pos)
                )
                cluster_pos[0] += block_width * 1.2  # Décalage horizontal pour chaque bloc
                idx += 1

        self.play(AnimationGroup(*clustering_animations, lag_ratio=0.1))  # Glisser vers les clusters
        self.wait(3)

        # Étape 4 : Animation pour emboîter les blocs (Pyramide)
        animations = [
            block.animate.move_to(block.target_position) for block in pyramid
        ]
        self.play(AnimationGroup(*animations, lag_ratio=0.1))  # Glisser vers position finale
        self.wait(2)

        # Étape 5 : Encadrer la pyramide finale
        final_structure = SurroundingRectangle(pyramid, color=WHITE, buff=0.2)
        self.play(Create(final_structure))
        self.wait(2)

        self.play(FadeOut(pyramid, final_structure), run_time=2)
