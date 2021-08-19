    def checkGhostEvents(self):
        for ghost in self.ghosts:
            if self.pacman.collideGhost(ghost):
                if ghost.mode.current is FREIGHT:
                    self.pacman.visible = False
                    ghost.visible = False
                    self.pause.setPause(pauseTime=1, func=self.showEntities)
                    ghost.startSpawn()
                #newtext::elif ghost.mode.current is not SPAWN:
                     #newtext::if self.pacman.alive:
                         #newtext::self.lives -=  1
                         #newtext::self.pacman.die()               
                         #newtext::self.ghosts.hide()
                         #newtext::if self.lives <= 0:
                             #newtext::self.pause.setPause(pauseTime=3, func=self.restartGame)
                         #newtext::else:
                             #newtext::self.pause.setPause(pauseTime=3, func=self.resetLevel)