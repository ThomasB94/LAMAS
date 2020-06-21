import pygame
import numpy as np

class GameGUI():
    def __init__(self, agents, num_of_initial_cards):
        pygame.init()
        #successes, failures = pygame.init()
        #print("{0} successes and {1} failures".format(successes, failures))
        #self.screen = pygame.display.set_mode((720, 480))  # Notice the tuple! It's not 2 arguments.

        infoObject = pygame.display.Info()
        pygame.display.set_caption('LAMAS - The Game')
        #self.size = self.width, self.height = int(infoObject.current_w/2), int(infoObject.current_h/2)
        self.size = self.width, self.height = 960, 540
        self.screen = pygame.display.set_mode(self.size)

        self.agents = agents
        self.clock = pygame.time.Clock()
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (110, 42, 81)
        self.RED_SHADE = (38, 14, 28)
        self.bg = (42, 81, 110)
        self.pile_colour = (110, 71, 42)
        
        self.font = pygame.font.SysFont('Arial', 50)

        # Player cards
        self.image = pygame.Surface((self.width/10, self.height/4))  # The tuple represent size.
        self.image.fill(self.WHITE)

        self.border_pile = pygame.Surface(((self.width/10)+4, (self.height/4)+4))
        self.border_pile.fill(self.BLACK)

        # Piles to put cards on
        self.image_pile = pygame.Surface((self.width/8, self.height/3.8))  # The tuple represent size.
        self.image_pile.fill(self.RED)

        self.image_pile_border = pygame.Surface(((self.width/8)+2, (self.height/3.8)+2))  # The tuple represent size.
        self.image_pile_border.fill(self.RED_SHADE)

        # Stacks to play on
        self.pile1 = pygame.Rect((self.width/3, (self.height/2)-(self.height/8)), (self.width/2, self.height/2))
        self.pile2 = pygame.Rect(((2*self.width/3)-(self.width/5.3), (self.height/2)-(self.height/8)), (self.width/2, self.height/2))  # First tuple is position, second is size.

        self.show_cards()
    
    def show_cards(self):
        agent_idx = 1
        for agent in self.agents:
            agent.hand.sort()
            spacing = len(agent.hand) + 1
            linspace = np.linspace(self.width/spacing, self.width - self.width/spacing, spacing)
            linspace = [int(lin) for lin in linspace]
            for idx, card in enumerate(agent.hand):
                if agent_idx == 1:
                    pile = pygame.Rect((linspace[idx], 14*self.height/20), (self.width/2, self.height/2))
                elif agent_idx == 2:
                    pile = pygame.Rect((linspace[idx], self.height/20), (self.width/2, self.height/2))
                self.render_card(str(card), self.image, pile, self.border_pile, agent_idx)
            agent_idx = 2

    def update_screen(self, table, remaining_cards):
        self.screen.fill(self.bg)
        pile1_card = str(table[0][0][-1])
        pile2_card = str(table[1][0][-1])
        # Playing piles will be bold
        self.font.set_bold(True)
        # Render stuff
        self.render_card(pile1_card, self.image_pile, self.pile1, self.image_pile_border, 1, 'UP')
        self.render_card(pile2_card, self.image_pile, self.pile2, self.image_pile_border, 1, 'DOWN')
        # Deactive bold text
        self.font.set_bold(False)
        # Render the player cards
        self.show_cards()
        text = pygame.font.SysFont('Arial', 16)
        text.set_italic(True)
        text1 = text.render('Press space to step through the game', True, self.BLACK)
        text.set_italic(False)
        self.screen.blit(text1, (15,15))
        text2 = text.render('The remaining cards are: ' + str(remaining_cards + self.agents[1].hand), True, self.BLACK)
        self.screen.blit(text2, (15,100))
        pygame.display.update()
        
    def render_card(self, card_value, source, destination, shade_source, agent_idx, pile_text=None):
        self.screen.blit(shade_source, destination)
        render_rect = self.screen.blit(source, destination)
        text_w, text_h = self.font.size(card_value)
        render_rect[0] += (render_rect[2] / 2) - (text_w/2)
        render_rect[1] += (render_rect[3] / 2) - text_h
        if agent_idx == 1:
            self.screen.blit(self.font.render(card_value, True, self.BLACK), render_rect)
        if pile_text is not None:
            #render_rect = self.screen.blit(source, destination)
            render_rect[0] -= (render_rect[2] / 2) - (text_w/2)
            render_rect[1] -= (render_rect[3] / 2) - text_h
            text_font = pygame.font.SysFont('Arial', 30)
            text_w, text_h = text_font.size(pile_text)
            render_rect[0] += (render_rect[2] / 2) - (text_w/2)
            render_rect[1] += 2*text_h
            text_font.set_underline(True)
            self.screen.blit(text_font.render(pile_text, True, self.BLACK), render_rect)
            text_font.set_underline(False)
    
    def display_game_ending(self, end_text):
        self.screen.fill(self.bg)
        end_img = pygame.Surface((self.width/2, self.height/4))  # The tuple represent size.
        end_img.fill(self.bg)
        text_pos = pygame.Rect((self.width/8, (self.height/2)-(self.height/8)), (self.width/2, self.height/2))
        render_rect = self.screen.blit(end_img, text_pos)
        text_font = pygame.font.SysFont('Arial', 50)
        #text_w, text_h = text_font.size(text)
        text_font.set_underline(True)
        self.screen.blit(text_font.render(end_text, True, self.BLACK), render_rect)
        pygame.display.update()        