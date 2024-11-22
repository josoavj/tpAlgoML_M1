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

# Fonction principale
def main():
    global chosen_grid, chosen_swap, dropdown_open_grid, dropdown_open_swap
    running = True
    puzzle = None
    pieces = None
    choosing_grid = True  # Indique si le joueur est en mode choix de grille

    while running:
        screen.fill(GRAY)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if choosing_grid:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos

                    # Ouverture/Fermeture du menu déroulant pour la grille
                    if 150 <= x <= 350 and 100 <= y <= 140:
                        dropdown_open_grid = not dropdown_open_grid
                        dropdown_open_swap = False  # Fermer l'autre menu déroulant

                    # Sélection dans le menu déroulant pour la grille
                    if dropdown_open_grid:
                        for i, option in enumerate(grid_options):
                            if 150 <= x <= 350 and 140 + i * 40 <= y <= 180 + i * 40:
                                chosen_grid = option
                                dropdown_open_grid = False

                    # Ouverture/Fermeture du menu déroulant pour le Swap
                    if 150 <= x <= 350 and 200 <= y <= 240:
                        dropdown_open_swap = not dropdown_open_swap
                        dropdown_open_grid = False  # Fermer l'autre menu déroulant

                    # Sélection dans le menu déroulant pour le Swap
                    if dropdown_open_swap:
                        for i, option in enumerate(swap_options):
                            if 150 <= x <= 350 and 240 + i * 40 <= y <= 280 + i * 40:
                                chosen_swap = option
                                dropdown_open_swap = False

                    # Validation du choix
                    if chosen_grid and chosen_swap and 200 <= x <= 300 and 400 <= y <= 450:
                        grid_size = chosen_grid[1]
                        puzzle = create_puzzle(grid_size)
                        pieces = slice_image(image, grid_size)
                        choosing_grid = False  # Passer en mode jeu

            elif event.type == pygame.KEYDOWN:
                # Gestion des mouvements dans le jeu
                """
                Commandes (Flêches): Déplacement d'un élement proche de la case vide
                  - UP: Case vide vers le haut
                  - DOWN: Case vide vers le bas
                  - LEFT: Case vide vers la gauche
                  - RIGHT: Case vide vers la droite
                """
                grid_size = chosen_grid[1]
                x, y = next((i, j) for i, row in enumerate(puzzle) for j, tile in enumerate(row) if tile == 0)
                if event.key == pygame.K_UP and x < grid_size - 1:
                    puzzle[x][y], puzzle[x + 1][y] = puzzle[x + 1][y], puzzle[x][y]
                elif event.key == pygame.K_DOWN and x > 0:
                    puzzle[x][y], puzzle[x - 1][y] = puzzle[x - 1][y], puzzle[x][y]
                elif event.key == pygame.K_LEFT and y < grid_size - 1:
                    puzzle[x][y], puzzle[x][y + 1] = puzzle[x][y + 1], puzzle[x][y]
                elif event.key == pygame.K_RIGHT and y > 0:
                    puzzle[x][y], puzzle[x][y - 1] = puzzle[x][y - 1], puzzle[x][y]

        if choosing_grid:
            # Dessiner le menu déroulant pour la grille
            ajouttexte("Choisissez une grille", BLACK, SCREEN_WIDTH // 2, 50)
            pygame.draw.rect(ecran, LIGHT_GRAY, (150, 100, 200, 40))
            ajouttexte(chosen_grid[0] if chosen_grid else "Grille", BLACK, SCREEN_WIDTH // 2, 120)

            if dropdown_open_grid:
                for i, option in enumerate(grid_options):
                    pygame.draw.rect(screen, GRAY, (150, 140 + i * 40, 200, 40))
                    ajouttexte(option[0], BLACK, SCREEN_WIDTH // 2, 160 + i * 40)

            # Dessiner le menu déroulant pour le Swap
            #draw_text("Choisissez Swap", BLACK, SCREEN_WIDTH // 2, 180)
            pygame.draw.rect(ecran, LIGHT_GRAY, (150, 200, 200, 40))
            ajouttexte(chosen_swap[0] if chosen_swap else "Swap", BLACK, SCREEN_WIDTH // 2, 220)

            if dropdown_open_swap:
                for i, option in enumerate(swap_options):
                    pygame.draw.rect(ecran, GRAY, (150, 240 + i * 40, 200, 40))
                    ajouttexte(option[0], BLACK, SCREEN_WIDTH // 2, 260 + i * 40)

            # Bouton Valider
            pygame.draw.rect(ecran, BLUE, (200, 400, 100, 50))
            ajouttexte("Valider", WHITE, SCREEN_WIDTH // 2, 425)
        else:
            # Afficher la grille
            dessinergrille(puzzle, pieces, chosen_grid[1])

        pygame.display.flip()

# Lancer le jeu
if __name__ == "__main__":
    main()
