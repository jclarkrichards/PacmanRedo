import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity


class Ghost(Entity):
    def __init__(self, node, pacmantest=None, mode=None):####
        Entity.__init__(self, node)
        self.name = "ghost"
        self.points = 200 
        self.goal = Vector2()
        self.directionMethod = self.goalDirection
        self.pacman = pacmantest####
        self.mode = mode###

    def update(self, dt):####
        #print(self.mode.mode)####
        if self.mode.mode is SCATTER:###
            self.scatter()###
        elif self.mode.mode is CHASE:###
            self.chase()###
        Entity.update(self, dt)####

    def scatter(self):
        #print("SCATTER")
        self.goal = Vector2()

    def chase(self):
        #print("CHASE")
        self.goal = self.pacman.position
      



                             