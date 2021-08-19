import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import GhostGroup
from fruit import Fruit, FruitMover
from pauser import Pause
from text import TextGroup
from sprites import LifeSprites
from sprites import MazeSprites
from mazes import MazeController########

class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.background_norm = None
        self.background_flash = None
        self.clock = pygame.time.Clock()
        self.fruit = None
        self.pause = Pause(True)
        self.level = 0
        self.lives = 5
        self.score = 0
        self.textgroup = TextGroup()
        self.lifesprites = LifeSprites(self.lives)
        self.flashBG = False
        self.flashTime = 0.2
        self.flashTimer = 0
        self.fruitNode = None######
        self.maze = MazeController()#######
        self.fruitCaptured = []

    def setBackground(self):
        self.background_norm = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_norm.fill(BLACK)
        self.background_flash = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_flash.fill(BLACK)

    def startGame(self):
        self.setBackground()
        maze = self.maze.loadMaze(self.level)#####

        self.nodes = NodeGroup(maze.name+".txt")#####
        maze.connectHomeNodes(self.nodes)#####


        #self.nodes.setPortalPair((0, 17), (27, 17))
        #homekey = self.nodes.createHomeNodes(11.5, 14)
        #self.nodes.connectHomeNodes(homekey, (12,14), LEFT)
        #self.nodes.connectHomeNodes(homekey, (15,14), RIGHT)
        #spawnkey = self.nodes.constructKey(2+11.5, 3+14) 
        #print("SPWN KEY")
        #print(spawnkey)
        
        #pacstartkey = self.nodes.constructKey(15, 26)
        pacnode = maze.getPacmanStartNode(self.nodes)######
        self.pacman = Pacman(pacnode)######

        self.pellets = PelletGroup(maze.name+".txt")####
        #self.ghosts = GhostGroup(self.nodes.getDefaultNode(), self.pacman)
        self.ghosts = GhostGroup(self.nodes.nodesLUT[self.nodes.homekey], self.pacman)####
        spawnnode = maze.getSpawnNode(self.nodes)#####
        self.ghosts.setSpawnNode(spawnnode)####

        maze.setup(self.nodes, self.pacman, self.ghosts)#######



        #blinkystartkey = self.nodes.constructKey(2+11.5, 0+14)
        #pinkystartkey = self.nodes.constructKey(2+11.5, 3+14)
        #inkystartkey = self.nodes.constructKey(0+11.5, 3+14)
        #clydestartkey = self.nodes.constructKey(4+11.5, 3+14)
        blinkynode = maze.getBlinkyStartNode(self.nodes)####
        pinkynode = maze.getPinkyStartNode(self.nodes)####
        inkynode = maze.getInkyStartNode(self.nodes)####
        clydenode = maze.getClydeStartNode(self.nodes)####

        self.ghosts.blinky.setStartNode(blinkynode)#####
        self.ghosts.pinky.setStartNode(pinkynode)###
        self.ghosts.inky.setStartNode(inkynode)###
        self.ghosts.clyde.setStartNode(clydenode)####

        self.ghosts.inky.startNode.denyAccess(RIGHT, self.ghosts.inky)
        self.ghosts.clyde.startNode.denyAccess(LEFT, self.ghosts.clyde)

        #self.nodes.denyAccess(2+11.5, 0+14, DOWN, self.pacman)
        #self.nodes.denyAccessList(2+11.5, 3+14, LEFT, self.ghosts)
        #self.nodes.denyAccessList(2+11.5, 3+14, RIGHT, self.ghosts)

        #self.nodes.denyAccessList(12, 14, UP, self.ghosts)
        #self.nodes.denyAccessList(15, 14, UP, self.ghosts)
        #self.nodes.denyAccessList(12, 26, UP, self.ghosts)
        #self.nodes.denyAccessList(15, 26, UP, self.ghosts)
        #self.nodes.denyAccessList(13.5, 14, DOWN, self.ghosts)#####

        self.fruitNode = maze.getFruitNode(self.nodes)#####

        self.mazesprites = MazeSprites(maze.name+".txt", maze.name+"_rotation.txt")######
        self.background_norm = self.mazesprites.constructBackground(self.background_norm, self.level%5)
        self.background_flash = self.mazesprites.constructBackground(self.background_flash, 5)
        self.background = self.background_norm
        self.flashBG = False

    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.textgroup.update(dt)
        self.pellets.update(dt)
        if not self.pause.paused:
            self.ghosts.update(dt)         
            if self.fruit is not None:
                self.fruit.update(dt)
            self.checkPelletEvents()
            self.checkGhostEvents()
            self.checkFruitEvents()

        if self.pacman.alive:
            if not self.pause.paused:
                self.pacman.update(dt)
        else:
            self.pacman.update(dt)

        if self.flashBG:
            self.flashTimer += dt
            if self.flashTimer >= self.flashTime:
                self.flashTimer = 0
                if self.background == self.background_norm:
                    self.background = self.background_flash
                else:
                    self.background = self.background_norm

        afterPauseMethod = self.pause.update(dt)
        if afterPauseMethod is not None:
            afterPauseMethod()
        self.checkEvents()
        self.render()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.pause.setPause(playerPaused=True)
                    if not self.pause.paused:
                        self.textgroup.hideText()
                        self.pacman.visible = True
                        self.ghosts.show()
                    else:
                        self.textgroup.showText(PAUSETXT)
                        self.pacman.visible = False
                        self.ghosts.hide()

    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.updateScore(pellet.points)
            self.pellets.numEaten += 1
            if self.pellets.numEaten == 30:
                self.ghosts.inky.startNode.allowAccess(RIGHT, self.ghosts.inky)
            if self.pellets.numEaten == 70:
                self.ghosts.clyde.startNode.allowAccess(LEFT, self.ghosts.clyde)

            self.pellets.pelletList.remove(pellet)
            if pellet.name is POWERPELLET:
                self.ghosts.startFreight()
             

            if self.pellets.isEmpty():
                self.flashBG = True
                self.pause.setPause(pauseTime=3, func=self.nextLevel)
           
    def checkGhostEvents(self):
        for ghost in self.ghosts:
            if self.pacman.collideGhost(ghost):
                if ghost.mode.current is FREIGHT:
                    self.updateScore(ghost.points)                  
                    self.textgroup.addText(str(ghost.points), WHITE, ghost.position.x, ghost.position.y, 8, time=1)
                    self.ghosts.updatePoints()
                    self.pacman.visible = False
                    ghost.visible = False
                    self.pause.setPause(pauseTime=1, func=self.showEntities)
                    ghost.startSpawn()
                    self.nodes.allowHomeAccess(ghost)

                elif ghost.mode.current is not SPAWN:
                    if self.pacman.alive:
                        self.lives -=  1
                        self.pacman.die()               
                        self.ghosts.hide()

                        self.lifesprites.removeImage()
                        if self.lives <= 0:
                            self.textgroup.showText(GAMEOVERTXT)
                            self.pause.setPause(pauseTime=3, func=self.restartGame)
                        else:
                            self.pause.setPause(pauseTime=3, func=self.resetLevel)
           
    
    def checkFruitEvents(self):
        if self.pellets.numEaten == 50 or self.pellets.numEaten == 140:
            if self.fruit is None:
                #nodekey = self.nodes.constructKey(9, 20)
                #self.fruit = Fruit(self.nodes.nodesLUT[nodekey])
                #self.fruit = Fruit(self.fruitNode, self.level)######Normal one
                startnode = self.nodes.getNodeFromTiles(0, 17)
                endnode = self.nodes.getNodeFromTiles(27, 17)
                if startnode is not None and endnode is not None:
                    self.fruit = FruitMover(startnode, endnode, self.level)
                else:
                    print("START node = " + str(startnode))
                    print("END node = " + str(endnode))

        if self.fruit is not None:
            if self.pacman.collideCheck(self.fruit):
                
                self.updateScore(self.fruit.points)
                self.textgroup.addText(str(self.fruit.points), WHITE, self.fruit.position.x, self.fruit.position.y, 8, time=1)
               
                fruitCaptured = False
                for fruit in self.fruitCaptured:
                    if fruit.get_offset() == self.fruit.image.get_offset():
                        fruitCaptured = True
                        break
                if not fruitCaptured:
                    self.fruitCaptured.append(self.fruit.image)
               
                self.fruit = None
                
            elif self.fruit.destroy:
                self.fruit = None

    def showEntities(self):
        self.pacman.visible = True
        self.ghosts.show()
    
    def nextLevel(self):
        self.level += 1
        self.pause.paused = True
        self.startGame()
        self.textgroup.updateLevel(self.level)

    
    def restartGame(self):
        self.lives = 5
        self.level = 0
        self.textgroup.updateLevel(self.level)
        self.score = 0
        self.textgroup.updateScore(self.score)
        self.fruitCaptured = []
        self.pause.paused = True
        self.fruit = None
        self.startGame()
        self.textgroup.showText(READYTXT)
        self.lifesprites.resetLives(self.lives)

    def resetLevel(self):
        self.pause.paused = True
        self.pacman.reset()
        self.ghosts.reset()
        self.fruit = None
        self.textgroup.showText(READYTXT)

    
    def updateScore(self, points):
        self.score += points
        self.textgroup.updateScore(self.score)
    
    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.pellets.render(self.screen)
        if self.fruit is not None:
            self.fruit.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        self.textgroup.render(self.screen)

        for i in range(len(self.lifesprites.images)):
            x = self.lifesprites.images[i].get_width() * i
            y = SCREENHEIGHT - self.lifesprites.images[i].get_height()
            self.screen.blit(self.lifesprites.images[i], (x, y))

        for i in range(len(self.fruitCaptured)):
            x = SCREENWIDTH - self.fruitCaptured[i].get_width() * (i+1)
            y = SCREENHEIGHT - self.fruitCaptured[i].get_height()
            self.screen.blit(self.fruitCaptured[i], (x, y))

        pygame.display.update()


if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()
