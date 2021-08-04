import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity


class Ghost(Entity):
    def __init__(self, node, pacman=None, mode=None):
        Entity.__init__(self, node)
        self.name = "ghost"
        self.points = 200 
        self.goal = Vector2()
        self.directionMethod = self.goalDirection
        self.pacman = pacman
        self.mainmode = mode
        self.othermode = None###

    def update(self, dt):
        if self.othermode is None:####
            if self.mainmode.mode is SCATTER:
                self.scatter()
            elif self.mainmode.mode is CHASE:
                self.chase()
        else:###
            self.timer += dt###
            if self.timer >= self.modetime:###
                self.normalMode()####

        Entity.update(self, dt)

    def scatter(self):
        self.goal = Vector2()

    def chase(self):
        self.goal = self.pacman.position

    ####
    def startFreight(self):
        if self.mainmode.mode in [SCATTER, CHASE]:
            print("Start freight mode")
            self.othermode = FREIGHT
            self.speed = 50
            self.directionMethod = self.randomDirection
            self.modetime = 7
            self.timer = 0
        elif self.mainmode.mode is FREIGHT:
            self.timer = 0
        self.points = 200

    def normalMode(self):
        self.speed = 100
        self.directionMethod = self.goalDirection
        self.othermode = None
    ####


      



                             