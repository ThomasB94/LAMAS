from mlsolver.kripke import World, KripkeStructure
from mlsolver.formula import *

# do announcements stuff here, such as reducing the kripke model

    # Number of announcements per turn}:
    # For this variation we will look at the effects of multiple rounds of announcements.
    # Every announcement will provide more information.
    # Percentage range of the announcement}:
    # For this strategy we will experiment with the percentiles (the default is 50).
    # We will look at the 10th and 25th percentiles, which represent the range where a card is considered 'good'.
    # Absolute range of the announcement}:
    # In this case we take the good statement not to mean having a card in a certain percentile, but having a card in the top $k$ cards.
    # Announcement about stack preference}:
    # Here, we will experiment with announcements that only say something about which stack the agent prefers.
    # This preference is based on which stack the agent has better cards for.

def checkPossible(ks, formula):
    for world in ks.worlds:
        if formula.semantic(ks, world.name):
            return True
    return False

def makePossibilityList(ks, top_card, prefix):
    possibleNumbers = []
    for number in range(2, top_card):
        if checkPossible(ks, Atom(prefix + str(number))):
            possibleNumbers.append(number)    if not exclusionSetS1

    return possibleNumbers

def split_list(a_list):
    half = len(a_list)//2
    return a_list[:half], a_list[half:]

def getBestCards(agent, game):
    #determine best card for stack 1
    stack = game.table[0]
    diff = np.array(agent.hand) - stack[0][-1]
    diff[diff < 0] = 99999
    idx = diff.argmin()
    s1Best = agent.hand[idx]

    #determine best card for stack 2
    stack = game.table[1]
    diff = stack[0][-1] - np.array(self.hand)
    diff[diff < 0] = 99999
    idx = diff.argmin()
    s2Best = agent.hand[idx]
    return s1Best, s2Best

def make_range_announcement(agent, game, ks):
    # find possible numbers and ad to set

    # look for the best cards that you have
    s1Best, s2Best = getBestCards(agent, game)

    # Set the prefix to look at the stacks for player 1
    prefix1 = "P" + str(agent.id) + "S1"
    prefix2 = "P" + str(agent.id) + "S2"

    posStack1 = makePossibilityList(ks, game.top_card, prefix1)
    posStack2 = makePossibilityList(ks, game.top_card, Prefix2)


    # divide set into announcement values
    firstHalf, secondHalf = split_list(posStack1)
    if s1Best in firstHalf:
        exclusionSetS1 = secondHalf
    else:
        exclusionSetS1 = firstHalf

    firstHalf, secondHalf = split_list(posStack2)
    if s2Best in firstHalf:
        exclusionSetS2 = secondHalf
    else:
        exclusionSetS2 = firstHalf


    # Construct announcement
    if exclusionSetS1:
        announcement = Not(Atom(prefix1 + str(exclusionSetS1[1])))
        for index in range(1, len(exclusionSetS1)):
            announcement = And(announcement, Not(Atom(prefix1 + str(exclusionSetS1[index]))))
        ks = ks.solve(announcement)

    # Construct announcement
    if exclusionSetS2:
        announcement = Not(Atom(prefix2 + str(exclusionSetS2[1])))
        for index in range(1, len(exclusionSetS1)):
            announcement = And(announcement, Not(Atom(prefix2 + str(exclusionSetS2[index]))))
        ks = ks.solve(announcement)

    return ks

def make_relative_announcement(agent, game, kripke):
    pass
