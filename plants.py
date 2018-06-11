from virtual_world.plant import Plant
from random import randint
from virtual_world.actions import *
from virtual_world.animal import Animal


class Belladonna(Plant):
    def __init__(self):
        super(Belladonna, self).__init__(20)

    def get_name(self):
        return "Belladonna"

    def get_symbol(self):
        return 'b'

    def get_strength(self):
        return 99

    def get_color(self):
        return "black"


class Dandelion(Plant):
    def __init__(self):
        super(Dandelion, self).__init__(70)

    def get_name(self):
        return "Dandelion"

    def get_symbol(self):
        return 'd'

    def get_color(self):
        return "yellow"

    def action(self, organisms):
        spreading_locations = []
        chance_of_spreading = randint(0, 99)
        if self._spreading_probability >= chance_of_spreading:
            for _ in range(0, 2):
                spreading_locations.append(self.choose_new_location(self.get_location()))
            return Spreading(spreading_locations, [])
        return DoNothing()


class Grass(Plant):
    def __init__(self):
        super(Grass, self).__init__(80)

    def get_name(self):
        return "Grass"

    def get_symbol(self):
        return 'g'

    def get_color(self):
        return "green"


class Guarana(Plant):
    def __init__(self):
        super(Guarana, self).__init__(30)

    def get_name(self):
        return "Guarana"

    def get_symbol(self):
        return 'u'

    def get_color(self):
        return "black"

    def is_increasing_strength(self):
        return True

    def get_increase(self):
        return 3


class SosnowskysBorscht(Plant):
    def __init__(self):
        super(SosnowskysBorscht, self).__init__(10)

    def get_name(self):
        return "SosnowskysBorscht"

    def get_symbol(self):
        return 's'

    def get_strength(self):
        return 10

    def get_color(self):
        return "red"

    def action(self, organisms):
        spreading_locations = []
        to_kill = []
        someone_killed = False
        for o in organisms:
            if isinstance(o, Animal) \
                    and o.get_location() == self.get_location().return_increased(Location(-1, 0)) \
                    and o.get_location() == self.get_location().return_increased(Location(1, 0)) \
                    and o.get_location() == self.get_location().return_increased(Location(0, -1)) \
                    and o.get_location() == self.get_location().return_increased(Location(0, 1)):
                to_kill.append(o)
                someone_killed = True
        if self._spreading_probability >= randint(0, 99):
            spreading_locations.append(self.choose_new_location(self.get_location()))
            return Spreading(spreading_locations, to_kill)
        if someone_killed:
            return Spreading([], to_kill)
        else:
            return DoNothing()
