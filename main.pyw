import ctypes
import pygame
import os
import mastermind
import pastrender
from buttonhandle import button
from random import randint

pygame.init()

gamefont = pygame.font.Font(None, 40)

screen = pygame.display.set_mode((640, 480))
running = True
clock = pygame.time.Clock()
mbu = False

startbutton = button((80, 210, 80, 60), (0, 80, 0), "Start!", 0, (85, 225))
multibutton = button((280, 300, 80, 60), (255, 127, 0), "Multi", 0, (290, 315))
quitbutton = button((480, 210, 80, 60), (80, 0, 0), "Quit", 0, (490, 225))
prevbutton = button((280, 210, 80, 60), (252, 252, 80), "Past", 0, (290, 225))

#-----stuff-----#

while running:

    #-----mainloop-----#

    clock.tick(60)


    mouse = pygame.mouse.get_pos()

    #for every event, if that event is useful, do smthin
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

    tutorialtext = gamefont.render("The tutorial is in the readme file!", True, (10, 10, 10))
    tutorialtextpos = tutorialtext.get_rect(centerx=screen.get_width() / 2, y=420)
    screen.blit(tutorialtext, tutorialtextpos) 

    #cuz the button script returns true or false this works off that
    if startbutton.update(screen, mouse, mbu, gamefont):
        combo = [randint(0, 7), randint(0, 7), randint(0, 7), randint(0, 7)]
        mastermind.mainmaster(screen, clock, 12, combo)

    if quitbutton.update(screen, mouse, mbu, gamefont):
        running = False

    if prevbutton.update(screen, mouse, mbu, gamefont):
        if os.path.exists("pastgames.dat"):
            pastrender.renderpast(screen, clock)
        else:
            ctypes.windll.user32.MessageBoxW(0, u"File \"pastgames.dat\" does not exist.", u"Error", 0)

    mbu = False

    pygame.display.update()

pygame.quit