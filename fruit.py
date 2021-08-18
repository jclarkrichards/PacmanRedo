import pygame
from entity import Entity
from constants import *
from sprites import FruitSprites

class Fruit(Entity):
    def __init__(self, node, level=0):
        Entity.__init__(self, node)
        self.name = FRUIT
        self.color = GREEN
        self.lifespan = 5
        self.timer = 0
        self.destroy = False
        self.points = 100 + level*20
        self.setBetweenNodes(RIGHT)
        self.sprites = FruitSprites(self, level)

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.lifespan:
            self.destroy = True


class FruitMover(Entity):
    def __init__(self, node, goalnode, level=0):
        Entity.__init__(self, node)
        self.name = FRUIT
        self.color = GREEN
        #self.lifespan = 5
        #self.timer = 0
        self.destroy = False
        self.points = 100 + level*20
        #self.setBetweenNodes(RIGHT)
        self.setStartNode(node)
        self.sprites = FruitSprites(self, level)
        self.goal = goalnode.position
        self.directionMethod = self.goalDirection
        self.disablePortal = True
        #self.direction = RIGHT

    def update(self, dt):
        print(self.node.position)
        print(self.target.position)
        print(self.goal)
        print("")
        Entity.update(self, dt)
            