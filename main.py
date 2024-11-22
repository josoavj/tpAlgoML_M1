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

# UI - Interface Utilisateur
# Initialisation des couleurs à utiliser
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (70, 130, 180)


# Police: Modification de la police pour l'ensemble des interfaces
font = pygame.font.SysFont("Poppins", 40)

# Lancement du Jeu
if __name__ == "__main__":
#    main()