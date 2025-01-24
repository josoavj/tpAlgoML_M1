import random

import pygame

from config import *
from testResolutionPuzzle import is_solvable

# Variable
selected_tiles = []

# Fonction pour créer une grille aléatoire
def create_puzzle(size):
    tiles = list(range(size * size))
    while True:
        random.shuffle(tiles)
        grid = [tiles[i:i + size] for i in range(0, len(tiles), size)]
        if is_solvable(grid):
            return grid


# Fonction pour dessiner la grille du puzzle
def draw_grid(grid, pieces, grid_size):
    tile_size = SCREEN_WIDTH // grid_size
    for i, row in enumerate(grid):
        for j, tile in enumerate(row):
            x = j * tile_size
            y = i * tile_size
            if tile != 0:  # Ne pas dessiner l'espace vide
                screen.blit(pieces[tile], (x, y))
            pygame.draw.rect(screen, GRAY, (x, y, tile_size, tile_size), 2)

            #Si tuile sélectionné
            if (i , j) in selected_tiles:
                pygame.draw.rect(screen, BLUE, (j * tile_size, i * tile_size, tile_size, tile_size), 2)
