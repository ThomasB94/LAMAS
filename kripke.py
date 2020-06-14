from mlsolver.kripke import World, KripkeStructure

# do some kripke stuff here

def initialize_model(num_agents, hands, played_cards, top_card, stacks):

    worlds = []
    #For all players make a world for every stack and best card
    for cardP1, seen in played_cards.items():
        # card hasn't been played yet
        if not seen:
            #limits of what is posible

    # All cards that fit on the first stack
    for cardP1S1 in range(stacks[0][0][-1] + 1, top_card):
        # Card wasn't seen before
        if not played_cards[cardP1S1]:
            # All cards that fit on the  second stack
            for CardP1S2 in range(2, stacks[1][0][-1]):
                if not played_cards[cardP1S2]
                   and not (CardP1S2 > stacks[0][0][-1]
                   and Cardp1S2 < Cardp1S1)

    return model
