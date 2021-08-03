from stack import Stack
from constants import *


class WorldMode(object):
    def __init__(self):
        self.timer = 0
        self.scatterMode()

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.time:
            if self.mode is SCATTER:
                self.chaseMode()
            elif self.mode is CHASE:
                self.scatterMode()

    def scatterMode(self):
        self.mode = SCATTER
        self.time = 7
        self.timer = 0

    def chaseMode(self):
        self.mode = CHASE
        self.time = 20
        self.timer = 0

          

    


class ModeMachine(object):
    def __init__(self):
        self.modes = Stack()
        #self.modes.push(SCATTER, time=7)
        #self.current = self.modes.peek()
        #self.scatter = {time:7}
        #self.chase = {time:20}
        #self.modes.push(Mode(name="CHASE"))
        #self.modes.push(Mode(name="SCATTER", time=5))
        #self.modes.push(Mode(name="CHASE", time=20))
        #self.modes.push(Mode(name="SCATTER", time=7))
        #self.modes.push(Mode(name="CHASE", time=20))
        #self.modes.push(Mode(name="SCATTER", time=7))
        #self.modes.push(Mode(name="CHASE", time=20))
        #self.modes.push(Mode(name="SCATTER", time=7))
        #self.mode = modes.pop()

    def update(self, dt):
        #if self.current is not None:
        self.current.udpate(dt)


    def setMode(self, mode):
        pass

