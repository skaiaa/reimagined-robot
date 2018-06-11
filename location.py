from random import randint


class Location:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    @classmethod
    def get_random_location(cls, width, height):
        return cls(randint(0, width), randint(0, height))

    def return_increased(self, other):
        return Location(other.x + self.x, other.y + self.y)

    def change_to(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)
