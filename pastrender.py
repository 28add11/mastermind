from sys import exit
from buttonhandle import button
import pygame
import pickle
from tkinter import messagebox

pygame.init()

def loadall(filename):
    #TYSM stackoverflow!!!
    with open(filename, "rb") as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break


#two classes from mastermind.py

class rownum(pygame.sprite.Sprite):
    def __init__(self, row : int, nums : list):
        self.row = row
        self.nums = nums
        pygame.sprite.Sprite.__init__(self)
    
    def update(self, window, font):
        textct = font.render(self.nums[0], True, (10, 10, 10))
        textinp = font.render(self.nums[1], True, (255, 50, 50))
        window.blit(textct, pygame.rect.Rect(410, 40 * self.row + 10, 20, 20))
        window.blit(textinp, pygame.rect.Rect(220, 40 * self.row + 10, 20, 20))
        


class dot(pygame.sprite.Sprite):
    def __init__(self, color, position):
        self.color = color
        self.position = (40 * position[0] + 260, 40 * position[1] + 20)
        pygame.sprite.Sprite.__init__(self)

    def update(self, window, colors):
        
        pygame.draw.circle(window, colors[self.color], (self.position[0], self.position[1]), 10)

#for simple, more clean text rendering
class text(pygame.sprite.Sprite):
    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        pygame.sprite.Sprite.__init__(self)

    def update(self, window):
        window.blit(self.text, self.pos)

def deleter(index):
    content = list(loadall("pastgames.dat"))
    content.pop(index)
    with open("pastgames.dat", "wb") as file:
        for i in content:
            pickle.dump(i, file)

#now I could break this code up... but
def render_and_dat(textgroup : pygame.sprite.Group, dotgroup : pygame.sprite.Group, numsgroup : pygame.sprite.Group, gamefont : pygame.sprite.Group, dataind : int):
    #empties the groups for new data
    textgroup.empty()
    dotgroup.empty()
    numsgroup.empty()
        
    #load all data in the file, get the one with the right index, get data
    content = list(loadall("pastgames.dat"))
    data = content[dataind]
    dataindex = 0       
    for i in data[0]:
        numsgroup.add(rownum(dataindex, i))
        dataindex += 1

    dataindex = 0
    dotsdata = data[1]
    for x in range(0, 12):
        for y in range(0, 4):
            dotgroup.add(dot(dotsdata[dataindex], (y, x)))
            dataindex += 1
        

    #I say I made a class for text to make things easy, but
    combotext = gamefont.render("Combo: ", True, (10, 10, 10))
    combopos = combotext.get_rect(x = 440, y = 10)
    textgroup.add(text(combotext, combopos))
    combodata = data[2]

    dataindex = 0
    for i in combodata:
        dotgroup.add(dot(i, (dataindex + 5, 1)))
        dataindex += 1


    datedata = data[3]
    datetext0 = gamefont.render("game of: ", 
    True, (10, 10, 10))
    datepos0 = datetext0.get_rect(x = 10, y = 10)
    datetext1 = gamefont.render(str(datedata[1]) + "/" + str(datedata[2]) + "/" + str(datedata[0]), 
    True, (10, 10, 10))
    datepos1 = datetext1.get_rect(x = 15, y = 40)
    datetext2 = gamefont.render(str(datedata[3]) + ":" + str(datedata[4]), 
    True, (10, 10, 10))
    datepos2 = datetext2.get_rect(x = 30, y = 70)        
    textgroup.add(text(datetext0, datepos0))
    textgroup.add(text(datetext1, datepos1))
    textgroup.add(text(datetext2, datepos2))



def renderpast(screen: pygame.display, clock: pygame.time.Clock, colors : tuple):
#the main function, has all the stuff for the UI
    dots = pygame.sprite.Group()
    rownums = pygame.sprite.Group()
    texts = pygame.sprite.Group()
    gamefont = pygame.font.Font(None, 40)
    running = True
    

    forwardbutton = button((480, 400, 130, 50), (0, 80, 0), "->", 0, (502, 410))
    backbutton = button((50, 400, 130, 50), (0, 80, 0), "<-", 0, (100, 410))
    menubutton = button((480, 300, 130, 50), (80, 0, 0), "Menu", 0, (505, 310))
    deletebutton = button((50, 300, 130, 50), (80, 0, 0), "Delete", 0, (75, 310))


    maxlineind = len(list(loadall("pastgames.dat"))) - 1
    lineind = maxlineind #sets first thing displayed to most recent game
    render_and_dat(texts, dots, rownums, gamefont, lineind)
        
#-----setup-----#
    while running:
#-----mainloop-----#
        screen.fill((193, 193, 193))
        pygame.draw.rect(screen, (10, 10, 10), (440, 40, 160, 40))
        clock.tick(60)
        mbu = False

        mouse = pygame.mouse.get_pos()

        for i in pygame.event.get():            
            match i.type:
                case pygame.QUIT:
                    running = False
                    pygame.quit
                    exit()

                case pygame.MOUSEBUTTONUP:
                    mbu = True

        if forwardbutton.update(screen, mouse, mbu, gamefont):
            if lineind == maxlineind:
                lineind = 0
            else:
                lineind += 1
            render_and_dat(texts, dots, rownums, gamefont, lineind)

        if backbutton.update(screen, mouse, mbu, gamefont):
            if lineind == 0:
                lineind = maxlineind
            else:
                lineind -= 1
            
            render_and_dat(texts, dots, rownums, gamefont, lineind)
        
        if menubutton.update(screen, mouse, mbu, gamefont):
            running = False
        
        if deletebutton.update(screen, mouse, mbu, gamefont):
            if messagebox.askokcancel("Are You Sure", "Are you sure you want to delete this game?"):
                deleter(lineind)
                running = False

        pygame.draw.rect(screen, (10, 10, 10), (240, 0, 160, 480))

        dots.update(screen, colors)
        rownums.update(screen, gamefont)
        texts.update(screen)

        pygame.display.update()
