from os import path, remove
import pygame
import pickle
from buttonhandle import button
from tkinter import colorchooser, messagebox
from sys import exit

pygame.init()

def save(data : pygame.Color):
    with open("settings.conf", "wb") as file:
        pickle.dump(data, file)

class magicbutton(pygame.sprite.Sprite): #Modified button class to match up with display elements
    def __init__(self, xpos : int, color : tuple):
        self.rect = pygame.Rect((((xpos * 64) + 64) - 10, 180, 20, 20))
        self.rectcopy = pygame.Rect((((xpos * 64) + 96) - 10, 180, 20, 20))
        self.hoverframes = 0
        self.originalhover = 0
        self.color = color
        self.colorcopy = color
        pygame.sprite.Sprite.__init__(self)

    def update(self, window : pygame.display, mousepos : tuple, mousebuttonup : bool):

        if self.rect.collidepoint(mousepos):
            if self.hoverframes < 10:
                self.hoverframes += 1
        
        else:
            if self.hoverframes > 0:
                self.hoverframes -= 1

        self.rect = pygame.Rect(self.rectcopy[0] - self.hoverframes, self.rectcopy[1] - self.hoverframes, 
        self.rectcopy[2] + (self.hoverframes * 2), self.rectcopy[3] + (self.hoverframes * 2))


        pygame.draw.rect(window, (0, 0, 0), (self.rect[0] - 5, self.rect[1] - 5, 
            self.rect[2] + 10, self.rect[3] + 10))

        pygame.draw.rect(window, self.color, self.rect)

        if self.rect.collidepoint(mousepos) and mousebuttonup:
            self.color = colorchooser.askcolor(self.color)[0]
            
            if self.color == None:
                self.color = self.colorcopy
            else:
                self.colorcopy = self.color




def setting(screen : pygame.display, clock : pygame.time.Clock, font : pygame.font.Font):

    running = True
    mbu  = False
    buttongroup = pygame.sprite.Group()

    menubutton = button((480, 400, 130, 50), (80, 0, 0), "Menu", 0, (505, 410))
    defaultbutton = button((50, 400, 130, 50), (0, 80, 0), "Reset", 0, (75, 410))
    clearbutton = button((50, 280, 130, 50), (255, 255, 0), "Erase", 0, (75, 290))

    with open("settings.conf", "rb") as file:
        colors = pickle.load(file)

    for i in range(8):
        buttongroup.add(magicbutton(i, colors[i]))

    colorstext = font.render("Dot colors", True, (10, 10, 10))
    clearstext = font.render("Clear past games", True, (10, 10, 10))
    titletext = font.render("Settings", True, (10, 10, 10))
    titletextpos = titletext.get_rect(centerx=screen.get_width() / 2, y=10)

    #-----stuff-----#

    while running:

    #-----mainloop-----#

        clock.tick(60)
        mouse = pygame.mouse.get_pos()
        for i in pygame.event.get():            
            match i.type:
                case pygame.QUIT:
                    running = False
                    exit()
                case pygame.MOUSEBUTTONUP:
                    mbu = True
        
        screen.fill((56, 56, 56))
    

        screen.blit(titletext, titletextpos)
        screen.blit(colorstext, (10, 120))
        screen.blit(clearstext, (10, 230))

        buttongroup.update(screen, mouse, mbu)

        if menubutton.update(screen, mouse, mbu, font):
            running = False
            with open("settings.conf", "wb") as file:
                newcolor = []
                for i in buttongroup:
                    newcolor.append(i.color)
                newcolor = tuple(newcolor)
                pickle.dump(newcolor, file)

        if defaultbutton.update(screen, mouse, mbu, font):
            with open("settings.conf", "wb") as file:
                colors = ((53, 53, 53), (193, 193, 193), (255, 50, 50), (50, 255, 50), (50, 50, 255), (255, 255, 0),
                (255, 0, 255), (255, 127, 0))
                for i, x in zip(buttongroup, range(8)):
                    i.color = colors[x]
                pickle.dump(colors, file)

        if clearbutton.update(screen, mouse, mbu, font):
            if not path.exists("pastgames.dat"):
                messagebox.showwarning("Warning", "You have no past games that need erasing.")
            elif messagebox.askokcancel("Are You Sure", "Are you sure you want to delete all pastgames?"):
                remove("pastgames.dat")
                

        mbu = False

        pygame.display.update()