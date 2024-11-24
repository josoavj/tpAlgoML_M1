
# Fonction pour vérifier si une grille est résolvable
def is_solvable(grid):
    flat_grid = [tile for row in grid for tile in row if tile != 0]
    inversions = 0
    for i in range(len(flat_grid)):
        for j in range(i + 1, len(flat_grid)):
            if flat_grid[i] > flat_grid[j]:
                inversions += 1
    return inversions % 2 == 0

