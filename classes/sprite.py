from pygame import image, Surface, Rect


class Sprite(object):
    def __init__(self, img, batch=None):
        if isinstance(img, str):
            self.surface = image.load(img)
        elif isinstance(img, Surface):
            self.surface = img
        else:
            raise TypeError('should be and path string or pygame.image.load obj')
        self.rect = self.surface.get_rect()
        self.clicked = False
        self.batch = batch

    def set_center(self, x_pos, y_pos=None):
        if y_pos:
            self.rect.center = (x_pos, y_pos)
        else:
            self.rect.center = x_pos
        return self

    def draw(self, disp):
        if self.batch:
            self.batch.add_to_batch(disp.blit(self.surface, self.rect))
        else:
            disp.blit(self.surface, self.rect)

    def move(self, x_pos, y_pos):
        self.rect.center = (self.rect.center[0]+x_pos, self.rect.center[1]+y_pos)

    def get_center(self):
        return {
            'x':self.rect.center[0],
            'y':self.rect.center[1]
            }

    def check_collide(self, arg):
        if isinstance(arg, Rect):
            return self.rect.colliderect(arg)
        return self.rect.collidepoint(arg)
