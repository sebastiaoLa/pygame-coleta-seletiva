from pygame import image,Surface
from time import time


class Sprite(object):
    
    def __init__(self,img):
        if isinstance(img,str):
            self.surface = image.load(img)    
        elif isinstance(img,Surface):
            self.surface = img
        else:
            raise(TypeError('should be and path string or pygame.image.load obj'))
        self.rect = self.surface.get_rect()
        self.clicked = False

    def set_center(self,pos):
        self.rect.center = pos
        return self

    def draw(self,disp):
        disp.blit(self.surface,self.rect)

    def move(self,x,y):
        self.rect.center = (self.rect.center[0]+x,self.rect.center[1]+y)

    def get_center(self):
        return {
            'x':self.rect.center[0],
            'y':self.rect.center[1]
            }

    
class tempSprite(Sprite):
    def __init__(self, *args, **kwargs):
        Sprite.__init__(self)
        self.time = 0
        self.count = 0

    def set_time(self,time):
        self.time = time
    
    def start_counter(self):
        self.count = time()

    def check_counter(self):
        # returns when time is over
        if self.count+self.time<time():
            return True
        return False