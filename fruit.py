import pygame
from entity import Entity
from constants import *
from sprites import FruitSprites

class Fruit(Entity):
    def __init__(self, node, level=0):######fruit stuff
        Entity.__init__(self, node)
        self.name = FRUIT
        self.color = GREEN
        self.lifespan = 5
        self.timer = 0
        self.destroy = False
        self.points = 100 + level*20#####fruit stuff
        self.setBetweenNodes(RIGHT)
        self.sprites = FruitSprites(self, level)####fruit stuff

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.lifespan:
            self.destroy = True
            