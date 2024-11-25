import pygame

from afficheAlert import draw_alert_box
from ajoutTexte import draw_text
from config import *
from creationGrilleRand import create_puzzle, draw_grid
from decoupeImage import slice_image

# Charger les images
BACKGROUND_PATH = "assets/Main.png"  # Image de fond pour le menu
IMAGE_PATH = "assets/pixelcut-export (1).png"  # Image pour le puzzle
BACKGROUND_PATH2 = "assets/Main 2.png"  # Image de fond pour le menu

try:
    background_image = pygame.image.load(BACKGROUND_PATH)
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    puzzle_image = pygame.image.load(IMAGE_PATH)
except pygame.error as e:
    print(f"Erreur de chargement des images : {e}")
    pygame.quit()
    exit()

try:
    background_image2 = pygame.image.load(BACKGROUND_PATH2)
    background_image2 = pygame.transform.scale(background_image2, (SCREEN_WIDTH, SCREEN_HEIGHT))
    puzzle_image = pygame.image.load(IMAGE_PATH)
except pygame.error as e:
    print(f"Erreur de chargement des images : {e}")
    pygame.quit()
    exit()

# Options pour les grilles
grid_options = [("3 x 3", 3), ("4 x 4", 4)]
swap_options = [("0", 0), ("4", 4), ("10", 10)]


def draw_rounded_rect(surface, color, rect, border_radius):
    x, y, width, height = rect
    pygame.draw.rect(surface, color, (x + border_radius, y, width - 2 * border_radius, height))  # Rectangle central
    pygame.draw.rect(surface, color, (x, y + border_radius, width, height - 2 * border_radius))  # Rectangle vertical

    # Dessiner les cercles pour les coins
    pygame.draw.circle(surface, color, (x + border_radius, y + border_radius), border_radius)  # Coin supérieur gauche
    pygame.draw.circle(surface, color, (x + width - border_radius, y + border_radius), border_radius)  # Coin supérieur droit
    pygame.draw.circle(surface, color, (x + border_radius, y + height - border_radius), border_radius)  # Coin inférieur gauche
    pygame.draw.circle(surface, color, (x + width - border_radius, y + height - border_radius), border_radius)  # Coin inférieur droit

# Bouton avec coins arrondis

button_rect = (200, 400, 100, 50)  # x, y, largeur, hauteur
border_radius = 15  # Rayon des coins

# Variables globales
chosen_grid = None
chosen_swap = None
dropdown_open_grid = False
dropdown_open_swap = False
swap_available = False
show_alert = False
swap_mode = False

global move_count
move_count = 0

def move_tile(grid, direction):
    # global move_count, swap_available, show_alert

    global move_count, swap_available, show_alert

    size = len(grid)
    empty_x, empty_y = [(x, y) for x in range(size) for y in range(size) if grid[x][y] == 0][0]

    moved = False
    if direction == "UP" and empty_x < size - 1:
        grid[empty_x][empty_y], grid[empty_x + 1][empty_y] = grid[empty_x + 1][empty_y], grid[empty_x][empty_y]
        moved = True
    elif direction == "DOWN" and empty_x > 0:
        grid[empty_x][empty_y], grid[empty_x - 1][empty_y] = grid[empty_x - 1][empty_y], grid[empty_x][empty_y]
        moved = True
    elif direction == "LEFT" and empty_y < size - 1:
        grid[empty_x][empty_y], grid[empty_x][empty_y + 1] = grid[empty_x][empty_y + 1], grid[empty_x][empty_y]
        moved = True
    elif direction == "RIGHT" and empty_y > 0:
        grid[empty_x][empty_y], grid[empty_x][empty_y - 1] = grid[empty_x][empty_y - 1], grid[empty_x][empty_y]
        moved = True

    if moved:
        move_count += 1
        if chosen_swap[1] > 0 and move_count % chosen_swap[1] == 0:
            swap_available = True
            show_alert = True

# Fonction pour échanger les tuiles


def perfomr_swap(puzzle, selected_tiles):
    if len(selected_tiles) == 2:
        pos1, pos2 = selected_tiles
        puzzle[pos1[0]][pos1[1]], puzzle[pos2[0]][pos2[1]] = puzzle[pos2[0]][pos2[1]], puzzle[pos1[0]][pos1[1]]
        return True
    return False

# Fonction de sélection tuiles


def get_tile_clicked(pos, grid_size):
    tile_size = SCREEN_WIDTH // grid_size
    x, y = pos
    row = y // tile_size
    col = x // tile_size
    return row, col


