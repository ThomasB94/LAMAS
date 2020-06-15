import pygame

class GameGUI():
    def __init__(self, size):
        pygame.init()
        #successes, failures = pygame.init()
        #print("{0} successes and {1} failures".format(successes, failures))
        #self.screen = pygame.display.set_mode((720, 480))  # Notice the tuple! It's not 2 arguments.
        self.clock = pygame.time.Clock()
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.size = size
        self.width, self.height = size

        self.font = pygame.font.SysFont('Arial', 18)
        print(self.font)

        self.pile1 = pygame.Rect((self.width/3, self.height/3), (self.width/2, self.height/2))
        self.pile2 = pygame.Rect(((2*self.width/3)-(self.width/9), self.height/3), (self.width/2, self.height/2))  # First tuple is position, second is size.
        self.image = pygame.Surface((self.width/9, self.height/4))  # The tuple represent size.
        self.image.fill(self.WHITE)


    