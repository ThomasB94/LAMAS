from mlsolver.kripke import World, KripkeStructure
from mlsolver.formula import *

# do some kripke stuff here

def createName(CardP1S1, CardP1S2, CardP2S1, CardP2S2):
    #create world name from 4 values
    return str(CardP1S1) + "/" + str(CardP1S2) + "/" + str(CardP2S1) + "/" + str(CardP2S2)

def createNameFromArray(worldValues):
    return createName(worldValues[0], worldValues[1], worldValues[2], worldValues[3])

def createWorld(CardP1S1, CardP1S2, CardP2S1, CardP2S2):
    #create a world object for ML mlsolver
    name = createName(CardP1S1, CardP1S2, CardP2S1, CardP2S2)
    truth_values = {}
    truth_values["P1S1" + str(CardP1S1)] =  True
    truth_values["P1S2" + str(CardP1S2)] =  True
    truth_values["P2S1" + str(CardP2S1)] =  True
    truth_values["P2S2" + str(CardP2S2)] =  True
    return World(name, truth_values)

def initialize_model(num_agents, played_cards, top_card, stacks):

    #Ml solver objects
    worlds = []
    #worlds identifiable by their numbers for building the relations
    worldsNumValues = []

    # All cards that fit on the first stack
    for cardP1S1 in range(stacks[0][0][-1] + 1, top_card):
        # Card wasn't seen before
        if not played_cards.get(cardP1S1, False):
            # All cards that fit on the  second stack
            for cardP1S2 in range(2, stacks[1][0][-1]):
                #cannot be played already, and cannot better for stack 1.
                if (not played_cards.get(cardP1S2, False)
                        and not (cardP1S2 > stacks[0][0][-1] and cardP1S2 < cardP1S1)
                ):
                    for cardP2S1 in range(stacks[0][0][-1] + 1, top_card):
                        if (not played_cards.get(cardP2S1, False)
                            and (cardP2S1 != cardP1S1)
                            and (cardP2S1 != cardP1S2)
                        ):

                            for cardP2S2 in range(2, stacks[1][0][-1]):
                                #cannot be played already, cannot better for stack 1 and no duplicates
                                if (not played_cards.get(cardP2S2, False)
                                    and not (cardP2S2 > stacks[0][0][-1] and cardP2S2 < cardP2S1)
                                    and (cardP2S2 != cardP1S1)
                                    and (cardP2S2 != cardP1S2)
                                ):
                                    #Create the worlds and add them to the numiric value list
                                    worlds.append(createWorld(cardP1S1, cardP1S2, cardP2S1, cardP2S2))
                                    worldsNumValues.append([cardP1S1, cardP1S2, cardP2S1, cardP2S2])

    #make relations
    P1relations = set()
    P2relations = set()

    #Use numeric value list for relations
    for world1 in worldsNumValues:
        for world2 in worldsNumValues:
            if (world1[0] == world2[0]
                and world1[1] == world2[1]
            ):
                P1relations.add((createNameFromArray(world1), createNameFromArray(world2)))
            if (world1[2] == world2[2]
                and world1[3] == world2[3]
            ):
                P2relations.add((createNameFromArray(world1), createNameFromArray(world2)))

    relations = {
        '1' : P1relations,
        '2' : P2relations
    }

    return KripkeStructure(worlds, relations)
