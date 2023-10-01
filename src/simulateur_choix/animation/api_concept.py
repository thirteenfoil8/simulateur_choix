from manim import *
#manim -pql api_concept.py APIConcept -p 

class APIConcept(Scene):
    def construct(self):
        # Robot (votre application web)
        robot = Circle(radius=0.8, fill_color=BLUE, fill_opacity=0.8).move_to(LEFT * 4)
        robot_eyes = VGroup(
            Dot(point=LEFT * 4 + UP * 0.2 + LEFT * 0.2),
            Dot(point=LEFT * 4 + UP * 0.2 + RIGHT * 0.2)
        )
        robot_label = Text("Application Web", font_size=18, font= "JetBrains Mono").next_to(robot, DOWN)

        # Bibliothèque (API de Google Maps)
        library = Rectangle(height=2, width=1.5, color=WHITE, fill_color=GREEN, fill_opacity=0.7).move_to(RIGHT * 4)
        library_label = Text("Google Maps Data", font_size=18, font= "JetBrains Mono").next_to(library, DOWN)

        # Drone (API)
        drone = Circle(radius=0.3, fill_color=YELLOW, fill_opacity=0.8)
        drone_label = Text("API", font_size=18, font= "JetBrains Mono").next_to(drone, DOWN)

        # Animation
        self.play(FadeIn(robot), FadeIn(robot_eyes), Write(robot_label))
        self.play(FadeIn(library), Write(library_label))
        self.wait(3)

        # Envoi du drone pour chercher des informations
        drone.move_to(robot.get_right() + RIGHT)
        self.play(FadeIn(drone), Write(drone_label))
        self.play(drone.animate.move_to(library.get_left() + LEFT))
        self.wait(2)

        # Drone revient avec un livre (données)
        book = Rectangle(height=0.5, width=0.3, color=WHITE, fill_color=RED, fill_opacity=0.7).next_to(drone, UP)
        book_drone = VGroup(drone, book)
        self.play(FadeIn(book))
        self.wait(1)
        self.play(book_drone.animate.move_to(robot.get_right() + RIGHT))

        # Préparer les labels
        open_book_label_1 = Text("Distance en voiture", font_size=14, font= "JetBrains Mono")
        open_book_label_2 = Text("Temps de trajet", font_size=14, font= "JetBrains Mono").next_to(open_book_label_1, DOWN, buff=0.1)
        open_book_labels = VGroup(open_book_label_1, open_book_label_2).center()

        # Calculer la taille nécessaire pour les arcs basée sur la taille du texte
        arc_width = open_book_labels.width / 2 + 0.2  # Ajouter un petit espace
        arc_height = open_book_labels.height + 0.2  # Ajouter un petit espace

        # Créer les arcs
        left_arc = Arc(start_angle=PI/2, angle=PI, radius=arc_width).set_height(arc_height).set_fill(RED, opacity=0.7).next_to(open_book_labels, LEFT, buff=0.1)
        right_arc = Arc(start_angle=-PI/2, angle=PI, radius=arc_width).set_height(arc_height).set_fill(RED, opacity=0.7).next_to(open_book_labels, RIGHT, buff=0.1)
        
        open_book_group = VGroup(left_arc, right_arc)

        # Animation
        self.play(Transform(book, open_book_group), FadeIn(open_book_labels))
        self.wait(3)
        self.play(FadeOut(open_book_group), FadeOut(open_book_labels),FadeOut(book))
        self.play(FadeOut(drone), FadeOut(drone_label))
        self.wait(1)


        # Conclusion
        conclusion = Text("L'API est comme un drone qui récupère les données pour l'application", font_size=24, font= "JetBrains Mono").move_to(UP*2)
        self.play(Write(conclusion))
        self.wait(1)
        self.play(FadeOut(conclusion))
        self.wait(2)