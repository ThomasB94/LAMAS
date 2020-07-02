import numpy as np
from constants import *
from kripke import initialize_model
from announcements import makePossibilityList
from announcements import make_announcement_of_type
import random

class Agent():
    def __init__(self, id, hand, game):
        self.id = id
        self.hand = hand
        self.hand.sort()
        self.game = game

    def make_announcement(self):
        return make_announcement_of_type(self, self.game, self.game.model, self.game.announcement_type)

    # return the card that has been placed and on which stack it has been placed
    def make_move(self):
        stack_idx, card = self.determine_strategy()
        self.hand.remove(card)
        self.game.table[stack_idx][0].append(card)
        self.game.played_cards[card] = True
        return (card, stack_idx)

    def can_make_move(self):
        cards = self.get_closest_cards()
        if cards[0][1] == 99999 and cards[1][1] == 99999:
            return False
        else:
            return True

    def take_card(self):
        if self.game.remaining:
            self.hand.append(self.game.remaining.pop())

    # Returns the a list of the closest cards and how far they are from the stack cards
    def get_closest_cards(self):
        closest = []
        up_card = self.game.table[0][0][-1]
        down_card = self.game.table[1][0][-1]

        # Closest cards for the down stack
        diffs = np.array(self.hand) - up_card
        diffs[diffs < 0] = 99999
        idx = diffs.argmin()
        card = self.hand[idx]
        diff = min(diffs)
        closest.append((card, diff))

        # Closest cards for the up stack
        diffs = down_card - np.array(self.hand)
        diffs[diffs < 0] = 99999
        idx = diffs.argmin()
        card = self.hand[idx]
        diff = min(diffs)
        closest.append((card, diff))

        return closest

    # Determines which stack a card should be put on and the card that should be put on the table
    def determine_strategy(self):
        closest = self.get_closest_cards()
        closest_up = closest[0][0]
        closest_down = closest[1][0]
        if closest[0][1] == 99999:
            return 1, closest_down
        elif closest[1][1] == 99999:
            return 0, closest_up
        else:
            ks = self.game.model
            all_worlds = ks.worlds
            possible_up = []
            possible_down = []
            prefix = str(closest_up) + '/' + str(closest_down)
            #TODO: fix this id of agent determines which world to check
            if self.id == 0:
                for world in all_worlds:
                    if prefix == world.name[0:3]:
                        possible_up.append(int(world.name[4]))
                        possible_down.append(int(world.name[6]))

            elif self.id == 1:
                for world in all_worlds:
                    if prefix == world.name[4:]:
                        possible_up.append(int(world.name[0]))
                        possible_down.append(int(world.name[2]))

            possible_up = list(set(possible_up))
            possible_down = list(set(possible_down))
            if possible_up == []:
                return 0, closest_up
            if possible_down == []:
                return 1, closest_down
            other_closest_up = min(possible_up)
            other_closest_down = max(possible_down)

            if closest_up < self.game.table[0][0][-1]:
                print(other_closest_up)

            if closest_up < other_closest_up:
                # here we have better cards for both stacks, so we make a random choice
                if closest_down > closest_down:
                    r = random.randint(0,1)
                    if r == 0:
                        return 0, closest_up
                    else:
                        return 1, closest_down
                else:
                    # we have better cards for the up stack
                    return 0, closest_up
            elif closest_down > other_closest_down:
                # we have better cards for the down stack
                return 1, closest_down
            else:
                # we have the worst cards for both stacks, again we make a random choice
                r = random.randint(0,1)
                if r == 0:
                    return 0, closest_up
                else:
                    return 1, closest_down
