import pygame
from constants import *

BASETILEWIDTH = 16
BASETILEHEIGHT = 16

class Spritesheet(object):
    def __init__(self):
        self.sheet = pygame.image.load("spritesheet.png").convert()
        transcolor = self.sheet.get_at((0,0))
        self.sheet.set_colorkey(transcolor)
        width = int(self.sheet.get_width() / BASETILEWIDTH * TILEWIDTH)
        height = int(self.sheet.get_height() / BASETILEHEIGHT * TILEHEIGHT)
        self.sheet = pygame.transform.scale(self.sheet, (width, height))
        
    def getImage(self, x, y, width, height):
        x *= TILEWIDTH
        y *= TILEHEIGHT
        self.sheet.set_clip(pygame.Rect(x, y, width, height))
        return self.sheet.subsurface(self.sheet.get_clip())

    
class PacmanSprites(Spritesheet):
    def __init__(self):
        Spritesheet.__init__(self)
        self.image = self.getStartImage()

    def getStartImage(self):
        return self.getImage(8, 0)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)


class GhostSprites(Spritesheet):
    def __init__(self, ghostname):
        Spritesheet.__init__(self)
        self.y = {BLINKY:4, PINKY:6, INKY:8, CLYDE:10}
        self.ghostname = ghostname
        self.image = self.getStartImage()

    def getStartImage(self):
        return self.getImage(0, self.y[self.ghostname])

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)


class FruitSprites(Spritesheet):
    def __init__(self):
        Spritesheet.__init__(self)
        self.image = self.getStartImage()

    def getStartImage(self):
        return self.getImage(16, 4)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)


##########
class LifeSprites(Spritesheet):
    def __init__(self, numlives):
        Spritesheet.__init__(self)
        self.images = []
        for i in range(numlives):
            self.images.append(self.getImage(0,0))

    def removeImage(self):
        if len(self.images) > 0:
            self.images.pop(0)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)




    
