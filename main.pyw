import pygame
from os import path, stat
from tkinter import messagebox
import pickle
import mastermind
import pastrender
from buttonhandle import button
from settings import setting
from random import randint


def main():
    pygame.init()


    icon = pygame.image.load('logo.png')
    pygame.display.set_icon(icon)

    pygame.display.set_caption("Mastermind", "epic gaming")

    gamefont = pygame.font.Font(None, 40)

    screen = pygame.display.set_mode((640, 480))
    running = True
    clock = pygame.time.Clock()
    mbu = False

    startbutton = button((80, 210, 80, 60), (0, 80, 0), "Start!", 0, (85, 225))
    settingbutton = button((280, 300, 80, 60), (255, 127, 0), "Sett.", 0, (290, 315))
    quitbutton = button((480, 210, 80, 60), (80, 0, 0), "Quit", 0, (490, 225))
    prevbutton = button((280, 210, 80, 60), (252, 252, 80), "Past", 0, (290, 225))

    if not path.exists("settings.conf"):
        with open("settings.conf", "wb") as file:
            pickle.dump(((53, 53, 53), (193, 193, 193), (255, 50, 50), (50, 255, 50), (50, 50, 255), (255, 255, 0),
                (255, 0, 255), (255, 127, 0)), file)

    tutorialtext = gamefont.render("The tutorial is in the readme file!", True, (10, 10, 10))
    tutorialtextpos = tutorialtext.get_rect(centerx=screen.get_width() / 2, y=420)
    titletext = gamefont.render("Mastermind", True, (10, 10, 10))
    titletextpos = titletext.get_rect(centerx=screen.get_width() / 2, y=10)


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
    
    
        screen.blit(titletext, titletextpos)   
        screen.blit(tutorialtext, tutorialtextpos) 

    #cuz the button script returns true or false this works off that
        if startbutton.update(screen, mouse, mbu, gamefont):
            combo = [randint(0, 7), randint(0, 7), randint(0, 7), randint(0, 7)]
            for i in range(7):
                if combo.count(i) > 3:
                    combo[combo.index(i)] = i + 1
            with open("settings.conf", "rb") as file:
                mastermind.mainmaster(screen, clock, 12, combo, pickle.load(file))

        if quitbutton.update(screen, mouse, mbu, gamefont):
            running = False

        if prevbutton.update(screen, mouse, mbu, gamefont):
            if path.exists("pastgames.dat") and stat("pastgames.dat").st_size > 0:
                with open("settings.conf", "rb") as file:
                    pastrender.renderpast(screen, clock, pickle.load(file))
            else:
                messagebox.showwarning("Warning", "Pastgames.dat doesn't exist or has no data. Play some games first!")
    
        if settingbutton.update(screen, mouse, mbu, gamefont):
            setting(screen, clock, gamefont)

        mbu = False

        pygame.display.update()

    pygame.quit

if __name__ == "__main__":
    main()
