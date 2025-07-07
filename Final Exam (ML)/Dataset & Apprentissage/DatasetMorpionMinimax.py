import numpy as np
import random
from collections import defaultdict
from enum import Enum
import functools

# --- Constants ---
BOARD_SIZE = 3
PLAYER_X = 1
PLAYER_O = -1
EMPTY_CELL = 0


# --- Enums for better readability ---
class Player(Enum):
    X = PLAYER_X
    O = PLAYER_O


class GameResult(Enum):
    X_WINS = "X_Wins"
    O_WINS = "O_Wins"
    DRAW = "Draw"
    IN_PROGRESS = "In_Progress"
    QUICK_WIN_X = "Quick_Win_X"
    QUICK_WIN_O = "Quick_Win_O"


class TicTacToe:
    def __init__(self):
        self.board: np.ndarray = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.current_player: Player = Player.X
        self.moves_made: list[str] = []  # Stores moves as "X1", "O5", etc.
        self.move_history_codes: list[int] = []  # Stores moves as 1-9 codes

    def reset(self) -> None:
        """Resets the game board and state."""
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.current_player = Player.X
        self.moves_made = []
        self.move_history_codes = []

    def _position_to_code(self, row: int, col: int) -> int:
        """Converts (row, col) to a 1-9 code."""
        return row * BOARD_SIZE + col + 1

    def _code_to_position(self, code: int) -> tuple[int, int]:
        """Converts a 1-9 code to (row, col)."""
        code -= 1
        return (code // BOARD_SIZE, code % BOARD_SIZE)

    def make_move(self, code: int) -> bool:
        """
        Attempts to make a move on the board.
        Returns True if the move was successful, False otherwise.
        """
        row, col = self._code_to_position(code)
        if self.board[row, col] == EMPTY_CELL:
            self.board[row, col] = self.current_player.value
            player_char = 'X' if self.current_player == Player.X else 'O'
            self.moves_made.append(f"{player_char}{code}")
            self.move_history_codes.append(code)
            self.current_player = Player.O if self.current_player == Player.X else Player.X
            return True
        return False

    def is_winner(self, player_value: int) -> bool:
        """Checks if the given player has won."""
        # Check rows
        for i in range(BOARD_SIZE):
            if np.all(self.board[i, :] == player_value):
                return True
        # Check columns
        for j in range(BOARD_SIZE):
            if np.all(self.board[:, j] == player_value):
                return True
        # Check diagonals
        if np.all(np.diag(self.board) == player_value):
            return True
        if np.all(np.diag(np.fliplr(self.board)) == player_value):
            return True
        return False

    def is_draw(self) -> bool:
        """Checks if the game is a draw."""
        return not np.any(self.board == EMPTY_CELL) and not (self.is_winner(PLAYER_X) or self.is_winner(PLAYER_O))

    def is_terminal(self) -> bool:
        """Checks if the game has ended (win or draw)."""
        return self.is_winner(PLAYER_X) or self.is_winner(PLAYER_O) or self.is_draw()

    def get_valid_moves(self) -> list[int]:
        """Returns a list of valid moves (1-9 codes)."""
        return [self._position_to_code(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if
                self.board[r, c] == EMPTY_CELL]

    def get_game_result(self) -> GameResult:
        """Determines the outcome of the game."""
        if self.is_winner(PLAYER_O):
            return GameResult.QUICK_WIN_O if len(self.moves_made) <= 6 else GameResult.O_WINS
        elif self.is_winner(PLAYER_X):
            return GameResult.QUICK_WIN_X if len(self.moves_made) <= 5 else GameResult.X_WINS
        elif self.is_draw():
            return GameResult.DRAW
        return GameResult.IN_PROGRESS

    def get_moves_string(self) -> str:
        """Returns a space-separated string of moves made."""
        return " ".join(self.moves_made)

    def get_board_tuple(self) -> tuple:
        """Returns a hashable representation of the board for caching."""
        return tuple(self.board.flatten())


# --- Minimax Function ---
@functools.lru_cache(maxsize=None)  # Cache results for board states
def minimax(board_tuple: tuple, current_player_value: int, depth: int, alpha: float, beta: float) -> int:
    """
    Minimax algorithm with Alpha-Beta pruning for Tic-Tac-Toe.
    Returns the score for the current board state.
    """
    temp_game = TicTacToe()
    temp_game.board = np.array(board_tuple).reshape((BOARD_SIZE, BOARD_SIZE))
    temp_game.current_player = Player(current_player_value)

    if temp_game.is_winner(PLAYER_O):  # O (maximizing player) wins
        return 1
    if temp_game.is_winner(PLAYER_X):  # X (minimizing player) wins
        return -1
    if temp_game.is_draw():
        return 0

    if current_player_value == PLAYER_O:  # Maximizing player (O)
        max_eval = -np.inf
        for move_code in temp_game.get_valid_moves():
            row, col = temp_game._code_to_position(move_code)
            temp_game.board[row, col] = PLAYER_O
            eval = minimax(temp_game.get_board_tuple(), PLAYER_X, depth + 1, alpha, beta)
            temp_game.board[row, col] = EMPTY_CELL  # Undo move
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:  # Minimizing player (X)
        min_eval = np.inf
        for move_code in temp_game.get_valid_moves():
            row, col = temp_game._code_to_position(move_code)
            temp_game.board[row, col] = PLAYER_X
            eval = minimax(temp_game.get_board_tuple(), PLAYER_O, depth + 1, alpha, beta)
            temp_game.board[row, col] = EMPTY_CELL  # Undo move
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


# --- Game Generation Functions ---
def generate_random_game() -> tuple[str, GameResult]:
    """Generates a game where both players make random valid moves."""
    game = TicTacToe()
    while not game.is_terminal():
        valid_moves = game.get_valid_moves()
        if not valid_moves:  # Should not happen in a non-terminal state unless board is full (draw)
            break
        move = random.choice(valid_moves)
        game.make_move(move)
    return game.get_moves_string(), game.get_game_result()


def generate_optimal_game(minimax_probability_o: float = 1.0, minimax_probability_x: float = 0.7) -> tuple[
    str, GameResult]:
    """
    Generates a game where players use minimax with a given probability,
    otherwise make random moves.
    """
    game = TicTacToe()
    while not game.is_terminal():
        valid_moves = game.get_valid_moves()
        if not valid_moves:
            break

        best_move = None

        # Decide if current player uses minimax
        use_minimax = False
        if game.current_player == Player.O and random.random() < minimax_probability_o:
            use_minimax = True
        elif game.current_player == Player.X and random.random() < minimax_probability_x:
            use_minimax = True

        if use_minimax:
            # Minimax logic
            if game.current_player == Player.O:  # Maximizing player
                best_score = -np.inf
                for move in valid_moves:
                    row, col = game._code_to_position(move)
                    game.board[row, col] = game.current_player.value
                    score = minimax(game.get_board_tuple(), Player.X.value, 0, -np.inf, np.inf)
                    game.board[row, col] = EMPTY_CELL  # Undo move
                    if score > best_score:
                        best_score = score
                        best_move = move
            else:  # Minimizing player (X)
                best_score = np.inf
                for move in valid_moves:
                    row, col = game._code_to_position(move)
                    game.board[row, col] = game.current_player.value
                    score = minimax(game.get_board_tuple(), Player.O.value, 0, -np.inf, np.inf)
                    game.board[row, col] = EMPTY_CELL  # Undo move
                    if score < best_score:
                        best_score = score
                        best_move = move

            if best_move is None:  # Fallback to random if minimax somehow fails (shouldn't happen with valid moves)
                best_move = random.choice(valid_moves)
        else:
            best_move = random.choice(valid_moves)

        game.make_move(best_move)

    return game.get_moves_string(), game.get_game_result()


def generate_dataset(num_games: int = 1000, optimal_ratio: float = 0.7) -> list[tuple[str, GameResult]]:
    """Generates a dataset of Tic-Tac-Toe games."""
    dataset = []
    num_optimal_games = int(num_games * optimal_ratio)
    num_random_games = num_games - num_optimal_games

    print(f"Generating {num_optimal_games} optimal games and {num_random_games} random games...")

    for i in range(num_optimal_games):
        moves, outcome = generate_optimal_game()
        dataset.append((moves, outcome))
        if (i + 1) % 100 == 0:
            print(f"Generated {i + 1}/{num_optimal_games} optimal games.")
            # Clear minimax cache periodically to prevent excessive memory usage if running many games
            minimax.cache_clear()

    for i in range(num_random_games):
        moves, outcome = generate_random_game()
        dataset.append((moves, outcome))
        if (i + 1) % 100 == 0:
            print(f"Generated {i + 1}/{num_random_games} random games.")

    return dataset


# --- Main execution block ---
if __name__ == "__main__":
    # Generate the dataset
    dataset = generate_dataset(num_games=1000)

    # Display a sample of games
    print("\nSample games:")
    for i in range(min(20, len(dataset))):
        print(f"Game {i + 1}: {dataset[i][0]}, Result: {dataset[i][1].value}")

    # Save to a file
    output_filename = 'tic_tac_toe_games.txt'
    with open(output_filename, 'w') as f:
        for game_moves, game_result in dataset:
            f.write(f'("{game_moves}", "{game_result.value}"),\n')

    print(f"\nDataset saved to '{output_filename}'")