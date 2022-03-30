import pygame
import mastermind
from buttonhandle import button
from random import randint

gamefont = pygame.font.Font(None, 40)

screen = pygame.display.set_mode((640, 480))
running = True
clock = pygame.time.Clock()
mbu = False

startbutton = button((80, 210, 80, 60), (0, 80, 0), "Start!", 0, (85, 225))
quitbutton = button((480, 210, 80, 60), (80, 0, 0), "Quit", 0, (490, 225))

#-----stuff-----#

while running:

    #-----mainloop-----#

    clock.tick(60)


    mouse = pygame.mouse.get_pos()

    for i in pygame.event.get():            
        match i.type:
            case pygame.QUIT:
                running = False
            case pygame.MOUSEBUTTONUP:
                    mbu = True

    screen.fill((193, 193, 193))
    
    titletext = gamefont.render("Mastermind", True, (10, 10, 10))
    titletextpos = titletext.get_rect(centerx=screen.get_width() / 2, y=10)
    screen.blit(titletext, titletextpos)   

    if startbutton.update(screen, mouse, mbu):
        combo = [randint(0, 7), randint(0, 7), randint(0, 7), randint(0, 7)]
        mastermind.mainmaster(screen, clock, 12, combo)

    elif quitbutton.update(screen, mouse, mbu):
        running = False

    mbu = False

    pygame.display.update()

pygame.quit