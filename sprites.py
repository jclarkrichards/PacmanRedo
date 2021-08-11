import pygame
from constants import *

class Spritesheet(object):
    def __init__(self):
        self.sheet = pygame.image.load("spritesheet.png").convert()   #self.sheet.get_size() --> (352, 368)
        transcolor = self.sheet.get_at((0,0))
        self.sheet.set_colorkey(transcolor)
        #width = self.sheet.get_width() / 16 * TILEWIDTH
        #height = self.sheet.get_height() / 16 * TILEHEIGHT
        #self.sheet = pygame.transform.scale(self.sheet, (width, height))#Add later when you need to stretch and/or squish in x and y directions.  This will resize the sheet
        
    def getImage(self, x, y, width, height):
        x *= width
        y *= height
        self.sheet.set_clip(pygame.Rect(x, y, width, height))
        return self.sheet.subsurface(self.sheet.get_clip())
