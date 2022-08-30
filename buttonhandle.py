import pygame


class button(pygame.sprite.Sprite):
    '''class for handling buttons in pygame. when the button is hovered over it will grow (waow.)
    will tell you if it's been clicked by returning true. check this by doing if button(args): then what you want it to do'''
    def __init__(self, rect : pygame.Rect, color : tuple, text : str, hoverframes : int, textpos : tuple):
        self.rect = pygame.Rect(rect[0] - 10, rect[1] - 10, rect[2] - 10, rect[3] - 10)
        self.rectcopy = rect
        self.color = color
        self.text = text
        self.hoverframes = hoverframes
        self.textpos = textpos
        
        self.colorcopy = color
        self.originalhover = hoverframes

        pygame.sprite.Sprite.__init__(self)

    def update(self, window : pygame.display, mousepos : tuple, mousebuttonup : bool, font : pygame.font.Font):

        if self.rect.collidepoint(mousepos):
            if self.hoverframes < 10:
                self.hoverframes += 1
        
        else:
            if self.hoverframes > self.originalhover:
                self.hoverframes -= 1


        self.rect = pygame.Rect(self.rectcopy[0] - self.hoverframes, self.rectcopy[1] - self.hoverframes, 
            self.rectcopy[2] + (self.hoverframes * 2), self.rectcopy[3] + (self.hoverframes * 2))

        if max(self.colorcopy) <= 245:
            self.color = (self.colorcopy[0] + self.hoverframes, self.colorcopy[1] + self.hoverframes, self.colorcopy[2] + self.hoverframes)


        pygame.draw.circle(window, self.color, (self.rect[0], self.rect[1]), 10, draw_top_left=True, draw_bottom_left=False, draw_bottom_right=False, draw_top_right=False)

        pygame.draw.circle(window, self.color, (self.rect[0] + self.rect[2], self.rect[1]), 
            10, draw_top_left=False, draw_bottom_left=False, draw_bottom_right=False, draw_top_right=True)

        pygame.draw.circle(window, self.color, (self.rect[0], self.rect[1] + self.rect[3]), 
            10, draw_top_left=False, draw_bottom_left=True, draw_bottom_right=False, draw_top_right=False)

        pygame.draw.circle(window, self.color, (self.rect[0] + self.rect[2], self.rect[1] + self.rect[3]), 
            10, draw_top_left=False, draw_bottom_left=False, draw_bottom_right=True, draw_top_right=False)


        pygame.draw.rect(window, self.color, pygame.Rect(self.rect[0], self.rect[1] - 10, self.rect[2], self.rect[3] + 20))
        pygame.draw.rect(window, self.color, pygame.Rect(self.rect[0] - 10, self.rect[1], self.rect[2] + 20, self.rect[3]))

        text = font.render(self.text, True, (10, 10, 10))
        window.blit(text, self.textpos)

        if self.rect.collidepoint(mousepos) and mousebuttonup:
            return True