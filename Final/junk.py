def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.pellets.numEaten += 1
            self.pellets.pelletList.remove(pellet)
            #newtext::if pellet.name == POWERPELLET:
                #newtext::self.ghosts.startFreight()