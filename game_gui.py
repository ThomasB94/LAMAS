import pygame
import numpy as np

class GameGUI():
    def __init__(self, size, agents, num_of_initial_cards, screen):
        pygame.init()
        #successes, failures = pygame.init()
        #print("{0} successes and {1} failures".format(successes, failures))
        #self.screen = pygame.display.set_mode((720, 480))  # Notice the tuple! It's not 2 arguments.
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.bg = (114, 160, 193)
        self.size = size
        self.width, self.height = size
        
        self.font = pygame.font.SysFont('Arial', 50)

        # Size of play stacks
        self.image = pygame.Surface((self.width/10, self.height/4))  # The tuple represent size.
        self.image.fill(self.WHITE)

        # Stacks to play on
        self.pile1 = pygame.Rect((self.width/3, (self.height/2)-(self.height/8)), (self.width/2, self.height/2))
        self.pile2 = pygame.Rect(((2*self.width/3)-(self.width/9), (self.height/2)-(self.height/8)), (self.width/2, self.height/2))  # First tuple is position, second is size.

        self.show_cards(agents)
        # Rectangles for each player their cards
    
    def show_cards(self, agents):
        agent_idx = 1
        
        for agent in agents:
            spacing = len(agent.hand) + 1
            linspace = np.linspace(self.width/spacing, self.width - self.width/spacing, spacing)
            linspace = [int(lin) for lin in linspace]
            for idx, card in enumerate(agent.hand):
                if agent_idx == 1:
                    pile = pygame.Rect((linspace[idx], self.height/20), (self.width/2, self.height/2))
                elif agent_idx == 2:
                    pile = pygame.Rect((linspace[idx], 14*self.height/20), (self.width/2, self.height/2))
                new_rect = self.screen.blit(self.image,pile)
                new_rect[0] += (new_rect[2] / 3)
                new_rect[1] += (new_rect[3] / 3)
                self.screen.blit(self.font.render(str(card), 1, self.BLACK), new_rect)
                #text = self.font.render(str(card),  1, self.gui.BLACK)
                #print('done')
            agent_idx = 2
        


    