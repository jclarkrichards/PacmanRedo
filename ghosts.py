import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity


class Ghost(Entity):
    def __init__(self, node):
        Entity.__init__(self, node)
        self.name = "ghost"
        self.points = 200 
        self.goal = Vector2()###
       
    """
    def update(self, dt):
        self.position += self.directions[self.direction]*self.speed*dt

        if self.overshotTarget():
            direction = self.getNextDirection()
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            #if self.target is self.node:
            #    self.direction = STOP
            self.setPosition()
        #else: 
        #    if self.oppositeDirection(direction):
        #        self.reverseDirection()
    """
   

    def goalDirection(self, directions):####
        distances = []
        for direction in directions:
            vec = self.node.neighbors[direction].position - self.goal
            distances.append(vec.magnitudeSquared())
        index = distances.index(min(distances))
        return directions[index]

    #def getNextDirection(self):
    #    validDirections = self.validDirections()
    #    return self.randomDirection(validDirections)###



                             