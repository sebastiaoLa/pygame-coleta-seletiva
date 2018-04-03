from pygame import display
import random

class Batch(object):
    def __init__(self, *args, **kwargs):
        self.rects = []

    def add_to_batch(self,rect):
        self.rects.append(rect)

    def draw(self):
        display.update(self.rects)
        self.rects = []