import random
from virtual_world.location import Location


class LocationHandler:
    def random_near_location(self, location, from_where, step):
        result = Location(0, 0)
        while ((result.x == 0) and (result.y == 0)
               or (location == from_where.return_increased(result))):
            # {//nie wylosuje miejsca gdzie stoje, kiedy rozmnazam
            if bool(random.getrandbits(1)):
                result.change_to(
                    (random.randint(step-1) + 1) * (1 if bool(random.getrandbits(1)) else -1), 0)
            else:
                result.change_to(0, (random.randint(step-1) + 1) * (
                    1 if bool(random.getrandbits(1)) else -1))
        return result
