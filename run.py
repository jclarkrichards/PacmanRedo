import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import GhostGroup

class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.setBackground()
        self.clock = pygame.time.Clock()

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

        print("Inky")
        print(self.ghosts.inky.startNode.position.asTuple())
        print(inkystartkey)
        self.ghosts.inky.startNode.denyAccess(RIGHT, self.ghosts.inky)
        self.ghosts.clyde.startNode.denyAccess(LEFT, self.ghosts.clyde)

        self.nodes.denyAccess(2+11.5, 0+14, DOWN, self.pacman)
        self.nodes.denyAccessList(2+11.5, 3+14, LEFT, self.ghosts)
        self.nodes.denyAccessList(2+11.5, 3+14, RIGHT, self.ghosts)

    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.pacman.update(dt)
        self.ghosts.update(dt)
        self.pellets.update(dt)
        self.checkPelletEvents()
        self.checkGhostEvents()
        self.checkEvents()
        self.render()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.pellets.numEaten += 1
            if self.pellets.numEaten == 30:
                self.ghosts.inky.startNode.allowAccess(RIGHT, self.ghosts.inky)
            if self.pellets.numEaten == 70:
                self.ghosts.clyde.startNode.allowAccess(LEFT, self.ghosts.clyde)
            self.pellets.pelletList.remove(pellet)
            if pellet.name is POWERPELLET:
                self.ghosts.startFreight()
           
    def checkGhostEvents(self):
        for ghost in self.ghosts:
            if self.pacman.collideGhost(ghost):
                if ghost.mode.current is FREIGHT:
                    ghost.startSpawn()
           
                
                
    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        pygame.display.update()


if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()
