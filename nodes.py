import pygame
from vector import Vector2
from constants import *
import numpy as np

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
    def __init__(self, level):
        self.level = level
        self.nodesLUT = {} #Lookup table for the nodes
        data = self.readMazeFile(level)
        self.createNodeTable(data)
        self.connectHorizontally(data)
        self.connectVertically(data)

        #For checking
        for key in self.nodesLUT.keys():
            print(key)
            node = self.nodesLUT[key]
            for nkey in node.neighbors.keys():
                print(nkey)
                print(node.neighbors[nkey])
            print("")
            
    def readMazeFile(self, textfile):
        return np.loadtxt(textfile, dtype='<U1')

    def createNodeTable(self, data):
        for i in list(range(data.shape[0])):
            for j in list(range(data.shape[1])):
                if data[i][j] == '+':
                    self.nodesLUT[(i,j)] = Node(i, j)


    def connectHorizontally(self, data):
        for i in list(range(data.shape[0])):
            key = None
            for j in list(range(data.shape[1])):
                if data[i][j] == '+':
                    if key is None:
                        key = (i, j)
                    else:
                        self.nodesLUT[key].neighbors[RIGHT] = self.nodesLUT[(i,j)]
                        self.nodesLUT[(i,j)].neighbors[LEFT] = self.nodesLUT[key]
                        key = (i, j)
                elif data[i][j] != '-':
                    key = None


    def connectVertically(self, data):
        dataT = data.transpose()
        for i in list(range(dataT.shape[0])):
            key = None
            for j in list(range(dataT.shape[1])):
                if dataT[i][j] == '+':
                    if key is None:
                        key = (j, i)
                    else:
                        self.nodesLUT[key].neighbors[DOWN] = self.nodesLUT[(j, i)]
                        self.nodesLUT[(j, i)].neighbors[UP] = self.nodesLUT[key]
                        key = (j, i)
                elif dataT[i][j] != '|':
                    key = None

    def getPacmanNode(self):
        nodes = list(self.nodesLUT.values())
        return nodes[0]
    
    def render(self, screen):
        for node in self.nodesLUT.values():
            node.render(screen)
