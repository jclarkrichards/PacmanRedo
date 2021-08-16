from vector import Vector2


class Maze1(object):
    def __init__(self):
        self.name = "maze1"
        self.portalPairs = {0:((0, 27), (17, 27))}
        self.homeoffset = (11.5, 14)
        self.homenodeconnectLeft = (12, 14)
        self.homenodeconnectRight = (15, 14)
        self.pacmanStart = (15, 26)
        self.ghostNodeDeny = {UP:((12, 14), (15, 14), (12, 26), (15, 26))}




class MazeController(object):
    def __init__(self):
        self.mazedict = {0:Maze1}

    def loadMaze(self, level):
        return self.mazedict[level%len(self.mazedict)]()

