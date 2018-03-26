import pygame

class Trash(object):
    def __init__(self,imgPath):
        self.img = pygame.image.load(imgPath)
        self.rect = self.img.get_rect()
        self.type = type
        self.in_screen = True
        self.clicked = False

    def set_pos(self,pos,coords):
        if pos == 'CENTER':
            self.rect.center = coords
        elif pos == 'LEFT':
            self.rect.left = coords
        elif pos == 'TOP':
            self.rect.top = coords
        elif pos == 'BOTTOM':
            self.rect.bottom = coords
        elif pos == 'RIGHT':
            self.rect.right = coords
            
    def get_draw_attr(self):
        return self.img,self.rect
    
    def get_clicked(self,pos):
        if self.rect.collidepoint(pos):
            self.clicked = True
            return True
        return False