from pygame.font import Font
from constants import RED
from sprite import Sprite

class Text(object):
    def __init__(self, text = None, color = None, batch = None, size = None, background=None):
        self.fontObj = Font('freesansbold.ttf',28 if not size else size)
        self.text = text if text else ""
        self.color = color if color else RED
        self.batch = batch
        self.background = background
        self.sprite = Sprite(self.fontObj.render(self.text,True,self.color,self.background),self.batch)
        self.draw = self.sprite.draw

    def update(self,text):
        self.text = text
        self.sprite.surface = self.fontObj.render(self.text,True,self.color,self.background)

    def set_center(self,x,y = None):
        self.sprite.set_center(x,y)

    def get_rect(self):
        return self.sprite.rect