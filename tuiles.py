from config import SCREEN_WIDTH


def move_tile(grid, direction):
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
        from main import chosen_swap
        if chosen_swap[1] > 0 and move_count % chosen_swap[1] == 0 :
            swap_available = True
            show_alert = True

#Fonction pour échanger les tuiles
def perfomr_swap(puzzle, selected_tiles):
    if len(selected_tiles) == 2:
        pos1, pos2 = selected_tiles
        puzzle[pos1[0]][pos1[1]], puzzle[pos2[0]][pos2[1]] = puzzle[pos2[0]][pos2[1]], puzzle[pos1[0]][pos1[1]]
        return True
    return False

#Fonction de sélection tuiles
def get_tile_clicked(pos, grid_size):
    tile_size = SCREEN_WIDTH // grid_size
    x,y = pos
    row = y // tile_size
    col = x // tile_size
    return row, col

