import numpy as np
from constants import *

class Agent():
    def __init__(self, id, hand, game):
        self.id = id
        self.hand = hand
        self.hand.sort()
        self.game = game

    def make_announcement(self):
        pass

    def make_move(self):
        # return the card that has been placed and on which stack it has been placed
        diffs = []
        for stack in self.game.table:
            print(stack)
            if stack[1] == UP:
                # difference between hand cards and stack card
                diff = np.array(self.hand) - stack[0][-1]
                diff[diff < 0] = 99999
                idx = diff.argmin()
                diff = diff[idx]
                diffs.append((diff, idx, UP))
            elif stack[1] == DOWN:
                diff = stack[0][-1] - np.array(self.hand)
                diff[diff < 0] = 99999
                idx = diff.argmin()
                diff = diff[idx]
                diffs.append((diff, idx, DOWN))
        stack_idx = np.array(diffs).argmin(axis=0)[0]
        (_, hand_idx, _) = min(diffs, key=lambda x:x[0])
        card = self.hand.pop(hand_idx)
        self.game.table[stack_idx][0].append(card)
        self.game.played_cards[card] = True
        return (card, stack_idx)


    def can_make_move(self):
        status = False
        for stack in self.game.table:
            if stack[1] == UP:
                diffs = np.array(self.hand) - stack[0][-1]
                if not all(x < 0 for x in diffs):
                    status = True
            elif stack[1] == DOWN:
                diffs = stack[0][-1] - np.array(self.hand)
                if not all(x < 0 for x in diffs):
                    status = True

        return status


    def take_card(self):
        if self.game.remaining:
            self.hand.append(self.game.remaining.pop())
