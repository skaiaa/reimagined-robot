from virtual_world.organism import Organism
import random
from virtual_world.animals import *
from virtual_world.plants import *
from virtual_world.human import Human
from virtual_world.location_handler import LocationHandler


class OrganismGenerator:
    @staticmethod
    def get_free_and_random_location(organisms, width, height):
        if len(organisms) >= width * height:
            raise ValueError("There's no place!")
        random_location = Location.get_random_location(width, height)
        for i in organisms:
            if i.get_location() == random_location:
                return OrganismGenerator.get_free_and_random_location(organisms, width, height)
        return random_location

    @staticmethod
    def get_initial_organisms(width, height):
        all_symbols = "WAFTSbguds"
        initial_organisms = []
        for l in all_symbols:
            # tutaj robie po jednym kazdego rodzaju
            initial_organisms.append(OrganismGenerator.get_organism(l))
        # tutaj sa losowe zwierzaki
        for i in range(int(0.2 * width * height) - len(all_symbols)):
            initial_organisms.append(OrganismGenerator.get_organism(random.choice(all_symbols)))

        initial_organisms.append(OrganismGenerator.get_organism('H'))
        # //dodanie czlowieka na koniec
        for i in initial_organisms:
            i.set_location(OrganismGenerator.get_free_and_random_location(initial_organisms, width, height))

        return sorted(initial_organisms, key=Organism.organism_sorting_key)

    @staticmethod
    def get_organism(symbol):
        organisms = {
            'W': lambda: Wolf(LocationHandler()),
            'S': lambda: Sheep(LocationHandler()),
            'F': lambda: Fox(LocationHandler()),
            'A': lambda: Antelope(LocationHandler()),
            'H': lambda: Human(LocationHandler()),
            'T': lambda: Turtle(LocationHandler()),
            'g': Grass,
            'd': Dandelion,
            'b': Belladonna,
            's': SosnowskysBorscht,
            'u': Guarana
        }
        return organisms[symbol]()
