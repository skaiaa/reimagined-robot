from virtual_world.organism import Organism
from random import randint
from virtual_world.actions import *


class Plant(Organism):
    def __init__(self, prob):
        super(Plant, self).__init__()
        self._spreading_probability = prob

    def get_initiative(self):
        return 0

    def get_strength(self):
        return 0

    def set_strength(self, s):
        pass

    def info_for_save(self):
        return str(self._age) + " " + str(self._spreading_probability) + " " + str(self.get_location().x) + " " + str(
            self.get_location().y) + "\n"

    def get_color(self):
        return "green"

    def retrieve_stats_from_file(self, line):
        self._age = int(line[0])
        self._spreading_probability = int(line[1])
        self._location.x = int(line[2])
        self._location.y = int(line[3])

    def choose_new_location(self, from_where):#OGSAARNIJJJJJJJ,LOCATION HANDLER MA MIECC
        change_in_location = Location(0, 0)
        while (change_in_location.x == 0 and change_in_location.y == 0
               and self.get_location() == from_where.return_increased(change_in_location)):
            change_in_location.change_to(randint(0, 2) - 1, randint(0, 2) - 1)
        return from_where.return_increased(change_in_location)

    def action(self, organisms):
        spreading_locations = []
        chance_of_spreading = randint(0, 99)
        spreading_locations.append(self.choose_new_location(self.get_location()))
        if self._spreading_probability >= chance_of_spreading:
            return Spreading(spreading_locations, [])
        return DoNothing()

    def collision(self, collider, where):
        return DoNothing()
