import pygame
from vector import Vector2
from constants import *
import numpy as np

class Node(object):
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.neighbors = {UP:None, DOWN:None, LEFT:None, RIGHT:None, PORTAL:None}
        
    def __str__(self):
        return "NODE at (" + str(self.x) + ", " + str(self.y)+")"

    def render(self, screen):
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                line_start = self.position.asTuple()
                line_end = self.neighbors[n].position.asTuple()
                pygame.draw.line(screen, WHITE, line_start, line_end, 4)
                pygame.draw.circle(screen, RED, self.position.asInt(), 12)


class NodeGroup(object):
    def __init__(self, level):
        self.level = level
        self.nodesLUT = {} #Lookup table for the nodes
        data = self.readMazeFile(level)
        self.createNodeTable(data)
        self.connectHorizontally(data)
        self.connectVertically(data)
        
    def readMazeFile(self, textfile):
        return np.loadtxt(textfile, dtype='<U1')

    def createNodeTable(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                if data[row][col] == '+':
                    x, y = self.constructKey(col+xoffset, row+yoffset)
                    self.nodesLUT[(x, y)] = Node(x, y)

    def constructKey(self, x, y):
        return x * TILEWIDTH, y * TILEHEIGHT

    def connectHorizontally(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            key = None
            for col in list(range(data.shape[1])):
                if data[row][col] == '+':
                    if key is None:
                        key = self.constructKey(col+xoffset, row+yoffset)
                    else:
                        otherkey = self.constructKey(col+xoffset, row+yoffset)
                        self.nodesLUT[key].neighbors[RIGHT] = self.nodesLUT[otherkey]
                        self.nodesLUT[otherkey].neighbors[LEFT] = self.nodesLUT[key]
                        key = otherkey
                elif data[row][col] != '-':
                    key = None


    def connectVertically(self, data, xoffset=0, yoffset=0):
        dataT = data.transpose()
        for col in list(range(dataT.shape[0])):
            key = None
            for row in list(range(dataT.shape[1])):
                if dataT[col][row] == '+':
                    if key is None:
                        key = self.constructKey(col+xoffset, row+yoffset)
                    else:
                        otherkey = self.constructKey(col+xoffset, row+yoffset)
                        self.nodesLUT[key].neighbors[DOWN] = self.nodesLUT[otherkey]
                        self.nodesLUT[otherkey].neighbors[UP] = self.nodesLUT[key]
                        key = otherkey
                elif dataT[col][row] != '|':
                    key = None

    def getPacmanNode(self):
        nodes = list(self.nodesLUT.values())
        return nodes[0]

   
    def setPortalPair(self, pair1, pair2):
        key1 = self.constructKey(*pair1)
        key2 = self.constructKey(*pair2)
        if key1 in self.nodesLUT.keys() and key2 in self.nodesLUT.keys():
            self.nodesLUT[key1].neighbors[PORTAL] = self.nodesLUT[key2]
            self.nodesLUT[key2].neighbors[PORTAL] = self.nodesLUT[key1]
  
    def createHomeNodes(self, xoffset, yoffset):
        homedata = np.array([['.','.','+','.','.'],
                             ['.','.','|','.','.'],
                             ['+','.','|','.','+'],
                             ['+','-','+','-','+'],
                             ['+','.','.','.','+']])

        self.createNodeTable(homedata, xoffset, yoffset)
        print(list(self.nodesLUT.keys()))
        self.connectHorizontally(homedata, xoffset, yoffset)
        self.connectVertically(homedata, xoffset, yoffset)
        keyhome = self.constructKey(xoffset+2, yoffset)
        keyleft = self.constructKey(12, 14)
        keyright = self.constructKey(15, 14)
        print(keyhome)
        print(keyleft)
        print(keyright)
        self.nodesLUT[keyleft].neighbors[RIGHT] = self.nodesLUT[keyhome]
        self.nodesLUT[keyright].neighbors[LEFT] = self.nodesLUT[keyhome]
        self.nodesLUT[keyhome].neighbors[RIGHT] = self.nodesLUT[keyright]
        self.nodesLUT[keyhome].neighbors[LEFT] = self.nodesLUT[keyleft]
        

    def render(self, screen):
        for node in self.nodesLUT.values():
            node.render(screen)
