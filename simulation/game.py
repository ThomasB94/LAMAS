from agent import Agent
from constants import *
from game_gui import GameGUI
from kripke import initialize_model
import random
import pygame
import time

class Game():
    def __init__(self, num_agents, top_card, announcements, num_announcements):
        self.num_agents = num_agents
        self.top_card = top_card
        self.empty_list = []
        #records which cards have been played
        self.played_cards = {}
        self.model = None
        self.removed_worlds = 0
        self.announcements_made = 0
        # how many cards get dealt
        self.num_initial_cards = 2
        self.won = False
        self.lost = False
        self.announcement_type = announcements
        self.num_announcements = num_announcements
        print("Setting up game with", num_agents, "agents and", top_card, "as the highest card.")
        print(announcements, "is the announcements setting")
        print("--------------------------------------------")
        self.setup_game()
        self.gui = GameGUI(self.agents, self.num_initial_cards)
        self.empty_list.extend(self.remaining)
        self.empty_list.extend(self.agents[1].hand)
        self.empty_list.sort()
        self.gui.update_screen(self.table, self.empty_list, 0)
        print("Remaing cards are:", self.empty_list)
        self.game_loop()
        
    def setup_game(self):
        # setup table
        # Even (inc. 0) table cards go up initially, odd go down
        #TODO: make this variable
        self.table = [([1],UP),([self.top_card],DOWN)]

        #record that none of the cars have been played yet
        for card in range(2,self.top_card):
            self.played_cards[card] = False

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
        print('The cards have been shuffled. You and your opponent both receive 2 cards.')
        
        
    # A round is a round of announcements after which an agent decides which stack to put their card on
    def game_loop(self):
        agent_turn = 0
        round = 1
        print("++++++++++++++++++++++++++++++++++++++++++++")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print('exited game')
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print("Starting round", round)
                        # Remove the 'press space to step through the game'
                        self.gui.first_show = False
                        self.model = initialize_model(self.num_agents, self.played_cards, self.top_card, self.table)
                        for agent in self.agents:
                            if agent != self.agents[agent_turn]:
                                for idx in range(self.num_announcements):
                                    self.model = agent.make_announcement(idx)
                        agent = self.agents[agent_turn]
                        
                        # Print name to notify which player is going to make a move this round
                        print_name = 'You' if agent_turn == 0 else 'Your opponent'
                        if not agent.can_make_move():
                            print(print_name, "can't make a move, so the game is lost")
                            print(print_name, "had the following cards left:", self.agents[agent_turn].hand)
                            self.lost = True
                            break
                        
                        # The current player plays a card
                        card, stack_idx = agent.make_move()

                        # Print statement to notify which card was put on which stack
                        print_stack = 'UP' if stack_idx == 0 else 'DOWN'
                        card_played_string = print_name + ' put ' + str(card) + ' on the ' + str(print_stack) + ' stack'
                        self.gui.display_card_played(card_played_string, agent_turn)

                        # The player who has played the card should draw a new one, if possible
                        agent.take_card()
                    
                        # Determine whether the game has been won
                        if self.game_won():
                            print("Game is won, because all agents have 0 cards left")
                            self.won = True
                            break

                        # Pass the turn to the other player
                        agent_turn = agent_turn + 1
                        if agent_turn == self.num_agents:
                            agent_turn = 0
                        
                        # Gather all cards that are still possible for 'you' player
                        self.empty_list = []
                        self.empty_list.extend(self.remaining)
                        self.empty_list.extend(self.agents[1].hand)
                        self.empty_list.sort()
                        round = round + 1
                        print("++++++++++++++++++++++++++++++++++++++++++++")
            
            # Update all things that have to be rendered
            self.gui.update_screen(self.table, self.empty_list, agent_turn)

            # The game is finished
            if self.won or self.lost:
                print('Number of removed worlds: {}'.format(self.removed_worlds))
                self.end_game(self.won, self.lost)

    # Check whether all agents have zero cards                                      
    def game_won(self):
        status = True
        for agent in self.agents:
            if agent.hand:
                status = False
                break
        return status
    
    # Prepare what text should be displayed based on the outcome of the game
    def end_game(self, won=False, lost=False):
        if won:
            end_text = 'The game has been won! Congratulations!'
        if lost:
            end_text = 'The game is lost. Maybe next time...'
        self.gui.display_game_ending(end_text)
        time.sleep(1)
        while True: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print('exited game')
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        quit()
            
