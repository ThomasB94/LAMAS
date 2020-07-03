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

    def make_announcement(self, announcement_idx):
        return make_announcement_of_type(self, self.game, self.game.model, self.game.announcement_type, announcement_idx)

    # return the card that has been placed and on which stack it has been placed
    def make_move(self):
        stack_idx, card = self.determine_strategy()
        self.hand.remove(card)
        self.game.table[stack_idx][0].append(card)
        self.game.played_cards[card] = True
        return (card, stack_idx)

    # determines whether the agent can make a move
    # agent can only make a move if it has a card higher than up stack or lower than down stack
    def can_make_move(self):
        cards = self.get_closest_cards()
        if cards[0][1] == 99999 and cards[1][1] == 99999:
            return False
        else:
            return True

    # get a card from the remaining stack
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
        # get the best cards for the agents
        closest = self.get_closest_cards()
        closest_up = closest[0][0]
        closest_down = closest[1][0]
        # if agent has just one possible card, put the card on the correct stack
        if closest[0][1] == 99999:
            return 1, closest_down
        elif closest[1][1] == 99999:
            return 0, closest_up
        # otherwise look at the possible cards for the other player, based on the worlds in the Kripke model
        # based on the closest possible cards for the other player, we put the best card on the right stack
        else:
            ks = self.game.model
            all_worlds = ks.worlds
            possible_up = []
            possible_down = []
            # given our cards, look at possible cards
            prefix = str(closest_up) + '/' + str(closest_down)
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
            # if the other player has no possible cards for the up stack, we should put our card on the up stack
            # to make sure we don't put a card on the down stack that hinders the other player
            if possible_up == []:
                return 0, closest_up
            # if the other player has no possible cards for the down stack, we should put our card on the down stack
            # to make sure we don't put a card on the up stack that hinders the other player
            if possible_down == []:
                return 1, closest_down
            other_closest_up = min(possible_up)
            other_closest_down = max(possible_down)

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
