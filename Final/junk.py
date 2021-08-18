class NodeGroup(object):
    def __init__(self):
        self.nodeList = []

    def setupTestNodes(self):
        nodeA = Node(80 ,80)
        nodeB = Node(160, 80)
        nodeC = Node(80, 160)
        nodeD = Node(160, 160)
        nodeE = Node(208, 160)
        nodeF = Node(80, 320)
        nodeG = Node(208, 320)
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