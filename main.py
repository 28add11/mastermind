import pygame
import mastermind
from random import randint

screen = pygame.display.set_mode((640, 480))
running = True
mbd = False
clock = pygame.time.Clock()
row = 0
combo = [randint(0, 7), randint(0, 7), randint(0, 7), randint(0, 7)]
gamefont = pygame.font.Font(None, 40)



mastermind.mainmaster(screen, clock, 12, combo, gamefont,)

pygame.quit