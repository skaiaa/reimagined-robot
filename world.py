from virtual_world.organism_generator import OrganismGenerator
import copy
from virtual_world.organism import Organism
from virtual_world.human import Human
from virtual_world.logger import logger


class World:
    organisms = []

    # private Logger logger;
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._fields = width * height
        self.organisms = OrganismGenerator.get_initial_organisms(width, height)

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def who_is_there(self, location):
        self.handle_worlds_edges(location)
        for o in self.organisms:
            if o.get_location() == location:
                return o
        return None

    def handle_worlds_edges(self, location):
        if location.x < 0:
            location.x = self._height + location.x
        if location.x >= self._height:
            location.x = location.x - self._height
        if location.y < 0:
            location.y = self._width + location.y
        if location.y >= self._width:
            location.y = location.y - self._width

    def play_round(self):
        tmp_organisms = copy.copy(self.organisms)
        # //jak w trakcie tury dodam cos do organizmow to nie moge iterowac po czyms do czego dodaje
        while tmp_organisms:
            # if ((tmpOrganisms.elementAt(0)).getSymbol() == 'H') logger.log("Your turn!");
            if self.execute_actions_and_check_end_of_game(tmp_organisms[0],
                                                          tmp_organisms[0].action(self.organisms),
                                                          tmp_organisms):
                return
        self.organisms = sorted(self.organisms, key=Organism.organism_sorting_key)

    def execute_actions_and_check_end_of_game(self, organism, action, tmp_organisms):
        killed_oneself = False
        if action.is_moving():
            location = action.get_move()
            organism_already_there = self.who_is_there(location)
            if not organism_already_there:
                # //logger.log(organism.getName() + " moving to " + location.y + " " + location.x);
                organism.set_location(location)
            else:  # //kolizje
                killed_oneself = self.execute_collisions_and_check_if_killed_oneself(organism,
                                                                                     organism.collision(
                                                                                        organism_already_there,
                                                                                        location),
                                                                                     organism_already_there,
                                                                                     tmp_organisms)
        if action.is_spreading():
            spread = action.get_spread()
            for location in spread:
                organism_already_there = self.who_is_there(location)
                # //logger.log(organism->getName() + " trying to spread to " + to_string(location.y) + " " + to_string(location.x));
                if not organism_already_there and len(self.organisms) < self._fields:
                    new_organism = OrganismGenerator.get_organism(organism.get_symbol())
                    new_organism.set_location(location)
                    # //logger.log(organism.getName() + " is spreading to " + location.y + " " + location.x);
                    self.organisms.append(new_organism)

            if action.kills():
                self.perform_killing_spree(action.kills(), organism, None, tmp_organisms)
            # //performKillingSpree(collision.kills(), organism, organismAlreadyThere, tmpOrganisms);

        if action.is_activating_special_ability():
            pass
            logger.log(organism.get_name() + " just activated " + action.get_ability())

        if tmp_organisms:
            tmp_organisms.pop(0)
        if not killed_oneself:
            organism.grow_older()
        return False

    def save_to_file(self, file_name):
        with open(file_name, "w") as text_file:
            text_file.write(str(self._width) + " " + str(self._height) + "\n")
            for o in self.organisms:
                info = o.info_for_save()
                text_file.write(str(o.get_symbol()) + " " + info)

    def load_from_file(self, file_name):
        self.kill_all_organisms()
        try:
            with open(file_name, "r") as text_file:
                dimensions = text_file.readline().split()
                self._width = int(dimensions[0])
                self._height = int(dimensions[1])
                for line in text_file:
                    stats = line.split()
                    o = OrganismGenerator.get_organism(stats[0])
                    o.retrieve_stats_from_file(stats[1:])
                    self.organisms.append(o)
        except Exception:
            logger.log("Cannot read organisms!")

    def execute_collisions_and_check_if_killed_oneself(self, organism, collision, organism_already_there,
                                                       tmp_organisms):
        killed_oneself = False
        if collision.is_reproducing():
            location = collision.get_reproduce()
            # //logger.log(organism.getName() + " trying to reproduce on " + location.y + " " + location.x);
            organism_on_place = self.who_is_there(location)
            if not organism_on_place and len(self.organisms) < self._fields:
                logger.log("Successfully reproduced!")
                child = OrganismGenerator.get_organism(organism.get_symbol())
                child.set_location(location)
                self.organisms.append(child)

        if collision.is_fighting():
            # //logger.log(organism.getName() + " is trying to eat " + organismAlreadyThere.getName());
            killed_oneself = self.perform_killing_spree(collision.kills(), organism, organism_already_there, tmp_organisms)
            if not killed_oneself:
                organism.set_location(collision.get_fight())

        if collision.is_trying_to_catch_it():
            logger.log(organism.get_name() + " is trying to catch " + organism_already_there.get_name())
            l = collision.get_catch()
            # //logger.log(organismAlreadyThere.getName() + " is trying to run away to " + l.y + " " + l.x);
            organism_on_place = self.who_is_there(l)
            if not organism_on_place:
                # logger.log(organismAlreadyThere.getName() + " succesfully run away!");
                organism.set_location(organism_already_there.get_location())
                organism_already_there.set_location(collision.get_catch())
            else:
                # logger.log(organismAlreadyThere.getName() + " didn't manage to run away!");
                possible_location = organism_already_there.get_location()
                killed_oneself = self.perform_killing_spree(collision.kills(), organism, organism_already_there, tmp_organisms)
                if not killed_oneself:
                    organism.set_location(possible_location)

        return killed_oneself

    def perform_killing_spree(self, killed, killer, organism_already_there, tmp_organisms):
        killed_oneself = False
        for victim in killed:
            name_of_victim = victim.get_name()
            name_of_killer = killer.get_name()
            if not victim.is_immune_to_killing_by(killer):
                if victim.get_location() == killer.get_location():
                    killed_oneself = True
                    if organism_already_there:
                        name_of_killer = organism_already_there.get_name()
                if victim.is_increasing_strength():
                    killer.set_strength(killer.get_strength() + victim.get_increase())
                    logger.log(
                        name_of_victim + " increased strength of " + name_of_killer + " by " + str(victim.get_increase()))
                position_in_round = self.get_position_in_vector(victim, tmp_organisms)
                position_in_world = self.get_position_in_vector(victim, self.organisms)
                if position_in_round > -1:
                    del tmp_organisms[position_in_round]
                    #tmp_organisms.remove(position_in_round)
                del self.organisms[position_in_world]
                #self.organisms.remove(position_in_world)
            logger.log(name_of_victim + " was killed by " + name_of_killer)
        return killed_oneself

    def get_position_in_vector(self, victim, organisms):
        position = 0
        for o in organisms:
            if o.get_location() == victim.get_location():
                return position
            position += 1
        return -1
        # //nie ma go w tym vectorze

    def kill_all_organisms(self):
        self.organisms.clear()

    def get_human(self):
        for o in self.organisms:
            if isinstance(o, Human):
                return o
        return None

    def create_new_world(self):
        self.kill_all_organisms()
        self.organisms = OrganismGenerator.get_initial_organisms(self._width, self._height)
