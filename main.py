import pygame
import random
import sys

# Initialisation de PyGame
pygame.init()

# Entrée des dimensions de la fenêtre
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sliding Puzzle - Choix de la grille du jeux")

