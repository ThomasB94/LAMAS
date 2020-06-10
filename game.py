from agent import Agent
import random

class Game():
    def __init__(self, num_agents, top_card, announcements):
        self.num_agents = num_agents
        self.top_card = top_card
        # how many cards get dealt
        self.num_initial_cards = 5
        self.announcements = announcements
        print("Setting up game with", num_agents, "agents and", top_card, "as the highest cards")
        print(announcements, "is the announcements setting")
        print("--------------------------------------------")
        self.setup_game()

    def setup_game(self):
        # setup table
        # Even (inc. 0) table cards go up initially, odd go down
        self.table = [1,self.top_card]

        # remaining is the pile that cars are taken from after every turn
        self.remaining = possible_cards = list(range(2,self.top_card))

        # setup agents and generate hands
        random.shuffle(possible_cards)
        self.agents = []
        for agent_idx in range(self.num_agents):
            hand = []
            for _ in range(self.num_initial_cards):
                hand.append(self.remaining.pop())
            self.agents.append(Agent(agent_idx, hand))
            print("Agent", agent_idx + 1, "has cards", hand)
        print("Remaing cards are:", self.remaining)
        print("-------------------------")
        
    def game_loop(self):
        round = 1
        while True:
            print("Starting round 1")
            for 
            

