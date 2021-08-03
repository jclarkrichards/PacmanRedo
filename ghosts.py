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

    def update(self, dt):
        if self.mainmode.mode is SCATTER:
            self.scatter()
        elif self.mainmode.mode is CHASE:
            self.chase()
        Entity.update(self, dt)

    def scatter(self):
        self.goal = Vector2()

    def chase(self):
        self.goal = self.pacman.position
      



                             