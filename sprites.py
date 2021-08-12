import pygame
from constants import *
from animation import Animator######Animation

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
        self.image = self.getStartImage()
        self.entity = entity####testing
        self.animations = {}###########Animations
        self.defineAnimations()############

    ############Animations
    def defineAnimations(self):
        self.animations[LEFT] = Animator(LOOPANIM, ((8,0), (0, 0), (0, 2), (0, 0)))
        self.animations[RIGHT] = Animator(LOOPANIM, ((8,0), (2, 0), (2, 2), (2, 0)))
        self.animations[UP] = Animator(LOOPANIM, ((8,0), (6, 0), (6, 2), (6, 0)))
        self.animations[DOWN] = Animator(LOOPANIM, ((8,0), (4, 0), (4, 2), (4, 0)))

    def update(self, dt):############Animation
        if self.entity.direction == LEFT:
            self.image = self.getImage(*self.animations[LEFT].update(dt))
        elif self.entity.direction == RIGHT:
            self.image = self.getImage(*self.animations[RIGHT].update(dt))
        elif self.entity.direction == DOWN:
            self.image = self.getImage(*self.animations[DOWN].update(dt))
        elif self.entity.direction == UP:
            self.image = self.getImage(*self.animations[UP].update(dt))
        elif self.entity.direction == STOP:
            self.image = self.getImage(8, 0)
    #######

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




    
