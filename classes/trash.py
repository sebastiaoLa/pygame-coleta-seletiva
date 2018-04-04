import pygame

class Trash(object):
    def __init__(self, imgPath, batch=None):
        self.img = pygame.image.load(imgPath)
        self.img = self.img.convert_alpha()
        self.rect = self.img.get_rect()
        self.type = type
        self.in_screen = True
        self.clicked = False
        self.batch = batch
        self.moved = False

    def set_pos(self, pos, coords):
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

    def move_center(self, pos):
        self.rect.center = pos

    def draw(self, surface):
        if self.batch:
            self.batch.add_to_batch(surface.blit(self.img, self.rect))
        else:
            surface.blit(self.img, self.rect)

    def check_collide_rect(self, rect):
        return self.rect.colliderect(rect)

    def check_clicked(self, pos):
        if self.rect.collidepoint(pos):
            self.clicked = True
            return True
        return False
