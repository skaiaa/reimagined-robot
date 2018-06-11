from virtual_world.organism import Organism
import random
from virtual_world.actions import *


class Animal(Organism):
    def __init__(self, init_strength, location_handler):
        super(Animal, self).__init__()
        self._location_handler = location_handler
        self._step = 1
        self._strength = init_strength

    def set_step(self, step):
        self._step = step

    def get_strength(self):
        return self._strength

    def set_strength(self, s):
        self._strength = s

    def info_for_save(self):
        return str(self._age) + " " + str(self._step) + " " + str(self._strength) \
               + " " + str(self._location.x) + " " + str(self._location.y) + "\n"

    def get_stats_from_file(self, line):
        line = line.split()
        self._age = int(line[0])
        self._step = int(line[1])
        self._strength = int(line[2])
        self._location.x = int(line[3])
        self._location.y = int(line[4])

    def choose_new_location(self, from_where):
        # Random random=new Random();
        change_in_location = self._location_handler.random_near_location(self.get_location(), from_where, self._step)
        return Location(from_where.return_increased(change_in_location))

    def action(self, organisms):
        return Moving(self.choose_new_location(self.get_location()), [])

    def collision(self, with_organism, place):
        to_kill = []
        if with_organism.get_symbol() == self.get_symbol():
            return Reproducing(self.choose_new_location(place))
        else:
            if with_organism.get_strength() <= self.get_strength():
                to_kill.append(with_organism)

            else:
                to_kill.append(self)
                # przegral i sam sie zabija:(
            if with_organism.is_deflecting_attack(self):
                return DoNothing()
            if with_organism.is_running_away():
                return TryingToCatchIt(with_organism.choose_new_location(place), to_kill)
            return Fighting(place, to_kill)
