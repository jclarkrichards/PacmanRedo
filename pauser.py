class Pause(object):
    def __init__(self, paused=False):
        self.paused = paused
        self.timer = 0
        self.pauseTime = None
        self.func = None
        
    def update(self, dt):
        if self.pauseTime is not None:
            self.timer += dt
            if self.timer >= self.pauseTime:
                self.timer = 0
                self.paused = False
                self.pauseTime = None
                return self.func
        return None

    def setPause(self, playerPaused=False, pauseTime=None, func=None):
        self.timer = 0
        self.func = func
        self.pauseTime = pauseTime
        #if playerPaused:
        self.flip()

    def flip(self):
        self.paused = not self.paused

    






    """            
    def startTimer(self, pauseTime, pauseType=None):
        self.pauseTime = pauseTime
        self.pauseType = pauseType
        self.timer = 0
        self.paused = True
        
    def player(self):
        self.playerPaused = not self.playerPaused
        if self.playerPaused:
            self.paused = True
        else:
            self.paused = False

    def force(self, pause):
        self.paused = pause
        self.playerPaused = pause
        self.timer = 0
        self.pauseTime = 0

    def settlePause(self, gamecontroller):
        if self.pauseType == "die":
            gamecontroller.resolveDeath()
        elif self.pauseType == "clear":
            gamecontroller.resolveLevelClear()
    """