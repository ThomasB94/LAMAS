from mlsolver.kripke import *
from mlsolver.formula import *
import numpy as np
import copy

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
            possibleNumbers.append(number)
    return possibleNumbers

def split_list(list):
    # Can change relative range
    half = len(list)//2
    return list[:half], list[half:]

def split_list_index(list, index):
    index = min(index, len(list))
    return list[:index], list[index:]

def getBestCards(agent, game):
    # Determine best card for UP stack
    stack = game.table[0]
    diff = np.array(agent.hand) - stack[0][-1]
    diff[diff < 0] = 99999
    idx = diff.argmin()
    s1Best = agent.hand[idx]

    # Determine best card for DOWN stack
    stack = game.table[1]
    diff = stack[0][-1] - np.array(agent.hand)
    diff[diff < 0] = 99999
    idx = diff.argmin()
    s2Best = agent.hand[idx]
    return s1Best, s2Best

def removeWorlds(ks, formula):
    ksCopy = KripkeStructure(ks.worlds.copy(), copy.deepcopy(ks.relations))
    notcompliant = ksCopy.nodes_not_follow_formula(formula)
    for world in notcompliant:
        ksCopy.remove_node_by_name(world)
    return ksCopy, len(notcompliant)

def make_range_announcement(agent, game, ks, announcement_type):
    # Find possible numbers and ad to set

    if not agent.hand:
        return ks

    # Look for the best cards that you have
    s1Best, s2Best = getBestCards(agent, game)

    # Set the prefix to look at the stacks for player 1
    prefix1 = "P" + str(agent.id + 1) + "S1"
    prefix2 = "P" + str(agent.id + 1) + "S2"

    posStack1 = makePossibilityList(ks, game.top_card, prefix1)
    posStack2 = makePossibilityList(ks, game.top_card, prefix2)
    posStack2.reverse()

    # Divide set into announcement values
    exclusionSetS1 = determine_exclusion_set(game, agent, posStack1, s1Best, announcement_type, 'UP')
    exclusionSetS2 = determine_exclusion_set(game, agent, posStack2, s2Best, announcement_type, 'DOWN')

    # To see if any worlds were actually removed
    announcement_flag = 0

    # Construct announcement
    if exclusionSetS1:
        announcement = Not(Atom(prefix1 + str(exclusionSetS1[0])))
        for index in range(1, len(exclusionSetS1)):
            announcement = And(announcement, Not(Atom(prefix1 + str(exclusionSetS1[index]))))
        ks, numRemoved = removeWorlds(ks, announcement)
        game.removed_worlds += numRemoved
        announcement_flag = 1

    # Construct announcement
    if exclusionSetS2:
        announcement = Not(Atom(prefix2 + str(exclusionSetS2[0])))
        for index in range(1, len(exclusionSetS2)):
            announcement = And(announcement, Not(Atom(prefix2 + str(exclusionSetS2[index]))))
        ks, numRemoved = removeWorlds(ks, announcement)
        game.removed_worlds += numRemoved
        announcement_flag = 1

    game.announcements_made += announcement_flag

    return ks

def determine_exclusion_set(game, agent, stack, best_for_stack, announcement_type, stack_type):
    if announcement_type == 'range':
        first_half, second_half = split_list(stack)
        print_rest = 'have a card in the best half of cards for stack'
    elif announcement_type == 'absolute':
        first_half, second_half = split_list_index(stack, 3)
        print_rest = 'have a card in the top 3 cards for stack'
    print_rest = print_rest + ' ' + stack_type
    print_name = 'YOU:' if agent.id == 0 else 'OPPONENT:'
    print('best for stack: ', best_for_stack)
    if best_for_stack in first_half:
        exclusion_set = second_half
        #print(print_name, 'I', print_rest)
        announcement_string = print_name + ' I ' + print_rest
        #print('Possible cards for UP stack after announcement: ' + str(first_half))
        game.gui.display_announcements(announcement_string, stack_type)
    elif best_for_stack in second_half:
        exclusion_set = first_half
        #print(print_name, 'I do NOT', print_rest)
        announcement_string = print_name + ' I do NOT ' + print_rest
        #print('Possible cards for UP stack after announcement: ' + str(second_half))
        game.gui.display_announcements(announcement_string, stack_type)
    else:
        game.gui.display_announcements('No announcement left', stack_type)
        exclusion_set = []
    return exclusion_set

def make_announcement_of_type(agent, game, ks, announcement_type):
    return make_range_announcement(agent, game, ks, announcement_type)
