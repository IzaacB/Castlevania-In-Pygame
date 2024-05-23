import pygame
import numpy as np
import copy

#Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

#Window properties.
window_width = 256
window_height = 224

refresh = pygame.time.Clock()
refresh_rate = 60