import pygame
import random
import sys
from creationPuzzle import creation_puzzle
from ajoutTexte import ajouttexte
from creationGrille import dessinergrille

# Initialisation de PyGame
pygame.init()

# Entrée des dimensions de la fenêtre
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
ecran = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sliding Puzzle - Choix de la grille du jeux")

# UI - Interface Utilisateur
# Initialisation des couleurs à utiliser
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (70, 130, 180)


# Police: Modification de la police pour l'ensemble des interfaces
font = pygame.font.SysFont("Arial", 20)


def main():
    # État de choix de la grille
    choosing_grid = True
    grid_size = None
    puzzle = []

    while True:
        ecran.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and choosing_grid:
                x, y = event.pos
                # Vérification des boutons
                if 150 <= x <= 350 and 200 <= y <= 260:  # Bouton 3x3
                    grid_size = 3
                    choosing_grid = False
                    puzzle = creation_puzzle(grid_size)
                elif 150 <= x <= 350 and 300 <= y <= 360:  # Bouton 4x4
                    grid_size = 4
                    choosing_grid = False
                    puzzle = creation_puzzle(grid_size)

            if event.type == pygame.KEYDOWN and not choosing_grid:
                # Gestion des mouvements dans le jeu
                x, y = next((i, j) for i, row in enumerate(puzzle) for j, tile in enumerate(row) if tile == 0)
                if event.key == pygame.K_UP and x < grid_size - 1:
                    puzzle[x][y], puzzle[x + 1][y] = puzzle[x + 1][y], puzzle[x][y]
                elif event.key == pygame.K_DOWN and x > 0:
                    puzzle[x][y], puzzle[x - 1][y] = puzzle[x - 1][y], puzzle[x][y]
                elif event.key == pygame.K_LEFT and y < grid_size - 1:
                    puzzle[x][y], puzzle[x][y + 1] = puzzle[x][y + 1], puzzle[x][y]
                elif event.key == pygame.K_RIGHT and y > 0:
                    puzzle[x][y], puzzle[x][y - 1] = puzzle[x][y - 1], puzzle[x][y]

        # Interface de choix de la grille
        if choosing_grid:
            ajouttexte(ecran, font, "Choisissez une grille", BLACK, SCREEN_WIDTH // 2, 100)
            pygame.draw.rect(ecran, GRAY, (150, 200, 200, 60))
            pygame.draw.rect(ecran, GRAY, (150, 300, 200, 60))
            ajouttexte(ecran, font, "Entrez un chiffre pour avoir un swap", BLACK, SCREEN_WIDTH // 2, 150)
            ajouttexte(ecran, font, "3 x 3", BLACK, SCREEN_WIDTH // 2, 230)
            ajouttexte(ecran, font, "4 x 4", BLACK, SCREEN_WIDTH // 2, 330)
        else:
            dessinergrille(ecran, SCREEN_WIDTH, font, puzzle, grid_size)

        pygame.display.flip()

# Lancer le jeu


if __name__ == "__main__":
    main()
