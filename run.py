import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import Ghost

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
        print(list(self.nodes.nodesLUT.keys()))
        spawnkey = self.nodes.constructKey(2+11.5, 3+14)     
        self.pacman = Pacman(self.nodes.getPacmanNode())
        self.pellets = PelletGroup("maze1_pellets.txt")
        self.ghost = Ghost(self.nodes.getPacmanNode(), self.pacman)
        self.ghost.setSpawnNode(self.nodes.nodesLUT[spawnkey])

    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.pacman.update(dt)
        self.ghost.update(dt)
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
            self.pellets.pelletList.remove(pellet)
            if pellet.name == "powerpellet":
                self.ghost.startFreight()
           
    def checkGhostEvents(self):
        if self.pacman.collideGhost(self.ghost):
            if self.ghost.mode.current is FREIGHT:
                self.ghost.startSpawn()
           
                
                
    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        self.pacman.render(self.screen)
        self.ghost.render(self.screen)
        pygame.display.update()


if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()
