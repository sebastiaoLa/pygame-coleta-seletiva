from pygame.font import Font
from constants import RED
from sprite import Sprite

class Text(object):
    def __init__(self,text = None,color = None,batch = None):
        self.fontObj = Font('freesansbold.ttf', 28)
        self.text = text if text else ""
        self.color = color if color else RED
        self.sprite = Sprite(self.fontObj.render(self.text,True,self.color),batch)
        self.draw = self.sprite.draw

    def update(self,text):
        self.text = text

    def set_center(self,x,y = None):
        self.sprite.set_center(x,y)

    def get_rect(self):
        return self.sprite.rect