import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity


class Ghost(Entity):
    def __init__(self, node, pacmantest=None):####
        Entity.__init__(self, node)
        self.name = "ghost"
        self.points = 200 
        self.goal = Vector2()
        self.directionMethod = self.goalDirection
        self.pacman = pacmantest####

    def update(self, dt):####
        print(self.pacman.position)####
        Entity.update(self, dt)####
      



                             