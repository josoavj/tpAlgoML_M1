import pygame
import random
import sys

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sliding Puzzle - Choix de la grille")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (70, 130, 180)
LIGHT_GRAY = (220, 220, 220)


# Police
font = pygame.font.SysFont("Arial", 28)

# Charger une image
IMAGE_PATH = "/run/media/josoa/Files/Dev/Python/tpAlgoML/assets/ISPM.jpg"  # Remplacez par le chemin de votre image
image = pygame.image.load(IMAGE_PATH)

# Options pour les grilles
grid_options = [("3 x 3", 3), ("4 x 4", 4)]  # Taille des grilles disponibles
swap_options = [("0", 0), ("10", 10)]  # Options pour le "Swap"
chosen_grid = None  # Option de grille choisie
chosen_swap = None  # Option de Swap choisie
dropdown_open_grid = False  # État du menu déroulant pour la grille
dropdown_open_swap = False  # État du menu déroulant pour le Swap

def slice_image(image, grid_size):
    """Découpe une image en morceaux pour chaque tuile."""
    image = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    tile_size = SCREEN_WIDTH // grid_size
    pieces = []
    for row in range(grid_size):
        for col in range(grid_size):
            x = col * tile_size
            y = row * tile_size
            piece = image.subsurface((x, y, tile_size, tile_size))
            pieces.append(piece)
    return pieces

# Fonction pour dessiner du texte
def draw_text(text, color, x, y, center=True):
    rendered_text = font.render(text, True, color)
    text_rect = rendered_text.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    screen.blit(rendered_text, text_rect)

# Fonction pour vérifier si une grille est résolvable
def is_solvable(grid):
    """Vérifie si une grille est résolvable en comptant les inversions."""
    flat_grid = [tile for row in grid for tile in row if tile != 0]
    inversions = 0
    for i in range(len(flat_grid)):
        for j in range(i + 1, len(flat_grid)):
            if flat_grid[i] > flat_grid[j]:
                inversions += 1
    return inversions % 2 == 0

# Fonction pour créer une grille aléatoire
def create_puzzle(size):
    tiles = list(range(size * size))
    while True:
        random.shuffle(tiles)
        grid = [tiles[i:i + size] for i in range(0, len(tiles), size)]
        if is_solvable(grid):
            return grid

def draw_rounded_rect(surface, color, rect, border_radius):
    x, y, width, height = rect
    pygame.draw.rect(surface, color, (x + border_radius, y, width - 2 * border_radius, height))  # Rectangle central
    pygame.draw.rect(surface, color, (x, y + border_radius, width, height - 2 * border_radius))  # Rectangle vertical

    # Dessiner les cercles pour les coins
    pygame.draw.circle(surface, color, (x + border_radius, y + border_radius), border_radius)  # Coin supérieur gauche
    pygame.draw.circle(surface, color, (x + width - border_radius, y + border_radius), border_radius)  # Coin supérieur droit
    pygame.draw.circle(surface, color, (x + border_radius, y + height - border_radius), border_radius)  # Coin inférieur gauche
    pygame.draw.circle(surface, color, (x + width - border_radius, y + height - border_radius), border_radius)  # Coin inférieur droit

# Fonction pour dessiner la grille
def draw_grid(grid, pieces, grid_size):
    tile_size = SCREEN_WIDTH // grid_size
    for i, row in enumerate(grid):
        for j, tile in enumerate(row):
            x = j * tile_size
            y = i * tile_size
            if tile != 0:  # Ne pas dessiner l'espace vide
                screen.blit(pieces[tile], (x, y))
            pygame.draw.rect(screen, BLACK, (x, y, tile_size, tile_size), 2)

# Fonction principale
def main():
    global chosen_grid, chosen_swap, dropdown_open_grid, dropdown_open_swap
    running = True
    puzzle = None
    pieces = None
    choosing_grid = True  # Indique si le joueur est en mode choix de grille

    # Bouton Valider avec coins arrondis
    button_rect = (200, 400, 100, 50)  # x, y, largeur, hauteur
    border_radius = 15  # Rayon des coins

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
            draw_text("Choisissez une grille", BLACK, SCREEN_WIDTH // 2, 50)
            pygame.draw.rect(screen, LIGHT_GRAY, (150, 100, 200, 40))
            draw_text(chosen_grid[0] if chosen_grid else "Grille", BLACK, SCREEN_WIDTH // 2, 120)

            if dropdown_open_grid:
                for i, option in enumerate(grid_options):
                    pygame.draw.rect(screen, GRAY, (150, 140 + i * 40, 200, 40))
                    draw_text(option[0], BLACK, SCREEN_WIDTH // 2, 160 + i * 40)

            # Dessiner le menu déroulant pour le Swap
            #draw_text("Choisissez Swap", BLACK, SCREEN_WIDTH // 2, 180)
            pygame.draw.rect(screen, LIGHT_GRAY, (150, 200, 200, 40))
            draw_text(chosen_swap[0] if chosen_swap else "Swap", BLACK, SCREEN_WIDTH // 2, 220)

            if dropdown_open_swap:
                for i, option in enumerate(swap_options):
                    pygame.draw.rect(screen, GRAY, (150, 240 + i * 40, 200, 40))
                    draw_text(option[0], BLACK, SCREEN_WIDTH // 2, 260 + i * 40)

            # Dessiner le bouton
            draw_rounded_rect(screen, BLUE, button_rect, border_radius)

            # Texte du bouton
            draw_text("Valider", WHITE, button_rect[0] + button_rect[2] // 2, button_rect[1] + button_rect[3] // 2)
        else:
            # Afficher la grille
            draw_grid(puzzle, pieces, chosen_grid[1])

        pygame.display.flip()

# Lancer le jeu
if __name__ == "__main__":
    main()
