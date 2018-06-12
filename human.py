from virtual_world.animal import Animal
from virtual_world.actions import *


class Human(Animal):
    def __init__(self, lh):
        super(Human, self).__init__(5, lh)
        self._my_move = Location(0, 0)
        self._magic_potion = 0
        self._using_special_ability = 0

    def get_name(self):
        return "Marcin"

    def get_initiative(self):
        return 4

    def get_symbol(self):
        return 'H'

    def get_color(self):
        return "pink"

    def info_for_save(self):
        return str(self._age) + " " + str(self._step) + " " + str(self._strength) \
               + " " + str(self._location.x) + " " + str(self._location.y) \
               + " " + str(self._magic_potion) + " " + str(self._using_special_ability) + "\n"

    def get_stats_from_file(self, line):
        super().get_stats_from_file(line)
        self._magic_potion = int(line[5])
        self._using_special_ability = int(line[6])

    def get_strength(self):
        return super(Human, self).get_strength() + self._magic_potion

    def action(self, organisms):
        if self._my_move != Location(0, 0):
            move = self.get_location().return_increased(self._my_move)
            self._my_move = Location(0, 0)
            return Moving(move, [])
        elif self._magic_potion == 5:
            return ActivatingSpecialAbility("magic potion", [])
        else:
            return DoNothing()

    def grow_older(self):
        if self._magic_potion > 0:
            self._magic_potion -= 1
        if 0 < self._using_special_ability < 12:
            self._using_special_ability += 1
        self._age += 1

    def key_typed(self, e):
        key = e.keysym

        if key == 'P':
            if self._using_special_ability == 0:
                self._magic_potion = 5
                self._using_special_ability = 1
        if key == "Up":
            self._my_move = Location(0, -1)
        if key == "Down":
            self._my_move = Location(0, 1)
        if key == "Left":
            self._my_move = Location(-1, 0)
        if key == "Right":
            self._my_move = Location(1, 0)
