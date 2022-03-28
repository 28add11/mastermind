import pygame


class button(pygame.sprite.Sprite):
    '''class for handling buttons in pygame. when the button is hovered over it will grow (waow.)
    also will tell you if it's been clicked'''
    def __init__(self, rect : pygame.Rect, color : tuple, text : str, hoverframes : int, textpos : tuple):
        self.rect = pygame.Rect(rect)
        self.rectcopy = pygame.Rect(rect)
        self.color = color
        self.text = text
        self.hoverframes = hoverframes
        self.textpos = textpos
        
        self.colorcopy = color
        self.originalhover = hoverframes

        pygame.sprite.Sprite.__init__(self)

    def update(self, window : pygame.display, mousepos : tuple, mousebuttonup : bool):

        font = pygame.font.Font(None, 40)

        if self.rect.collidepoint(mousepos):


            if self.hoverframes < 10:
                self.hoverframes += 1
            
            self.color = (self.colorcopy[0] + self.hoverframes, self.colorcopy[1] + self.hoverframes, self.colorcopy[2] + self.hoverframes)

            if self.rect.collidepoint(mousepos) and mousebuttonup:
                return True
        
        else:


            if self.hoverframes > self.originalhover:
                self.hoverframes -= 1

            self.color = (self.colorcopy[0] + self.hoverframes, self.colorcopy[1] + self.hoverframes, self.colorcopy[2] + self.hoverframes)

        self.rect = pygame.Rect(self.rectcopy[0] - self.hoverframes, self.rectcopy[1] - self.hoverframes, 
        self.rectcopy[2] + (self.hoverframes * 2), self.rectcopy[3] + (self.hoverframes * 2))


        pygame.draw.rect(window, (0, 0, 0), (self.rect[0] - 5, self.rect[1] - 5, 
            self.rect[2] + 10, self.rect[3] + 10))

        pygame.draw.rect(window, self.color, self.rect)

        text = font.render(self.text, True, (10, 10, 10))
        window.blit(text, self.textpos)