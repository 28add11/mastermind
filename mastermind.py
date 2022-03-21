import pygame

pygame.init()

#-----setup stuff-----#

class dot(pygame.sprite.Sprite):
    def __init__(self, color, position):
        self.color = color
        self.position = position
        pygame.sprite.Sprite.__init__(self)

    def update(self, window):
        pygame.draw.circle(window, self.color, self.position, 10)

    def clicked(self, plus):
        match self.color:
            case (53, 53, 53):
                self.color = (193, 193, 193)
            case (193, 193, 193):
                self.color = (255, 50, 50)
            case (255, 50, 50):
                self.color = (50, 255, 50)
            case (50, 255, 50):
                self.color = (50, 50, 255)
            case (50, 50, 255):
                self.color = (255, 255, 0)
            case (255, 255, 0):
                self.color = (255, 0, 255)
            case (255, 0, 255):
                self.color = (255, 127, 0)
            case (255, 127, 0):
                self.color = (53, 53, 53)

        
def mainmaster(screen: pygame.display, clock: pygame.time.Clock, rowmax: int, combo, gamefont):
    '''The main base function for the game
    screen is the screen things will be displaid on, clock is a pygame clock, rowmax is the num of rows with max of 11(to make it harder), 
    combo is the games final combo (set in main for networking), and gamefont is the font'''

    dots = pygame.sprite.Group()
    row = 0
    running = True
    win = False
    loss = False
    guessframe = False
    guess = [0, 0, 0, 0]

    #dots is the group with dots (i know, revolutionary)
    #row is the current row you are playing on
    #running is... i dont know maybe if the game is running
    #win. did you win?
    #loss. did you lose?
    #guessframe tells if you pressed the guess button on that frame

    #those were some patronising comments

    print(combo)
    
    #these just create static screen elements
    screen.fill((193, 193, 193))
    pygame.draw.rect(screen, (10, 10, 10), (240, 0, 160, 480))
    for i in range(0, rowmax):
        for x in range(0, 4):
            dots.add(dot((53, 53, 53), (40 * x + 260, 40 * i + 20)))


    pygame.draw.rect(screen, (0, 0, 0), (495, 415, 140, 60))
    guessbox = pygame.Rect(500, 420, 130, 50)
    pygame.draw.rect(screen, (0, 80, 0), guessbox)
    guesstext = gamefont.render("Guess", True, (10, 10, 10))
    guesstextpos = (520, 430)
    screen.blit(guesstext, guesstextpos)

    #-----stuff-----#


    while running:
    #-----mainloop-----#

        clock.tick(60)



        for i in pygame.event.get():            
            match i.type:
                case pygame.QUIT:
                    running = False

                case pygame.MOUSEBUTTONUP:
                    #this first bit just is about getting all the important shit
                    #colorup is for wether the colors of the dots go up or down
                    if i.button == 1 or i.button == 4:
                        colorup = True
                    else:
                        colorup = False
                    mouse = pygame.mouse.get_pos()

                    if guessbox.collidepoint(mouse):
                        guessframe = True

                    else: #else because no one is going to click both at the same time unless they are doing some magic
                        for i in dots:
                            irect = pygame.Rect(i.position[0] - 10, i.position[1] - 10, 20, 20) #hehe irect sounds like erect
                            #in all seriousness though, this just creates the hitboxes for the dots then checks if they were clicked
                            if irect.collidepoint(mouse) and ((i.position[1] - 20) / 40) == row:
                                i.clicked(colorup)
                                x = (i.position[0] - 260) / 40
                                x = int(x)
                                if guess[x] != 7:
                                    guess[x] += 1
                                else:
                                    guess[x] = 0



        dots.update(screen)

        if guessframe:

            colorthere = 0
            inpos = 0

            for i in guess:
                if i in combo:
                    colorthere += 1
                    guessind = guess.index(i)
                    print(guessind, combo, guess)

                    if i == combo[guessind]:
                        inpos += 1

                    guess.remove(i)

            strct = str(colorthere)
            strinp = str(inpos)
            textct = gamefont.render(strct, True, (10, 10, 10))
            textinp = gamefont.render(strinp, True, (255, 50, 50))
            screen.blit(textct, pygame.rect.Rect(410, 40 * row + 10, 20, 20))
            screen.blit(textinp, pygame.rect.Rect(220, 40 * row + 10, 20, 20))

            if row < rowmax - 1:
                if guess == combo:
                    win = True
            else:
                loss = True

            row += 1
            guessframe = False
            guess = [0, 0, 0, 0]
            

        if win:
            screen.fill((193, 193, 193))
            wintext = gamefont.render("You did it!", True, (10, 10, 10))
            wintextpos = wintext.get_rect(centerx=screen.get_width() / 2, y=10)
            screen.blit(wintext, wintextpos)            

        if loss:
            screen.fill((193, 193, 193))
            losetext = gamefont.render("You lost", True, (10, 10, 10))
            losetextpos = losetext.get_rect(centerx=screen.get_width() / 2, y=10)
            screen.blit(losetext, losetextpos)


        pygame.display.update()