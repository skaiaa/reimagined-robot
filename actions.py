from abc import *
from virtual_world.location import Location


class Action(ABC):

    def is_moving(self):
        return False

    def is_spreading(self):
        return False

    def is_reproducing(self):
        return False

    def is_fighting(self):
        return False

    def is_trying_to_catch_it(self):
        return False

    def is_activating_special_ability(self):
        return False

    def kills(self):
        pass


class Moving(Action):

    def __init__(self, new_location, to_kill):
        self.new_location = new_location
        self.to_kill = to_kill

    def is_moving(self):
        return True

    def get_move(self):
        return self.new_location

    def kills(self):
        return self.to_kill  # same


class DoNothing(Action):
    def kills(self):
        return ()


class Fighting(Action):
    fight_location = Location()
    to_kill = ()

    def __init__(self, fight_location, to_kill):
        self.to_kill = to_kill
        self.fight_location = fight_location

    def is_fighting(self):
        return True

    def get_fight(self):
        return self.fight_location

    def kills(self):
        return self.to_kill


class Reproducing(Action):
    new_location = Location()

    def __init__(self, new_location):
        self.new_location = new_location

    def is_reproducing(self):
        return True

    def get_reproduce(self):
        return self.new_location

    def kills(self):
        return ()


class Spreading(Action):
    to_locations = ()
    to_kill = ()

    def __init__(self, to_locations, to_kill):
        self.to_locations = to_locations
        self.to_kill = to_kill

    def is_spreading(self):
        return True

    def get_spread(self):
        return self.to_locations

    def kills(self):
        return self.to_kill


class TryingToCatchIt(Action):
    new_location = Location()
    to_kill = ()

    def __init__(self, new_location, to_kill):
        self.new_location = new_location
        self.to_kill = to_kill

    def is_trying_to_catch_it(self):
        return True

    def get_catch(self):
        return self.new_location

    def kills(self):
        return ()


class ActivatingSpecialAbility(Action):
    ability = ""
    to_kill = ()

    def __init__(self, ability, to_kill):
        self.ability = ability
        self.to_kill = to_kill

    def is_activating_special_ability(self):
        return True

    def get_ability(self):
        return self.ability

    def kills(self):
        return self.to_kill
