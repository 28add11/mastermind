import pygame
from os import path, stat
from tkinter import messagebox
import pickle
import mastermind #Each of our seperate "pages" is a different function
import pastrender
from buttonhandle import button
from settings import setting
from random import randint


def main():
    pygame.init()


    icon = pygame.image.load('logo.png')
    pygame.display.set_icon(icon)

    pygame.display.set_caption("Mastermind", "Mastermind Game")

    gamefont = pygame.font.Font(None, 40)

    screen = pygame.display.set_mode((640, 480))
    running = True
    clock = pygame.time.Clock()
    mbu = False
    framecounter = 0

    startbutton = button((80, 210, 80, 60), (0, 80, 0), "Start!", 0, (85, 225))
    settingbutton = button((280, 300, 80, 60), (255, 127, 0), "Sett.", 0, (290, 315))
    quitbutton = button((480, 210, 80, 60), (80, 0, 0), "Quit", 0, (490, 225))
    prevbutton = button((280, 210, 80, 60), (252, 252, 80), "Past", 0, (290, 225))

    if not path.exists("settings.conf"): #Create settings file if one does not exist and fill it with the default values
        with open("settings.conf", "wb") as file:
            pickle.dump(((53, 53, 53), (193, 193, 193), (255, 50, 50), (50, 255, 50), (50, 50, 255), (255, 255, 0),
                (255, 0, 255), (255, 127, 0)), file)

    tutorialtext = gamefont.render("The tutorial is in the readme file!", True, (10, 10, 10))
    tutorialtextpos = tutorialtext.get_rect(centerx=screen.get_width() / 2, y=420)
    titletext = gamefont.render("Mastermind", True, (10, 10, 10))
    titletextpos = titletext.get_rect(centerx=screen.get_width() / 2, y=10)


    #-----setup stuff-----#

    while running:

        #-----mainloop-----#

        clock.tick(60) #Limit framerate to 60FPS

        mouse = pygame.mouse.get_pos()

        #for every event, if that event is useful, do a thing
        for i in pygame.event.get():            
            match i.type:
                case pygame.QUIT:
                    running = False #Don't exit execution immediately, to allow for cleaning up assets
                case pygame.MOUSEBUTTONUP:
                        mbu = True #Use a boolean to allow for checking in better locations

        screen.fill((56, 56, 56)) 

        for x in range(-50, 640, 25): #Dot scrolling animation
            for y in range(-50, 480, 25):
                pygame.draw.circle(screen, (41, 41, 41), (x + framecounter / 2, y + framecounter / 2), 5)
    
        screen.blit(titletext, titletextpos)   
        screen.blit(tutorialtext, tutorialtextpos) 

        #Button script returns boolean if clicked when drawn, so we exclude the need for a seperate drawing call
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
                messagebox.showwarning("Warning", "Pastgames.dat doesn't exist or has no data. Play some games first!") #windows msg box
    
        if settingbutton.update(screen, mouse, mbu, gamefont):
            setting(screen, clock, gamefont)

        mbu = False

        pygame.display.update()

        framecounter += 1 #used to display background effects
        if framecounter > 100:
            framecounter = 0

    pygame.quit

if __name__ == "__main__": #For functional calling structure, more flexible when substituting code
    main()
