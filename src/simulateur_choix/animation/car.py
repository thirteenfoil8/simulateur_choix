from manim import *

class CarOnTheRoad(Scene):
    def construct(self):
        # Maison
        house_base = Rectangle(height=0.5, width=0.5, color=WHITE, fill_color=BLUE, fill_opacity=0.7).move_to(LEFT * 4)
        roof = Polygon(
            house_base.get_corner(UP + LEFT),
            house_base.get_corner(UP + RIGHT),
            house_base.get_center() + UP * 0.5,
            color=WHITE, fill_color=BLUE, fill_opacity=0.7
        )
        house = VGroup(house_base, roof)
        house_label = Text("Maison", font_size=18, font= "JetBrains Mono").next_to(house, DOWN)
        house_group = VGroup(house, house_label)

        # Immeuble
        building_base = Rectangle(height=2, width=0.8, color=WHITE, fill_color=GRAY, fill_opacity=0.7)
        windows = VGroup(*[
            Rectangle(height=0.2, width=0.2, color=WHITE, fill_color=BLUE, fill_opacity=0.7)
            for _ in range(4)
        ])
        windows.arrange(DOWN, buff=0.3)
        windows.move_to(building_base)
        building = VGroup(building_base, windows)
        building.next_to(house, RIGHT, buff=4).move_to(RIGHT * 4)
        building_label = Text("Travail", font_size=18, font= "JetBrains Mono").next_to(building, DOWN)
        building_group = VGroup(building, building_label)

        # Trajet (route)
        road = CurvedArrow(start_point=house.get_right(), end_point=building.get_left(), color=WHITE)

        # Voiture initialement grande au centre
        car = Circle(radius=0.8, fill_color=RED, fill_opacity=0.8)
        car_label = Text("Voiture", font_size=18, font= "JetBrains Mono").next_to(car, DOWN)
        self.play(FadeIn(car), Write(car_label))
        self.play(FadeOut(car_label))
        self.wait(1)

        

        self.play(Write(house), Write(house_label))
        self.play(Write(building), Write(building_label))
        self.play(Create(road))

        # Redéfinir la position et la taille cibles pour la voiture
        car.target = car.copy().scale(0.5).move_to(road.get_start()) 

        # Animation de la voiture vers sa position initiale
        self.play(MoveToTarget(car))

        # Animation de la voiture le long de la route
        self.play(MoveAlongPath(car, road))
        self.play(FadeOut(car))
        self.play(FadeOut(road))

        self.wait(2)

        # Indiquer un rapprochement de 20 kilomètres
        rapprochement = Text("Rapprochement de 5 kilomètres", font_size=24, font= "JetBrains Mono").move_to(UP*2)
        self.play(Write(rapprochement))
        self.wait(2)
        self.play(FadeOut(rapprochement))

        # Rapprocher la maison et l'immeuble
        self.play(
            house_group.animate.move_to(LEFT * 2),
            building_group.animate.move_to(RIGHT * 2)
        )

        # Redéfinir la route après le rapprochement
        road_new = CurvedArrow(start_point=house.get_right(), end_point=building.get_left(), color=WHITE)
        self.play(Create(road_new))

        # Faire réapparaître la voiture et la déplacer
        car.move_to(road_new.get_start()) 
        self.play(FadeIn(car))
        self.play(MoveAlongPath(car, road_new))

        self.wait(2)
