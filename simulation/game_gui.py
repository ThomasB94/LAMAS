import pygame
import numpy as np

class GameGUI():
    def __init__(self, agents, num_of_initial_cards):
        self.agents = agents
        pygame.init()

        # Get user screen information
        infoObject = pygame.display.Info()
        pygame.display.set_caption('LAMAS - The Game')

        # Ratio scaling
        screen_width, screen_height = int(infoObject.current_w/2), int(infoObject.current_h/2)
        self.width_scale = screen_width/960
        self.height_scale = screen_height/540
        self.width = 960 / self.width_scale
        self.height = 540 / self.height_scale
        self.size = int(self.width), int(self.height)
        self.screen = pygame.display.set_mode(self.size)

        # Flag to show stuff only once
        self.first_show = True
        
        # Colour constants
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (110, 42, 81)
        self.RED_SHADE = (38, 14, 28)
        self.YELLOW = (247, 187, 46)
        self.bg = (42, 81, 110)
        self.pile_colour = (110, 71, 42)
        
        # Font constant
        self.font = pygame.font.SysFont('Arial', 50)

        # Player cards
        self.image = pygame.Surface((self.width/10, self.height/4))  
        self.image.fill(self.WHITE)

        self.border_pile = pygame.Surface(((self.width/10)+4, (self.height/4)+4))
        self.border_pile.fill(self.BLACK)

        # Piles to put cards on
        self.image_pile = pygame.Surface((self.width/8, self.height/3.8)) 
        self.image_pile.fill(self.RED)

        self.image_pile_border = pygame.Surface(((self.width/8)+2, (self.height/3.8)+2))  
        self.image_pile_border.fill(self.RED_SHADE)

        # Stacks to play on
        self.pile1 = pygame.Rect((self.width/3, (self.height/2)-(self.height/8)), (self.width/2, self.height/2))
        self.pile2 = pygame.Rect(((2*self.width/3)-(self.width/5.3), (self.height/2)-(self.height/8)), (self.width/2, self.height/2))  # First tuple is position, second is size.

        self.show_cards()
    
    # Display the players' cards
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

    def update_screen(self, table, remaining_cards, agent_turn):
        self.screen.fill(self.bg)

        # Render the stacks to play on
        self.font.set_bold(True)
        pile1_card = str(table[0][0][-1])
        pile2_card = str(table[1][0][-1])
        self.render_card(pile1_card, self.image_pile, self.pile1, self.image_pile_border, 1, 'UP')
        self.render_card(pile2_card, self.image_pile, self.pile2, self.image_pile_border, 1, 'DOWN')
        self.font.set_bold(False)

        # Render the player cards
        self.show_cards()

        # Render all textual components
        self.display_text(remaining_cards, agent_turn)
        pygame.display.update()
        
    def render_card(self, card_value, source, destination, shade_source, agent_idx, pile_text=None):
        self.screen.blit(shade_source, destination)
        render_rect = self.screen.blit(source, destination)
        
        # Account for the size of the text
        text_w, text_h = self.font.size(card_value)
        render_rect[0] += (render_rect[2] / 2) - (text_w/2)
        render_rect[1] += (render_rect[3] / 2) - text_h

        # Do not show your opponent's cards
        if agent_idx == 1:
            self.screen.blit(self.font.render(card_value, True, self.BLACK), render_rect)
        
        # Render 'UP' and 'DOWN' 
        if pile_text is not None:
            render_rect[0] -= (render_rect[2] / 2) - (text_w/2)
            render_rect[1] -= (render_rect[3] / 2) - text_h
            text_font = pygame.font.SysFont('Arial', 30)

            # Account for the size of the text
            text_w, text_h = text_font.size(pile_text)
            render_rect[0] += (render_rect[2] / 2) - (text_w/2)
            render_rect[1] += (render_rect[3] / 2) + (text_h/2)
            text_font.set_underline(True)
            self.screen.blit(text_font.render(pile_text, True, self.BLACK), render_rect)
            text_font.set_underline(False)
    
    # Displays whether the game has been won or lost
    def display_game_ending(self, end_text):
        self.screen.fill(self.bg)
        end_img = pygame.Surface((self.width/2, self.height/4)) 
        end_img.fill(self.bg)
        text_pos = pygame.Rect((self.width/2, (self.height/2)-(self.height/8)), (self.width/2, self.height/2))
        render_rect = self.screen.blit(end_img, text_pos)
        text_font = pygame.font.SysFont('Arial', 50)

        # Account for the size of the text
        text_w, text_h = text_font.size(end_text)
        render_rect[0] -= (text_w/2)
        render_rect[1] -= (text_h / 2)
        text_font.set_underline(True)
        self.screen.blit(text_font.render(end_text, True, self.BLACK), render_rect)
        pygame.display.update()

    def display_text(self, remaining_cards, agent_turn):
        text = pygame.font.SysFont('Arial', 18)
        
        # Display general step tooltip
        if self.first_show:
            text.set_italic(True)
            text1 = text.render('Press space to step through the game', True, self.WHITE)
            text.set_italic(False)
            self.screen.blit(text1, (self.width/40, self.height/10))

        # Display what the remaining cards are
        text2 = text.render('The remaining cards are: ' + str(remaining_cards), True, self.WHITE)
        self.screen.blit(text2, (self.width/40, self.height/20))

        # Text to display where the announcements for UP stack will be located
        text.set_underline(True)
        announce_stack1 = text.render('Announcements for UP stack', True, self.BLACK)
        self.screen.blit(announce_stack1, (self.width/14, self.height/3))

        # Text to display where the announcements for DOWN stack will be located
        announce_stack2 = text.render('Announcements for DOWN stack', True, self.BLACK)
        self.screen.blit(announce_stack2, (self.width/1.45, self.height/3))
        text.set_underline(False)

        # Display who's turn it is
        text_turn = pygame.font.SysFont('Arial', 20)
        print_name = 'your' if agent_turn == 0 else 'your opponent\'s'
        print_text = 'It is now ' + print_name + ' turn'
        text3 = text_turn.render(print_text, True, self.YELLOW)
        y = self.height/1.4 if agent_turn == 0 else self.height/4
        self.screen.blit(text3, (self.width/40, y))

    def display_announcements(self, text, stack_type, announcement_idx=1):
        font = pygame.font.SysFont('Arial', 18)
        pygame.display.update()
        height_idx = (self.height/40)*(announcement_idx-1)
        # Loop to keep displaying the announcements
        while True:
            display_text = font.render(text, True, self.WHITE)
            x = self.width/40 if stack_type == 'UP' else self.width/1.55
            self.screen.blit(display_text, (x, (self.height/2.5)+height_idx))
            pygame.display.update()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        print('exited game')
                        quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            return

    # Displays what card has been played by which player
    def display_card_played(self, text, agent_turn):
        font = pygame.font.SysFont('Arial', 30)
        y = self.height/3.03 if agent_turn == 1 else self.height/1.52
        while True:
            display_text = font.render(text, True, self.YELLOW)
            text_w, text_h = font.size(text)
            self.screen.blit(display_text, ((self.width/2.15)-(text_w/2), y))
            pygame.display.update()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        print('exited game')
                        quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            return