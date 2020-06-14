from agent import Agent
from constants import *
import random

class Game():
    def __init__(self, num_agents, top_card, announcements):
        self.num_agents = num_agents
        self.top_card = top_card
        # how many cards get dealt
        self.num_initial_cards = 5
        self.won = False
        self.announcements = announcements
        print("Setting up game with", num_agents, "agents and", top_card, "as the highest cards")
        print(announcements, "is the announcements setting")
        print("--------------------------------------------")
        self.setup_game()
        self.game_loop()

    def setup_game(self):
        # setup table
        # Even (inc. 0) table cards go up initially, odd go down
        #TODO: make this variable
        self.table = [([1],UP),([self.top_card],DOWN)]

        # remaining is the pile that cars are taken from after every turn
        self.remaining = possible_cards = list(range(2,self.top_card))

        # setup agents and generate hands
        random.shuffle(possible_cards)
        self.agents = []
        for agent_idx in range(self.num_agents):
            hand = []
            for _ in range(self.num_initial_cards):
                hand.append(self.remaining.pop())
            self.agents.append(Agent(agent_idx, hand, self))
            print("Agent", agent_idx + 1, "has cards", hand)
        print("Remaing cards are:", self.remaining)
        print("-------------------------")
        
    # A round is a round of announcements after which an agent decides which stack to put their card on
    def game_loop(self):
        agent_turn = 0
        round = 1
        while True:
            print("----------------------------------")
            print("Starting round", round)
            print("Every agent will make an announcement, after which")
            print("agent", agent_turn + 1, "will decide which table stack to put a card on")
            # this doesn't do anything yet
            for agent in self.agents:
                agent.make_announcement()
            agent = self.agents[agent_turn]
            
            if not agent.can_make_move():
                print("Agent", agent_turn + 1, "can't make a move, so the game is lost")
                print("HERE AGENT STACKS", self.agents[0].hand, self.agents[1].hand)
                break
            

            print("Agent had stack", self.agents[agent_turn].hand)
            card, stack_idx = agent.make_move()
            print("agent put", card, "on stack", stack_idx)

            agent.take_card()
        
            if self.game_won():
                print("Game is won, because all agents have 0 cards left")
                self.won = True
                break
            agent_turn = agent_turn + 1
            if agent_turn == self.num_agents:
                agent_turn = 0
            round = round + 1


    def game_won(self):
        status = True
        for agent in self.agents:
            if agent.hand:
                status = False
                break
        return status
            