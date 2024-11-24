# Fonction pour découper une image en morceaux
import pygame

from main import SCREEN_WIDTH, SCREEN_HEIGHT


def slice_image(image, grid_size):
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
