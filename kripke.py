from mlsolver.kripke import World, KripkeStructure

# do some kripke stuff here

def createName(CardP1S2, CardP1S2, CardP2S1, CardP2S2):
    #create world name from 4 values
    return str(CardP1S1) + "/" + str(CardP1S2) + "/" + str(CardP2S2) + "/" + str(CardP2S2)

def createNameFromArray(worldValues):
    return createName(worldValues[0], worldValues[1], worldValues[2], worldValues[3])

def createWorld(CardP1S2, CardP1S2, CardP2S1, CardP2S2):
    #create a world object for ML mlsolver
    name = createName(CardP1S2, CardP1S2, CardP2S1, CardP2S2)
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
        if not played_cards[cardP1S1]:
            # All cards that fit on the  second stack
            for CardP1S2 in range(2, stacks[1][0][-1]):
                #cannot be played already, and cannot better for stack 1.
                if (not played_cards[CardP1S2]
                        and not (CardP1S2 > stacks[0][0][-1] and Cardp1S2 < Cardp1S1)
                ):
                    for CardP2S1 in range(stacks[0][0][-1] + 1, top_card):
                        if (not played_cards[cardP1S1]
                            and (Cardp2S1 != Cardp1S1)
                            and (Cardp2S1 != Cardp1S2)
                        ):

                            for CardP2S2 in range(2, stacks[1][0][-1]):
                                #cannot be played already, cannot better for stack 1 and no duplicates
                                if (not played_cards[CardP1S2]
                                    and not (CardP1S2 > stacks[0][0][-1] and Cardp1S2 < Cardp1S1)
                                    and (Cardp2S2 != Cardp1S1)
                                    and (Cardp2S2 != Cardp1S2)
                                ):
                                    worlds.append(CreateWorld(CardP1S2, CardP1S2, CardP2S1, CardP2S2))
                                    worldsNumValues.append([CardP1S2, CardP1S2, CardP2S1, CardP2S2])

    #make relations
    P1relations = set()
    P2relations = set()

    for world1 in worldsNumValues:
        for world2 in worldsNumValues:
            if (world1[0] == world2[0]
                and world1[1] == world2[1]
            ):
                P1relations.add((createNameFromArray(world1), createNameFromArray(world2)))
            if (world1[3] == world2[3]
                and world1[4] == world2[4]
            ):
                P2relations.add((createNameFromArray(world1), createNameFromArray(world2)))

    relations = {
        '1' : P1relations
        '2' : P2relations
    }

    return KripkeStructure(worlds, relations)
