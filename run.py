import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import GhostGroup
from fruit import Fruit
from pauser import Pause
from text import TextGroup
#from sprites import Spritesheet#####

class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.setBackground()
        self.clock = pygame.time.Clock()
        self.fruit = None
        self.pause = Pause(True)
        self.level = 1
        self.lives = 2
        self.score = 0
        self.textgroup = TextGroup(self.level)
        #self.sheet = Spritesheet()#####

    def setBackground(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    def startGame(self):
        self.nodes = NodeGroup("maze1.txt")
        self.nodes.setPortalPair((0, 17), (27, 17))
        homekey = self.nodes.createHomeNodes(11.5, 14)
        self.nodes.connectHomeNodes(homekey, (12,14), LEFT)
        self.nodes.connectHomeNodes(homekey, (15,14), RIGHT)
        spawnkey = self.nodes.constructKey(2+11.5, 3+14) 
        
        pacstartkey = self.nodes.constructKey(15, 26)
        self.pacman = Pacman(self.nodes.nodesLUT[pacstartkey])

        self.pellets = PelletGroup("maze1_pellets.txt")
        self.ghosts = GhostGroup(self.nodes.getDefaultNode(), self.pacman)
        self.ghosts.setSpawnNode(self.nodes.nodesLUT[spawnkey])

        blinkystartkey = self.nodes.constructKey(2+11.5, 0+14)
        pinkystartkey = self.nodes.constructKey(2+11.5, 3+14)
        inkystartkey = self.nodes.constructKey(0+11.5, 3+14)
        clydestartkey = self.nodes.constructKey(4+11.5, 3+14)
        self.ghosts.blinky.setStartNode(self.nodes.nodesLUT[blinkystartkey])
        self.ghosts.pinky.setStartNode(self.nodes.nodesLUT[pinkystartkey])
        self.ghosts.inky.setStartNode(self.nodes.nodesLUT[inkystartkey])
        self.ghosts.clyde.setStartNode(self.nodes.nodesLUT[clydestartkey])

        self.ghosts.inky.startNode.denyAccess(RIGHT, self.ghosts.inky)
        self.ghosts.clyde.startNode.denyAccess(LEFT, self.ghosts.clyde)

        self.nodes.denyAccess(2+11.5, 0+14, DOWN, self.pacman)
        self.nodes.denyAccessList(2+11.5, 3+14, LEFT, self.ghosts)
        self.nodes.denyAccessList(2+11.5, 3+14, RIGHT, self.ghosts)

        #self.pacman.image = self.sheet.getImage(0, 1, 32, 32)#####Just so as example for section

    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.textgroup.update(dt)
        if not self.pause.paused:
            self.pacman.update(dt)
            self.ghosts.update(dt)
            self.pellets.update(dt)
            if self.fruit is not None:
                self.fruit.update(dt)
            self.checkPelletEvents()
            self.checkGhostEvents()
            self.checkFruitEvents()
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
                    else:
                        self.textgroup.showText(PAUSETXT)

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
                self.pause.setPause(pauseTime=3, func=self.nextLevel)
           
    def checkGhostEvents(self):
        for ghost in self.ghosts:
            if self.pacman.collideGhost(ghost):
                if ghost.mode.current is FREIGHT:
                    self.updateScore(ghost.points)
                    
                    self.textgroup.addText(str(ghost.points), WHITE, ghost.position.x, ghost.position.y, 8, time=1)
                    self.ghosts.updatePoints()
                    self.pause.setPause(pauseTime=1)
                    ghost.startSpawn()
                elif ghost.mode.current is not SPAWN:
                    print("PACMAN DEAD")
                    self.lives -=  1
                    if self.lives <= 0:
                        self.textgroup.showText(GAMEOVERTXT)
                        self.pause.setPause(pauseTime=3, func=self.restartGame)
                    else:
                        self.pause.setPause(pauseTime=3, func=self.resetLevel)
           
    
    def checkFruitEvents(self):
        if self.pellets.numEaten == 50 or self.pellets.numEaten == 140:
            if self.fruit is None:
                nodekey = self.nodes.constructKey(9, 20)
                self.fruit = Fruit(self.nodes.nodesLUT[nodekey])
        if self.fruit is not None:
            if self.pacman.collideCheck(self.fruit):
                
                self.updateScore(self.fruit.points)
                self.textgroup.addText(str(self.fruit.points), WHITE, self.fruit.position.x, self.fruit.position.y, 8, time=1)
                self.fruit = None
                
            elif self.fruit.destroy:
                self.fruit = None

    
    def nextLevel(self):
        self.level += 1
        self.pause.paused = True
        self.startGame()

    
    def restartGame(self):
        print("Restart Game")
        self.lives = 5
        self.level = 1
        self.pause.paused = True
        self.fruit = None
        self.startGame()
        self.textgroup.showText(READYTXT)

    def resetLevel(self):
        print("Reset " + str(self.lives) + " lives left")
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
        self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        if self.fruit is not None:
            self.fruit.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        self.textgroup.render(self.screen)
        pygame.display.update()


if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()
