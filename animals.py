from virtual_world.animal import Animal
from random import randint
# import virtual_world.actions as actions
from virtual_world.actions import *
from virtual_world.plants import SosnowskysBorscht


class Sheep(Animal):
    def __init__(self, lh):
        super(Sheep, self).__init__(4,lh)

    def get_name(self):
        return "Sheep"

    def get_initiative(self):
        return 4

    def get_symbol(self):
        return 'S'

    def get_color(self):
        return "white"


class Antelope(Animal):
    def __init__(self,lh):
        super(Antelope, self).__init__(4,lh)
        self.set_step(2)

    def is_running_away(self):
        return randint(0, 99) < 50

    def get_name(self):
        return "Antelope"

    def get_initiative(self):
        return 4

    def get_symbol(self):
        return 'A'

    def get_color(self):
        return "green"


class Fox(Animal):
    def __init__(self,lh):
        super(Fox, self).__init__(3,lh)

    def get_name(self):
        return "Fox"

    def get_initiative(self):
        return 7

    def get_symbol(self):
        return 'F'

    def action(self, organisms):
        new_location = self.choose_new_location(self.get_location())
        for o in organisms:
            if (o.get_location() == new_location) and (o.get_strength > self.get_strength()):
                return DoNothing()
            else:
                return Moving(new_location, [])

    def get_color(self):
        return "orange"


class Turtle(Animal):
    def __init__(self,lh):
        super(Turtle, self).__init__(2,lh)
        self._probability_to_move = 25

    def get_name(self):
        return "Turtle"

    def get_initiative(self):
        return 1

    def get_symbol(self):
        return 'T'

    def get_color(self):
        return "brown"

    def action(self, organisms):
        new_location = self.choose_new_location(self.get_location())
        if randint(0, 99) < self._probability_to_move:
            return Moving(new_location, [])
        else:
            return DoNothing()

    def is_deflecting_attack(self, attacker):
        return attacker.get_strength() < 5


class Wolf(Animal):
    def __init__(self,lh):
        super(Wolf, self).__init__(9,lh)

    def get_name(self):
        return "Wolf"

    def get_initiative(self):
        return 5

    def get_symbol(self):
        return 'W'

    def get_color(self):
        return "gray"


class CyberSheep(Sheep):
    def __init__(self,lh):
        super(CyberSheep, self).__init__(lh)

    def get_name(self):
        return "CyberSheep"

    def get_strength(self):
        return 11

    def get_symbol(self):
        return 'C'

    def get_color(self):
        return "metallic"

    def action(self, organisms):
        def distance(location):
            return abs(self.get_location().x - location.x) + abs(self.get_location().y - location.y)

        borschtes = sorted([(o, distance(o.get_location()))
                            for o in organisms if isinstance(o, SosnowskysBorscht)],
                           key=lambda borscht_with_distance: borscht_with_distance[1])
        if borschtes:
            nearest_borscht_location = borschtes[0][0].get_location()
            move = Location(0, 0)
            if nearest_borscht_location.x < self.get_location().x:
                move.x = -1
            elif nearest_borscht_location.x > self.get_location().x:
                move.x = 1
            elif nearest_borscht_location.y < self.get_location().y:
                move.y = -1
            else:
                move.y = 1
            return Moving(self.get_location().return_increased(move), [])
        else:
            return super(CyberSheep, self).action(organisms)
