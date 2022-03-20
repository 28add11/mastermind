from random import randint
import pygame

pygame.init()

#-----setup stuff-----#

screen = pygame.display.set_mode((640, 480))
running = True
mbd = False
clock = pygame.time.Clock()
row = 0
guess = [0, 0, 0, 0]
combo = [randint(0, 7), randint(0, 7), randint(0, 7), randint(0, 7)]
combocopy = combo
dots = pygame.sprite.Group()
gamefont = pygame.font.Font(None, 40)
guessframe = False
win = False
loss = False

print(combo)

class dot(pygame.sprite.Sprite):
    def __init__(self, color, position):
        self.color = color
        self.position = position
        pygame.sprite.Sprite.__init__(self)

    def update(self, window):
        pygame.draw.circle(window, self.color, self.position, 10)

    def clicked(self):
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

        
def mainmaster():
    
    screen.fill((193, 193, 193))
    pygame.draw.rect(screen, (10, 10, 10), (240, 0, 160, 480))
    for i in range(0, 12):
        for x in range(0, 4):
            dots.add(dot((53, 53, 53), (40 * x + 260, 40 * i + 20)))


    pygame.draw.rect(screen, (0, 0, 0), (495, 415, 140, 60))
    guessbox = pygame.Rect(500, 420, 130, 50)
    pygame.draw.rect(screen, (0, 80, 0), guessbox)
    guesstext = gamefont.render("Guess", True, (10, 10, 10))
    guesstextpos = (520, 430)
    screen.blit(guesstext, guesstextpos)

    #-----mainloop-----#

    while running:

        clock.tick(60)



        for i in pygame.event.get():
            match i.type:
                case pygame.QUIT:
                    running = False

                case pygame.MOUSEBUTTONUP:
                    mouse = pygame.mouse.get_pos()
                    if guessbox.collidepoint(mouse):
                        guessframe = True
                    else:
                        for i in dots:
                            irect = pygame.Rect(i.position[0] - 10, i.position[1] - 10, 20, 20)
                            if irect.collidepoint(mouse) and ((i.position[1] - 20) / 40) == row:
                                i.clicked()
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

                    if i == combo[guessind]:
                        inpos += 1

                    combo.remove(i)

            strct = str(colorthere)
            strinp = str(inpos)
            textct = gamefont.render(strct, True, (10, 10, 10))
            textinp = gamefont.render(strinp, True, (255, 50, 50))
            screen.blit(textct, pygame.rect.Rect(410, 40 * row + 10, 20, 20))
            screen.blit(textinp, pygame.rect.Rect(220, 40 * row + 10, 20, 20))

            if row < 11:
                if guess == combo:
                    win = True
            else:
                loss = True

            row += 1
            guessframe = False
            guess = [0, 0, 0, 0]
            combo = combocopy

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


pygame.quit