from buttonhandle import button
import pygame
import pickle

pygame.init()

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
        self.position = position
        pygame.sprite.Sprite.__init__(self)

    def update(self, window):
        colors = ((53, 53, 53), (193, 193, 193), (255, 50, 50), (50, 255, 50), (50, 50, 255), (255, 255, 0),
            (255, 0, 255), (255, 127, 0))

        pygame.draw.circle(window, colors[self.color], (40 * self.position[0] + 260, 40 * self.position[1] + 20), 10)

class text(pygame.sprite.Sprite):
    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        pygame.sprite.Sprite.__init__(self)

    def update(self, window):
        window.blit(self.text, self.pos)



def renderpast(screen: pygame.display, clock: pygame.time.Clock):

    dots = pygame.sprite.Group()
    rownums = pygame.sprite.Group()
    texts = pygame.sprite.Group()
    gamefont = pygame.font.Font(None, 40)
    running = True

    fowardbutton = button((480, 400, 130, 50), (0, 80, 0), "Guess", 0, (502, 410))

    with open("pastgames", "rb") as file:

        content = file.readlines()
        maxlineind = len(content) - 1
        data = pickle.loads(content[maxlineind])
        dataindex = 0
        for i in data[0]:
            rownums.add(rownum(dataindex, i))
            dataindex += 1

        dataindex = 0
        dotsdata = data[1]
        for x in range(0, 12):
            for y in range(0, 4):
                dots.add(dot(dotsdata[dataindex], (y, x)))
                dataindex += 1
        

        combodata = data[2]
        combotext = gamefont.render("Combo: ", True, (10, 10, 10))
        combodattext = gamefont.render(str(combodata), True, (10, 10, 10))
        combopos = combotext.get_rect(x = 440, y = 10)
        combodatapos = combodattext.get_rect(x = 445, y = 40)
        texts.add(text(combotext, combopos))
        texts.add(text(combodattext, combodatapos))


        datedata = data[3]
        datetext = gamefont.render("The tutorial is in the readme file!", True, (10, 10, 10))

        

    while running:

        clock.tick(60)

        mouse = pygame.mouse.get_pos()

        for i in pygame.event.get():            
            match i.type:
                case pygame.QUIT:
                    running = False
                    pygame.quit
                    quit()

                case pygame.MOUSEBUTTONUP:
                    mbu = True

        
        screen.fill((193, 193, 193))

        pygame.draw.rect(screen, (10, 10, 10), (240, 0, 160, 480))

        dots.update(screen)
        rownums.update(screen, gamefont)
        texts.update(screen)

        pygame.display.update()