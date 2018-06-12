from abc import *
from virtual_world.location import Location


class Organism(ABC):
    def __init__(self):
        self._location = Location(-1, -1)
        self._age = 0

    def action(self, organisms):
        pass

    def set_location(self, location):
        self._location = location

    def get_location(self):
        return self._location

    def get_age(self):
        return self._age

    def grow_older(self):
        self._age += 1

    def get_initiative(self):
        pass

    def get_symbol(self):
        pass

    def get_strength(self):
        pass

    def set_strength(self, strength):
        pass

    def get_info_for_save(self):
        pass

    def set_stats_from_file(self, line):
        pass

    def get_color(self):
        pass

    def collision(self, collider, where):
        pass

    def is_running_away(self):
        return False

    def is_deflecting_attack(self, attacker):
        return False

    def is_increasing_strength(self):
        return False

    def get_increase(self):
        return 0

    def choose_new_location(self, from_where):
        pass

    def is_immune_to_killing_by(self, killer):
        return False

    def get_name(self):
        raise RuntimeError("I don't have a name")

    @staticmethod
    def organism_sorting_key(organism):
        return -organism.get_initiative(), -organism.get_age()
