import pygame
from vector import Vector2
from constants import *

class Node(object):
    def __init__(self, row, column):
        self.row, self.column = row, column
        self.position = Vector2(column*TILEWIDTH, row*TILEHEIGHT)
        self.neighbors = {UP:None, DOWN:None, LEFT:None, RIGHT:None}
        
    def __str__(self):
        return "NODE at (" + str(self.row) + ", " + str(self.column)+")"

    def render(self, screen):
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                line_start = self.position.asTuple()
                line_end = self.neighbors[n].position.asTuple()
                pygame.draw.line(screen, WHITE, line_start, line_end, 4)
                pygame.draw.circle(screen, RED, self.position.asInt(), 12)


class NodeGroup(object):
    def __init__(self):
        self.nodeList = []
    
    def setupTestNodes(self):
        nodeA = Node(5, 5)
        nodeB = Node(5, 10)
        nodeC = Node(10, 5)
        nodeD = Node(10, 10)
        nodeE = Node(10, 13)
        nodeF = Node(20, 5)
        nodeG = Node(20, 13)
        nodeA.neighbors[RIGHT] = nodeB
        nodeA.neighbors[DOWN] = nodeC
        nodeB.neighbors[LEFT] = nodeA
        nodeB.neighbors[DOWN] = nodeD
        nodeC.neighbors[UP] = nodeA
        nodeC.neighbors[RIGHT] = nodeD
        nodeC.neighbors[DOWN] = nodeF
        nodeD.neighbors[UP] = nodeB
        nodeD.neighbors[LEFT] = nodeC
        nodeD.neighbors[RIGHT] = nodeE
        nodeE.neighbors[LEFT] = nodeD
        nodeE.neighbors[DOWN] = nodeG
        nodeF.neighbors[UP] = nodeC
        nodeF.neighbors[RIGHT] = nodeG
        nodeG.neighbors[UP] = nodeE
        nodeG.neighbors[LEFT] = nodeF
        self.nodeList = [nodeA, nodeB, nodeC, nodeD, nodeE, nodeF, nodeG]
        
    def render(self, screen):
        for node in self.nodeList:
            node.render(screen)
