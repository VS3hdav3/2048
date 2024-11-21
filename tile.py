import pygame
import math

class Tile:
    colors = [
        (237, 229, 218),
        (238, 225, 201),
        (243, 178, 122),
        (246, 150, 101),
        (247, 124, 95),
        (247, 95, 59),
        (237, 208, 115),
        (237, 204, 99),
        (236, 202, 80),
    ]
    
    def __init__(self, value, row, col, rect_width, rect_heigth):
        self.val = value
        self.row = row
        self.col = col
        self.x = col * rect_width
        self.y = row * rect_heigth
    
    def getColor(self):
        color_index = int(math.log2(self.val)) - 1
        color = self.colors[color_index]
        return color
    
    def draw(self, window, rect_width, rect_height, font, font_color1, font_color2):
        color = self.getColor()
        pygame.draw.rect(window, color, (self.x, self.y, rect_width, rect_height))
        if self.val <= 4:
            text = font.render(str(self.val), 1, font_color1)
        else:
            text = font.render(str(self.val), 1, font_color2)
        window.blit(text, (self.x + (rect_width / 2 - text.get_width() / 2),
                            self.y + (rect_height / 2 - text.get_height() / 2),),)
    
    def move(self, delta):
        self.x += delta[0]
        self.y += delta[1]
    
    def setPos(self, rect_width, rect_height, ceil=False):
        if ceil:
            self.row = math.ceil(self.y / rect_height)
            self.col = math.ceil(self.x / rect_width)
        else:
            self.row = math.floor(self.y / rect_height)
            self.col = math.floor(self.x / rect_width)

