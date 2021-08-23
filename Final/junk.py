from vector import Vector2
from constants import *

class MazeBase(object):
    def __init__(self):
        self.name = ""
        self.portalPairs = {}
        self.homeoffset = []
        self.homenodeconnectLeft = []
        self.homenodeconnectRight = []
        self.pacmanStart = []
        self.fruitStart = []
        self.ghostNodeDeny = {UP:None, DOWN:None, LEFT:None, RIGHT:None}

    def setup(self, nodegroup, pacman, ghostgroup):
        self.setPortals(nodegroup)
        self.denyAccess(nodegroup, pacman, ghostgroup)

    def denyAccess(self, nodegroup, pacman, ghostgroup):
        nodegroup.denyHomeAccess(pacman)
        nodegroup.denyHomeAccessList(ghostgroup)
        x, y = self.addoffset(2, 3)
        nodegroup.denyAccessList(x, y, LEFT, ghostgroup)
        nodegroup.denyAccessList(x, y, RIGHT, ghostgroup)

        for direction in list(self.ghostNodeDeny.keys()):
            if self.ghostNodeDeny[direction] is not None:
                for x, y in self.ghostNodeDeny[direction]:
                    nodegroup.denyAccessList(x, y, direction, ghostgroup)


    def getPacmanStartNode(self, nodegroup):
        pacstartkey = nodegroup.constructKey(*self.pacmanStart)
        return nodegroup.nodesLUT[pacstartkey]

    def getBlinkyStartNode(self, nodegroup):
        return self.getGhostStart(nodegroup, 2, 0)

    def getPinkyStartNode(self, nodegroup):
        return self.getGhostStart(nodegroup, 2, 3)

    def getInkyStartNode(self, nodegroup):
        return self.getGhostStart(nodegroup, 0, 3)

    def getClydeStartNode(self, nodegroup):
        return self.getGhostStart(nodegroup, 4, 3)

    def getGhostStart(self, nodegroup, x, y):
        key = nodegroup.constructKey(*self.addoffset(x, y))
        return nodegroup.nodesLUT[key]

    def getSpawnNode(self, nodegroup):
        spawnkey = nodegroup.constructKey(*self.addoffset(2, 3))
        return nodegroup.nodesLUT[spawnkey]

    def getFruitNode(self, nodegroup):
        key = nodegroup.constructKey(*self.fruitStart)
        return nodegroup.nodesLUT[key]

    def setPortals(self, nodegroup):
        for key in list(self.portalPairs.keys()):
            p1, p2 = self.portalPairs[key]
            nodegroup.setPortalPair(p1, p2)

    def connectHomeNodes(self, nodegroup):
        homekey = nodegroup.createHomeNodes(*self.homeoffset)
        nodegroup.connectHomeNodes(homekey, self.homenodeconnectLeft, LEFT)
        nodegroup.connectHomeNodes(homekey, self.homenodeconnectRight, RIGHT)

    def addoffset(self, x, y):
        return x+self.homeoffset[0], y+self.homeoffset[1]