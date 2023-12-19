from sys import exit
import pygame
import pickle
import datetime
from buttonhandle import button

pygame.init()

#-----setup stuff-----#
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
        

#from stackoverflow, https://stackoverflow.com/a/58541111/17493432 
def fadeout(screen : pygame.display, clock : pygame.time.Clock):
    fadeout = pygame.Surface((640, 480))
    fadeout = fadeout.convert()
    fadeout.fill((56, 56, 56))
    for i in range(60):
        clock.tick(60)
        fadeout.set_alpha(i)
        screen.blit(fadeout, (0, 0))
        pygame.display.update()

class dot(pygame.sprite.Sprite):
    def __init__(self, position, colorset, window):
        self.color = 0
        self.position = position
        self.colorset = colorset
        self.window = window
        pygame.sprite.Sprite.__init__(self)
        self.boundrect = pygame.draw.circle(window, self.colorset[self.color], (40 * self.position[0] + 260, 40 * self.position[1] + 20), 10)

    def update(self):

        pygame.draw.circle(self.window, (0, 0, 0), (40 * self.position[0] + 260, 40 * self.position[1] + 20), 12, width=2)
        pygame.draw.circle(self.window, self.colorset[self.color], (40 * self.position[0] + 260, 40 * self.position[1] + 20), 10)

    def clicked(self, colorind):
        
        self.color = colorind

        
def mainmaster(screen: pygame.display, clock: pygame.time.Clock, rowmax: int, combo : list, colorset : tuple):
    '''The main base function for the game
    screen is the screen things will be displaid on, clock is a pygame clock, rowmax is the num of rows with max of 11(to make it harder), 
    combo is the games final combo (set in main for networking), and gamefont is the font'''

    dots = pygame.sprite.Group()
    rownums = pygame.sprite.Group()
    gamefont = pygame.font.Font(None, 40)
    time = datetime.datetime.now() #used in game saving
    row = 0
    running = True
    guess = [0, 0, 0, 0]
    mbu = False
    win = False
    loss = False

    #these just create static screen elements

    for i in range(0, rowmax):
        for x in range(0, 4):
            dots.add(dot((x, i), colorset, screen))


    guessbutton = button((480, 400, 130, 50), (0, 80, 0), "Guess", 0, (502, 410))
    mainbutton = button((235, 215, 170, 50), (252, 252, 80), "Main Menu", 0, (245, 225))



    #-----setup stuff-----#


    while running:

        #-----mainloop-----#

        clock.tick(60)
        
        mouse = pygame.mouse.get_pos()

        for i in pygame.event.get():            
            match i.type:
                case pygame.QUIT:
                    running = False
                    pygame.quit
                    exit()

                case pygame.MOUSEBUTTONUP:

                    mbu = True

                    for j in dots:

                        #this just creates the hitboxes for the dots then checks if they were clicked
                        if j.boundrect.collidepoint(mouse) and (j.position[1]) == row:
                            x = j.position[0]

                            if i.button == 1 or i.button == 4:
                                if guess[x] != 7:
                                    guess[x] += 1

                                else:
                                    guess[x] = 0
                            else:
                                if guess[x] != 0:
                                    guess[x] -= 1
                                else:
                                    guess[x] = 7

                            j.clicked(guess[x])


        #time to draw stuff on the screen!
        screen.fill((56, 56, 56))

        pygame.draw.rect(screen, (10, 10, 10), (240, 0, 160, 480))


        dots.update()
        rownums.update(screen, gamefont)


        if not win and not loss:
            if guessbutton.update(screen, mouse, mbu, gamefont):
                #this deals with if the player presses the guess button
                #so here there is a bug where the game wants to say you have all 4 colors on the row if you put one color and that color happens to be in the combo
                #im getting around this by replacing the already "gone to" list items with an impossible (to the game at least) number, 8. if i did list.remove it just broke
                #thats what combocopy is for
                #aside from that weird fix this is really just simple code for checking if an item is in a list
                colorthere = 0
                inpos = 0
                combocopy = combo.copy()

                for i in range(0, 4):
                    if guess[i] in combo:
                        colorthere += 1

                        comboind = combo.index(guess[i])

                        if combo[comboind] == guess[comboind]:
                            inpos += 1


                        combo[comboind] = 8

                combo = combocopy.copy()


                strct = str(colorthere) #convert to a string for display
                strinp = str(inpos)
                classnums = [strct, strinp]

                rownums.add(rownum(row, classnums))

                if row < rowmax - 1:
                   if guess == combo:
                        fadeout(screen, clock)
                        win = True
                else:
                    fadeout(screen, clock)
                    loss = True


                row += 1
                guess = [0, 0, 0, 0]

        if win:
            screen.fill((56, 56, 56))
            wintext = gamefont.render("You did it!", True, (10, 10, 10))
            wintextpos = wintext.get_rect(centerx=screen.get_width() / 2, y=10)
            screen.blit(wintext, wintextpos)

        elif loss:
            screen.fill((56, 56, 56))
            losetext = gamefont.render("You lost", True, (10, 10, 10))
            losetextpos = losetext.get_rect(centerx=screen.get_width() / 2, y=10)
            screen.blit(losetext, losetextpos)


        if (win or loss) and mainbutton.update(screen, mouse, mbu, gamefont): #check if main menu button was pressed and then exit

            running = False

            with open("pastgames.dat", "ab") as file:

                data = []
                tempdata = []

                for i in rownums:
                    tempdata.append(i.nums)
                data.append(tempdata) #adding to the array which will contain all our data for this game

                tempdata = []
                for x in dots:
                    tempdata.append(x.color)
                data.append(tempdata)

                data.append(combo)
                data.append((time.year, time.month, time.day, time.hour, time.minute))

                pickle.dump(data, file) #Pickle allows us to use plain binary data for the file

        mbu = False


        pygame.display.update()