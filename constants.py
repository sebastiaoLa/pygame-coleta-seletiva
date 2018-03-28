import pygame

#consts :
#	COLORS
RED = (255,000,000)
GREEN = (000,255,000)
BLUE = (000,000,255)
WHITE = (255,255,255)
BLACK = (000,000,000)
BROWN = (139,69,19)
YELLOW = (255,255,0)
PINK = (248,24,148)

# 	TYPES
ORGANICO = 0
METAL = 1
PAPEL = 2
PLASTICO = 3
VIDRO = 4
# SCREEN SIZE

pygame.display.init()
screen = pygame.display.Info()
WIDTH = int(screen.current_w*0.9)
HEIGHT = int(screen.current_h*0.9)


# WIDTH = 800
# HEIGHT = 600