# Fonction principale
def main():
    global chosen_grid, chosen_swap, dropdown_open_grid, dropdown_open_swap, show_alert, swap_available
    global swap_mode, selected_tiles
    selected_tiles = []
    running = True
    puzzle = None
    pieces = None
    current_screen = "menu"

    while running:
        screen.fill(GRAY)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if current_screen == "menu":
                    if play_button_rect.collidepoint(event.pos):
                        current_screen = "options"
                elif current_screen == "options":
                    x, y = event.pos
                    if 150 <= x <= 350 and 100 <= y <= 140:
                        dropdown_open_grid = not dropdown_open_grid
                        dropdown_open_swap = False
                    elif dropdown_open_grid:
                        for i, option in enumerate(grid_options):
                            if 150 <= x <= 350 and 140 + i * 40 <= y <= 180 + i * 40:
                                chosen_grid = option
                                dropdown_open_grid = False
                    elif 150 <= x <= 350 and 200 <= y <= 240:
                        dropdown_open_swap = not dropdown_open_swap
                        dropdown_open_grid = False
                    elif dropdown_open_swap:
                        for i, option in enumerate(swap_options):
                            if 150 <= x <= 350 and 240 + i * 40 <= y <= 280 + i * 40:
                                chosen_swap = option
                                dropdown_open_swap = False
                    if chosen_grid and chosen_swap and 200 <= x <= 300 and 400 <= y <= 450:
                        grid_size = chosen_grid[1]
                        puzzle = create_puzzle(grid_size)
                        pieces = slice_image(puzzle_image, grid_size)
                        current_screen = "game"
                # Gestion de l'alerte box
                elif show_alert:
                    x,y = event.pos
                    ok_button_rect, close_button_rect = draw_alert_box()
                    if ok_button_rect.collidepoint(x,y):
                        show_alert = False
                        swap_mode = True
                    elif close_button_rect.collidepoint(x,y):
                        show_alert = False

                # échange tuiles
                elif swap_mode and current_screen == "game":
                    tile_clicked = get_tile_clicked(event.pos, chosen_grid[1])
                    if tile_clicked not in selected_tiles:
                        selected_tiles.append(tile_clicked)
                    if len(selected_tiles) == 2:
                        if perfomr_swap(puzzle, selected_tiles):
                            swap_mode = False
                            selected_tiles = []
            elif event.type == pygame.KEYDOWN and current_screen == "game":
                if event.key == pygame.K_UP:
                    move_tile(puzzle, "UP")
                elif event.key == pygame.K_DOWN:
                    move_tile(puzzle, "DOWN")
                elif event.key == pygame.K_LEFT:
                    move_tile(puzzle, "LEFT")
                elif event.key == pygame.K_RIGHT:
                    move_tile(puzzle, "RIGHT")
            elif event.type == pygame.MOUSEBUTTONDOWN and show_alert:
                x, y = event.pos
                if 100 <= x <= 400 and 150 <= y <= 350:
                    # Envoie une alerte
                    show_alert = False
                    swap_available = False
        if current_screen == "menu":
            screen.blit(background_image, (0, 0))
            play_button_rect = pygame.Rect(150, 400, 200, 50)

            # Bouton play
            # Dessiner le bouton
            draw_rounded_rect(screen, LIGHT_GREEN, button_rect, border_radius)
            # Texte du bouton
            draw_text("PLAY", WHITE, button_rect[0] + button_rect[2] // 2, button_rect[1] + button_rect[3] // 2)

        elif current_screen == "options":
            screen.blit(background_image2, (0, 0))
            draw_text("Choisissez vos options", WHITE, SCREEN_WIDTH // 2, 50)

            # Bouton grille
            pygame.Rect(150, 100, 200, 40)
            # Dessiner le bouton
            draw_rounded_rect(screen, LIGHT_GREEN, button_rect, border_radius)

            draw_text(chosen_grid[0] if chosen_grid else "Grille +", WHITE, SCREEN_WIDTH // 2, 120)
            if dropdown_open_grid:
                for i, option in enumerate(grid_options):
                    pygame.Rect(150, 140 + i * 40, 200, 40)
                    # Dessiner le bouton
                    draw_rounded_rect(screen, LIGHT_GREEN, button_rect, border_radius)
                    draw_text(option[0], BLUE, SCREEN_WIDTH // 2, 160 + i * 40)
            pygame.Rect(150, 200, 200, 40)
            # Dessiner le bouton
            draw_rounded_rect(screen, LIGHT_GREEN, button_rect, border_radius)

            draw_text(chosen_swap[0] if chosen_swap else "Swap +", WHITE, SCREEN_WIDTH // 2, 220)
            if dropdown_open_swap:
                for i, option in enumerate(swap_options):
                    pygame.Rect(150, 240 + i * 40, 200, 40)
                    # Dessiner le bouton
                    draw_rounded_rect(screen, LIGHT_GREEN, button_rect, border_radius)
                    draw_text(option[0], BLUE, SCREEN_WIDTH // 2, 260 + i * 40)
            validate_button_rect = pygame.Rect(200, 400, 100, 50)
            # Bouton valider

            # Dessiner le bouton
            draw_rounded_rect(screen, BLUE, button_rect, border_radius)
            # Texte du bouton
            draw_text("Valider", WHITE, button_rect[0] + button_rect[2] // 2, button_rect[1] + button_rect[3] // 2)

        elif current_screen == "game":
            draw_grid(puzzle, pieces, chosen_grid[1])
            draw_text(f"Déplacements : {move_count}", BLUE, 50, 10, center=False)
            if show_alert:
                draw_alert_box()
            elif swap_mode:
                draw_text("Mode Swap activé: Cliquez sur 2 tuiles", RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)

        pygame.display.flip()

    pygame.quit()


# Lancer le jeu
if __name__ == "__main__":
    main()
