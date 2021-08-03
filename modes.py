from stack import Stack

class Mode(object):
    def __init__(self, name="", time=None, speedMult=1, direction=None):
        self.name = name
        self.time = time
        self.speedMult = speedMult
        self.direction = direction
        self.timer = 0
        self.started = False
        self.finished = False

    def update(self, dt):
        if self.started:
            self.timer += dt
            if self.time is not None:
                if self.timer >= self.time:
                    self.finished = True

                #self.reverseDirection()
                #self.mode = self.modeStack.pop()
                #self.timer = 0

    


class ModeMachine(object):
    def __init__(self):
        self.modes = Stack()
        self.modes.push(Mode(name="CHASE"))
        self.modes.push(Mode(name="SCATTER", time=5))
        self.modes.push(Mode(name="CHASE", time=20))
        self.modes.push(Mode(name="SCATTER", time=7))
        self.modes.push(Mode(name="CHASE", time=20))
        self.modes.push(Mode(name="SCATTER", time=7))
        self.modes.push(Mode(name="CHASE", time=20))
        self.modes.push(Mode(name="SCATTER", time=7))
        self.mode = modes.pop()

    def update(self, dt):
        if self.mode.finished:
            self.mode = self.modespop()

    def addMode(self, mode):
        pass

