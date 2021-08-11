import pygame
from vector import Vector2
from constants import *

class Text(object):
    def __init__(self, text, color, x, y, size, time=None, id=None, visible=True):
        self.id = id
        self.text = text
        self.color = color
        self.size = size
        self.visible = visible
        self.position = Vector2(x, y)
        self.timer = 0
        self.lifespan = time
        self.label = None
        self.destroy = False
        self.setupFont("PressStart2P-Regular.ttf")
        self.createLabel()

    def setupFont(self, fontpath):
        self.font = pygame.font.Font(fontpath, self.size)

    def createLabel(self):
        self.label = self.font.render(self.text, 1, self.color)

    def setText(self, newtext):
        self.text = str(newtext)
        self.createLabel()

    def update(self, dt):
        if self.lifespan is not None:
            self.timer += dt
            if self.timer >= self.lifespan:
                self.timer = 0
                self.lifespan = None
                self.destroy = True

    def render(self, screen):
        if self.visible:
            x, y = self.position.asTuple()
            screen.blit(self.label, (x, y))


class TextGroup(object):
    def __init__(self, level):
        self.nextid = 1  #Because SCORETXT is 0 and LEVELTXT is 1
        self.level = level
        self.alltext = {}
        self.setupText()
        self.showText(READYTXT)

    def addText(self, text, color, x, y, size, time=None, id=None):
        self.nextid += 10
        self.alltext[self.nextid] = Text(text, color, x, y, size, time=time, id=id)
        return self.nextid

    def removeText(self, id):
        self.alltext.pop(id)
        
    def setupText(self):
        self.alltext[SCORETXT] = Text("0".zfill(8), WHITE, 0, 16, 16)
        self.alltext[LEVELTXT] = Text(str(self.level).zfill(3), WHITE, 368, 16, 16)
        self.alltext[READYTXT] = Text("READY!", YELLOW, 180, 320, 16, visible=False)
        self.alltext[PAUSETXT] = Text("PAUSED!", YELLOW, 170, 320, 16, visible=False)
        self.alltext[GAMEOVERTXT] = Text("GAMEOVER!", YELLOW, 160, 320, 16, visible=False)
        self.addText("SCORE", WHITE, 0, 0, 16)
        self.addText("LEVEL", WHITE, 368, 0, 16)

    def update(self, dt):
        for tkey in list(self.alltext.keys()):
            self.alltext[tkey].update(dt)
            if self.alltext[tkey].destroy:
                self.removeText(tkey)

    def showText(self, id):
        self.hideText()
        self.alltext[id].visible = True

    def hideText(self):
        self.alltext[READYTXT].visible = False
        self.alltext[PAUSETXT].visible = False
        self.alltext[GAMEOVERTXT].visible = False

    def updateScore(self, score):
        self.updateText(SCORETXT, str(score).zfill(8))

    def updateText(self, id, value):
        if id in self.alltext.keys():
            self.alltext[id].setText(value)

    def render(self, screen):
        for tkey in list(self.alltext.keys()):
            self.alltext[tkey].render(screen)
     