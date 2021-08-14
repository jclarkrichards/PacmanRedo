import pygame
from constants import *
from animation import Animator
import numpy as np

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
    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.entity = entity
        self.entity.image = self.getStartImage()       
        self.animations = {}
        self.defineAnimations()

    def defineAnimations(self):
        self.animations[LEFT] = Animator(((8,0), (0, 0), (0, 2), (0, 0)))
        self.animations[RIGHT] = Animator(((8,0), (2, 0), (2, 2), (2, 0)))
        self.animations[UP] = Animator(((8,0), (6, 0), (6, 2), (6, 0)))
        self.animations[DOWN] = Animator(((8,0), (4, 0), (4, 2), (4, 0)))

    def update(self, dt):
        if self.entity.direction == LEFT:
            self.entity.image = self.getImage(*self.animations[LEFT].update(dt))
        elif self.entity.direction == RIGHT:
            self.entity.image = self.getImage(*self.animations[RIGHT].update(dt))
        elif self.entity.direction == DOWN:
            self.entity.image = self.getImage(*self.animations[DOWN].update(dt))
        elif self.entity.direction == UP:
            self.entity.image = self.getImage(*self.animations[UP].update(dt))
        elif self.entity.direction == STOP:
            self.entity.image = self.getImage(8, 0)

    def getStartImage(self):
        return self.getImage(8, 0)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)


class GhostSprites(Spritesheet):
    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.y = {BLINKY:4, PINKY:6, INKY:8, CLYDE:10}
        self.entity = entity
        self.entity.image = self.getStartImage()
        self.animations = {}
        self.defineAnimations()

    def defineAnimations(self):
        y = self.y[self.entity.name]
        self.animations[UP] = Animator(((0, y), (2, y)))
        self.animations[DOWN] = Animator(((4, y), (6, y)))
        self.animations[LEFT] = Animator(((8, y), (10, y)))
        self.animations[RIGHT] = Animator(((12, y), (14, y)))
        self.animations[FREIGHT] = Animator()#####
        
    def update(self, dt):
        if self.entity.direction == LEFT:
            self.entity.image = self.getImage(*self.animations[LEFT].update(dt))
        elif self.entity.direction == RIGHT:
            self.entity.image = self.getImage(*self.animations[RIGHT].update(dt))
        elif self.entity.direction == DOWN:
            self.entity.image = self.getImage(*self.animations[DOWN].update(dt))
        elif self.entity.direction == UP:
            self.entity.image = self.getImage(*self.animations[UP].update(dt))
       

    def getStartImage(self):
        return self.getImage(0, self.y[self.entity.name])

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)


class FruitSprites(Spritesheet):
    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.entity = entity
        self.entity.image = self.getStartImage()

    def getStartImage(self):
        return self.getImage(16, 4)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)


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



class MazeSprites(Spritesheet):
    def __init__(self, mazefile, rotfile, level=1, xstart=0):
        Spritesheet.__init__(self)
        self.level = level
        self.xstart = xstart
        self.data = self.readMazeFile(mazefile)
        self.rotdata = self.readMazeFile(rotfile)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, TILEWIDTH, TILEHEIGHT)

    def readMazeFile(self, mazefile):
        return np.loadtxt(mazefile, dtype='<U1')

    def constructBackground(self, background):
        for row in list(range(self.data.shape[0])):
            for col in list(range(self.data.shape[1])):
                if self.data[row][col].isdigit():
                    x = int(self.data[row][col]) + self.xstart
                    y = 16+self.level
                    sprite = self.getImage(x, y)
                    rotval = int(self.rotdata[row][col])
                    sprite = self.rotate(sprite, rotval)
                    background.blit(sprite, (col*TILEWIDTH, row*TILEHEIGHT))
                elif self.data[row][col] == '=':
                    sprite = self.getImage(10, 16+self.level)
                    background.blit(sprite, (col*TILEWIDTH, row*TILEHEIGHT))

        return background

    def rotate(self, sprite, value):
        return pygame.transform.rotate(sprite, value*90)
                





    
