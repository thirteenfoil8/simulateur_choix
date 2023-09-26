from manim import *

class MVPTerm(Scene):
    def construct(self):
        # Définition de la mise en forme du texte
        default_text_config = {
            "font_size": 24,
            "color": WHITE,
            "font": "JetBrains Mono"
        }

        # Terme MVP et sa définition
        mvp_term = Text("\"MVP\"", color=BLUE, font_size=28)
        mvp_def = Text("pour \"Minimum Valuable Product\"", **default_text_config)
        mvp_def.next_to(mvp_term, DOWN, buff=0.2)
        mvp_group = Group(mvp_term, mvp_def)


        # Animation
        self.play(FadeIn(mvp_group))

        self.wait(10)