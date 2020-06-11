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
                diff = np.array(self.hand) - stack[0]
                idx = diff.argmin()
                diff = diff[idx]
                diffs.append((diff, idx, UP))
            elif stack[1] == DOWN:
                diff = stack[0] - np.array(self.hand)
                idx = diff.argmin()
                diff = diff[idx]
                diffs.append((diff, idx, DOWN))
        stack_idx = np.array(diffs).argmin(axis=0)[0]
        (card, hand_idx, stack_direction) = min(diffs, key=lambda x:x[0])
        self.game.table[stack_idx] = (self.hand.pop(hand_idx), stack_direction)
        return (card, stack_idx)
        
        
    def can_make_move(self):
        for stack in self.game.table:
            if stack[1] == UP:
                diffs = np.array(self.hand) - stack[0]
                if all(x < 0 for x in diffs):
                    return False
                else:
                    return True

            elif stack[1] == DOWN:
                diffs = stack[0] - np.array(self.hand)
                if all(x < 0 for x in diffs):
                    return False
                else:
                    return True

    def take_card(self):
        if self.game.remaining:
            self.hand.append(self.game.remaining.pop())


    
        





