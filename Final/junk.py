...
#strikeout::from ghosts import Ghost
#newtext::from ghosts import GhostGroup

class GameController(object):

    def startGame(self):
        ...
        #strikeout::self.ghost = Ghost(self.nodes.getStartTempNode(), self.pacman)
        #newtext::self.ghosts = GhostGroup(self.nodes.getPacmanNode(), self.pacman)
        spawnkey = self.nodes.constructKey(2+11.5, 3+14)
        #strikeout::self.ghost.setSpawnNode(self.nodes.nodesLUT[spawnkey])     
        #newtext::self.ghosts.setSpawnNode(self.nodes.nodesLUT[spawnkey])

    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.pacman.update(dt)
        #strikeout::self.ghost.update(dt)
        #newtext::self.ghosts.update(dt)
        ...

    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.pellets.pelletList.remove(pellet)
            if pellet.name is POWERPELLET:
                #strikeout::self.ghost.startFreight()
                #newtext::self.ghosts.startFreight()
           
    def checkGhostEvents(self):
        #newtext::for ghost in self.ghosts:
            #strikeout::if self.pacman.collideGhost(self.ghost):
            #newtext::if self.pacman.collideGhost(ghost):
                #strikeout::if self.ghost.mode.current is FREIGHT:
                #newtext::if ghost.mode.current is FREIGHT:
                    #strikeout::self.ghost.startSpawn()
                    #newtext::ghost.startSpawn()
                          
    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        self.pacman.render(self.screen)
        #strikeout::self.ghost.render(self.screen)
        #newtext::self.ghosts.render(self.screen)
        pygame.display.update()