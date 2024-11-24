import pygame

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sliding Puzzle Game")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (70, 130, 180)
LIGHT_GRAY = (220, 220, 220)
LIGHT_GREEN = (4, 203, 0)
RED = (255, 0, 0)

# Police
font = pygame.font.SysFont("Arial bold", 28)
