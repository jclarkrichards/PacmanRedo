import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from modes import ModeController


class Ghost(Entity):
    def __init__(self, node, pacman=None):
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200 
        self.goal = Vector2()
        self.directionMethod = self.goalDirection
        self.pacman = pacman
        self.mode = ModeController(self)

    def update(self, dt):
        self.mode.update(dt)

        if self.mode.current is SCATTER:
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()

        

        Entity.update(self, dt)

    def scatter(self):
        self.goal = Vector2()

    def chase(self):
        self.goal = self.pacman.position

    def spawn(self):
        self.goal = self.spawnNode.position

    def setSpawnNode(self, node):
        self.spawnNode = node
        print("SPAWN node at " + str(self.spawnNode.position))

    def startFreight(self):
        self.mode.setFreightMode()
        if self.mode.current == FREIGHT:
            print("Start freight mode")
            self.speed = 50
            self.directionMethod = self.randomDirection         
        self.points = 200

    def startSpawn(self):
        self.mode.setSpawnMode()
        if self.mode.current == SPAWN:
            self.speed = 150
            self.directionMethod = self.goalDirection
            self.spawn()

    def normalMode(self):
        self.speed = 100
        self.directionMethod = self.goalDirection
    


      



                             