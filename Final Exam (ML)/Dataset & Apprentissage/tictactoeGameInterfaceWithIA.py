import pygame
import sys
import math
import random
import numpy as np
from enum import Enum
import pandas as pd
import joblib  # Pour charger le modèle entraîné
import re

# IMPORTANT: Importez TicTacToe et GameResult depuis votre module de dataset
# Assurez-vous que votre structure de dossier et les __init__.py sont corrects.
# Le chemin dépendra de l'emplacement d'exécution.
# Si vous exécutez depuis le dossier "Final Exam (ML)", alors c'est:
from DatasetMorpionMinimax import TicTacToe, GameResult, PLAYER_X, PLAYER_O, EMPTY_CELL, BOARD_SIZE

# Initialisation de Pygame
pygame.init()

# Constantes Pygame
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BOARD_SIZE_PX = 350  # Renommé pour éviter conflit avec BOARD_SIZE du jeu (qui est 3)
CELL_SIZE_PX = BOARD_SIZE_PX // 3
BOARD_X = (WINDOW_WIDTH - BOARD_SIZE_PX) // 2
BOARD_Y = 100

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)
BLUE = (33, 150, 243)
RED = (244, 67, 54)
GREEN = (76, 175, 80)
ORANGE = (255, 152, 0)
PURPLE = (156, 39, 176)


class Difficulty(Enum):
    #EASY = "Facile"
   # MEDIUM = "Moyen"
    EXPERT = "Minimax"
    ML_MODEL = "Modèle ML"  # Nom de l'IA utilisant le modèle Machine Learning


# ... (le début de votre fichier Pygame)

class TicTacToeMLModel:
    """Classe pour gérer le modèle ML (RandomForest) et l'extraction de features."""

    def __init__(self, model_path='tic_tac_toe_classifier.pkl'):
        self.model = None
        self.is_loaded = False

        # Récupérer l'ordre des features tel qu'utilisé lors de l'entraînement
        max_moves = 9
        self.feature_names = []
        for i in range(1, max_moves + 1):
            self.feature_names.append(f'X_move_{i}')
        for i in range(1, max_moves + 1):
            self.feature_names.append(f'O_move_{i}')

        try:
            self.model = joblib.load(model_path)
            self.is_loaded = True
            print(f"Modèle ML ({type(self.model).__name__}) chargé depuis '{model_path}'")

        except FileNotFoundError:
            print(
                f"Erreur: Le fichier modèle '{model_path}' n'a pas été trouvé. Assurez-vous qu'il est dans le bon répertoire.")
        except Exception as e:
            print(f"Erreur lors du chargement du modèle: {e}")

    def extract_features(self,
                         board_state: list[str]) -> pd.DataFrame:  # <-- Changer le type de retour pour pd.DataFrame
        """
        Extrait les features d'un état de plateau pour le modèle ML.
        Doit correspondre exactement aux features utilisées lors de l'entraînement.
        Le board_state est une liste de 9 strings ('X', 'O', ou '').
        """
        max_moves = 9
        game_features = [0] * (max_moves * 2)  # 9 coups pour X, 9 pour O

        for i in range(BOARD_SIZE * BOARD_SIZE):  # i de 0 à 8
            if board_state[i] == 'X':
                feature_index = i
                game_features[feature_index] = 1
            elif board_state[i] == 'O':
                feature_index = i + max_moves
                game_features[feature_index] = 1

        # Retournez le DataFrame directement, avec les noms de colonnes
        features_df = pd.DataFrame([game_features], columns=self.feature_names)
        return features_df  # <-- C'est la modification clé ici !

    def predict_best_move(self, current_board_state: list[str], current_player_char: str) -> int:
        """
        Prédit le meilleur coup pour le joueur courant en utilisant le modèle ML.
        Simule chaque coup possible, prédit l'issue, et choisit le meilleur.
        """
        if not self.is_loaded:
            print("Modèle ML non chargé, ne peut pas prédire de coup.")
            return None

        available_moves_indices = [i for i, cell in enumerate(current_board_state) if cell == '']
        if not available_moves_indices:
            return None

        best_move = None

        if current_player_char == 'O':
            best_score = -np.inf
            priority_map = {
                GameResult.O_WINS.value: 2.0,
                GameResult.QUICK_WIN_O.value: 2.5,
                GameResult.DRAW.value: 0.5,
                GameResult.X_WINS.value: -1.0,
                GameResult.QUICK_WIN_X.value: -1.5
            }
            is_maximizing_player = True
        else:
            best_score = np.inf
            priority_map = {
                GameResult.X_WINS.value: 2.0,
                GameResult.QUICK_WIN_X.value: 2.5,
                GameResult.DRAW.value: 0.5,
                GameResult.O_WINS.value: -1.0,
                GameResult.QUICK_WIN_O.value: -1.5
            }
            is_maximizing_player = False

        # ... (le reste de la fonction predict_best_move reste identique)
        for move_idx in available_moves_indices:
            temp_board = list(current_board_state)
            temp_board[move_idx] = current_player_char

            temp_game_obj = TicTacToe()
            temp_game_obj.board = np.array([
                PLAYER_X if c == 'X' else (PLAYER_O if c == 'O' else EMPTY_CELL)
                for c in temp_board
            ]).reshape((BOARD_SIZE, BOARD_SIZE))

            if temp_game_obj.is_winner(PLAYER_O) and current_player_char == 'O':
                return move_idx

            features = self.extract_features(
                temp_board)  # Cette ligne appelle la fonction modifiée, qui renvoie un DataFrame

            probabilities = self.model.predict_proba(features)[0]  # model.predict_proba() recevra un DataFrame

            current_move_score = 0
            for i, prob in enumerate(probabilities):
                outcome_class_value = self.model.classes_[i]
                current_move_score += prob * priority_map.get(outcome_class_value, 0)

            if is_maximizing_player:
                if current_move_score > best_score:
                    best_score = current_move_score
                    best_move = move_idx
            else:
                if current_move_score < best_score:
                    best_score = current_move_score
                    best_move = move_idx

        if best_move is None and available_moves_indices:
            best_move = random.choice(available_moves_indices)

        return best_move


# ... (le reste de votre script Pygame)


class TicTacToeAI:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("🧠 IA Tic-Tac-Toe avec Modèle ML")

        # Polices
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)

        # Variables de jeu
        self.board = ['' for _ in range(9)]  # Le plateau de jeu de Pygame
        self.player_turn = True  # True for 'X', False for 'O' (AI)
        self.game_over = False
        self.winner = None
        self.difficulty = Difficulty.ML_MODEL  # Commencer avec le modèle ML
        self.ai_thinking = False
        self.ai_think_timer = 0

        # Scores
        self.player_score = 0
        self.ai_score = 0
        self.draws = 0

        # Modèle ML (chargera RandomForest)
        self.ml_model = TicTacToeMLModel(model_path='tic_tac_toe_classifier.pkl')

        # Boutons
        self.buttons = []
        self.setup_buttons()

        # Horloge pour contrôler le FPS
        self.clock = pygame.time.Clock()

    def setup_buttons(self):
        """Initialiser les boutons de l'interface"""
        # Bouton nouvelle partie
        self.new_game_btn = {
            'rect': pygame.Rect(50, 500, 150, 50),
            'text': 'Nouvelle Partie',
            'color': GREEN,
            'hover_color': (56, 142, 60)
        }

        # Bouton reset scores
        self.reset_scores_btn = {
            'rect': pygame.Rect(220, 500, 150, 50),
            'text': 'Reset Scores',
            'color': ORANGE,
            'hover_color': (245, 124, 0)
        }

        # Boutons de difficulté (uniquement les difficultés demandées)
        self.difficulty_buttons = []
        difficulties = [Difficulty.EXPERT, Difficulty.ML_MODEL]
        colors = [RED, PURPLE]

        for i, (diff, color) in enumerate(zip(difficulties, colors)):
            btn = {
                'rect': pygame.Rect(550 + i * 100, 500, 90, 50),
                'text': diff.value,
                'color': color,
                'hover_color': tuple(max(0, c - 30) for c in color),
                'difficulty': diff
            }
            self.difficulty_buttons.append(btn)

    def draw_board(self):
        """Dessiner le plateau de jeu"""
        # Fond du plateau
        board_rect = pygame.Rect(BOARD_X, BOARD_Y, BOARD_SIZE_PX, BOARD_SIZE_PX)
        pygame.draw.rect(self.screen, WHITE, board_rect)
        pygame.draw.rect(self.screen, BLACK, board_rect, 3)

        # Lignes de séparation
        for i in range(1, 3):
            # Lignes verticales
            pygame.draw.line(self.screen, BLACK,
                             (BOARD_X + i * CELL_SIZE_PX, BOARD_Y),
                             (BOARD_X + i * CELL_SIZE_PX, BOARD_Y + BOARD_SIZE_PX), 3)
            # Lignes horizontales
            pygame.draw.line(self.screen, BLACK,
                             (BOARD_X, BOARD_Y + i * CELL_SIZE_PX),
                             (BOARD_X + BOARD_SIZE_PX, BOARD_Y + i * CELL_SIZE_PX), 3)

        # Dessiner X et O
        for i in range(9):
            row = i // 3
            col = i % 3
            cell_x = BOARD_X + col * CELL_SIZE_PX
            cell_y = BOARD_Y + row * CELL_SIZE_PX
            center_x = cell_x + CELL_SIZE_PX // 2
            center_y = cell_y + CELL_SIZE_PX // 2

            if self.board[i] == 'X':
                # Dessiner X
                pygame.draw.line(self.screen, BLUE,
                                 (center_x - 50, center_y - 50),
                                 (center_x + 50, center_y + 50), 8)
                pygame.draw.line(self.screen, BLUE,
                                 (center_x + 50, center_y - 50),
                                 (center_x - 50, center_y + 50), 8)
            elif self.board[i] == 'O':
                # Dessiner O
                pygame.draw.circle(self.screen, RED, (center_x, center_y), 50, 8)

    def draw_ui(self):
        """Dessiner l'interface utilisateur"""
        # Titre
        title_text = self.font_large.render("Tic Tac Toe", True, BLACK)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 30))
        self.screen.blit(title_text, title_rect)

        # Scores
        score_y = 60
        player_text = self.font_medium.render(f"Joueur: {self.player_score}", True, BLUE)
        self.screen.blit(player_text, (50, score_y))

        draws_text = self.font_medium.render(f"Nuls: {self.draws}", True, GRAY)
        draws_rect = draws_text.get_rect(center=(WINDOW_WIDTH // 2, score_y + 15))
        self.screen.blit(draws_text, draws_rect)

        ai_text = self.font_medium.render(f"IA: {self.ai_score}", True, RED)
        ai_rect = ai_text.get_rect(right=WINDOW_WIDTH - 50, top=score_y)
        self.screen.blit(ai_text, ai_rect)

        # Statut du jeu
        status_y = BOARD_Y + BOARD_SIZE_PX + 20
        if self.game_over:
            if self.winner == 'X':
                status = "🎉 Vous avez gagné !"
                color = GREEN
            elif self.winner == 'O':
                status = "🤖 L'IA a gagné !"
                color = RED
            else:
                status = "🤝 Match nul !"
                color = ORANGE
        else:
            if self.player_turn:
                status = "Votre tour (X)"
                color = BLUE
            else:
                if self.ai_thinking:
                    if self.difficulty == Difficulty.ML_MODEL:
                        status = "Modèle ML analyse..."
                    else:
                        status = "L'IA réfléchit..."
                else:
                    status = f"Tour de l'IA ({self.difficulty.value})"
                color = PURPLE

        status_text = self.font_medium.render(status, True, color)
        status_rect = status_text.get_rect(center=(WINDOW_WIDTH // 2, status_y))
        self.screen.blit(status_text, status_rect)

        # Difficulté actuelle
        diff_text = self.font_small.render(f"Mode: {self.difficulty.value}", True, BLACK)
        self.screen.blit(diff_text, (50, WINDOW_HEIGHT - 40))

        # Indicateur ML Model
        if self.difficulty == Difficulty.ML_MODEL:
            ml_status = "✅ Modèle chargé" if self.ml_model.is_loaded else "❌ Modèle non trouvé"
            ml_text = self.font_small.render(f"Modèle ML: {ml_status}", True, PURPLE)
            self.screen.blit(ml_text, (50, WINDOW_HEIGHT - 20))

    def draw_button(self, button, mouse_pos):
        """Dessiner un bouton"""
        color = button['hover_color'] if button['rect'].collidepoint(mouse_pos) else button['color']
        pygame.draw.rect(self.screen, color, button['rect'])
        pygame.draw.rect(self.screen, BLACK, button['rect'], 2)

        text = self.font_small.render(button['text'], True, WHITE)
        text_rect = text.get_rect(center=button['rect'].center)
        self.screen.blit(text, text_rect)

    def draw_buttons(self, mouse_pos):
        """Dessiner tous les boutons"""
        self.draw_button(self.new_game_btn, mouse_pos)
        self.draw_button(self.reset_scores_btn, mouse_pos)

        for btn in self.difficulty_buttons:
            # Marquer le bouton de difficulté actuel
            if btn['difficulty'] == self.difficulty:
                pygame.draw.rect(self.screen, BLACK, btn['rect'], 4)
            self.draw_button(btn, mouse_pos)

    def get_cell_from_mouse(self, mouse_pos):
        """Obtenir la cellule cliquée à partir de la position de la souris"""
        x, y = mouse_pos
        if (BOARD_X <= x <= BOARD_X + BOARD_SIZE_PX and
                BOARD_Y <= y <= BOARD_Y + BOARD_SIZE_PX):
            col = (x - BOARD_X) // CELL_SIZE_PX
            row = (y - BOARD_Y) // CELL_SIZE_PX
            return row * 3 + col
        return None

    def player_move(self, cell):
        """Effectuer le mouvement du joueur"""
        if (self.board[cell] == '' and self.player_turn and
                not self.game_over and not self.ai_thinking):
            self.board[cell] = 'X'
            self.player_turn = False
            self.check_game_over()

            if not self.game_over:
                self.ai_thinking = True
                self.ai_think_timer = pygame.time.get_ticks()

    def ai_move(self):
        """Effectuer le mouvement de l'IA"""
        move = None
        if self.difficulty == Difficulty.ML_MODEL:
            move = self.ml_model.predict_best_move(self.board, 'O')  # L'IA joue 'O'
        else:  # EXPERT (Minimax)
            move = self.get_best_move()

        if move is not None:
            self.board[move] = 'O'
            self.player_turn = True
            self.ai_thinking = False
            self.check_game_over()

    def get_random_move(self):
        """Mouvement aléatoire pour difficulté facile"""
        available_moves = [i for i in range(9) if self.board[i] == '']
        return random.choice(available_moves) if available_moves else None

    def get_medium_move(self):
        """Mouvement pour difficulté moyenne"""
        # Utilise minimax 70% du temps, sinon aléatoire
        if random.random() < 0.7:
            return self.get_best_move()
        else:
            return self.get_random_move()

    def get_best_move(self):
        """Mouvement optimal avec algorithme minimax"""
        best_score = -math.inf
        best_move = None

        for i in range(9):
            if self.board[i] == '':
                self.board[i] = 'O'
                score = self.minimax(self.board, 0, False)  # IA est max, donc le joueur suivant est min
                self.board[i] = ''  # Annuler le coup

                if score > best_score:
                    best_score = score
                    best_move = i

        return best_move

    def minimax(self, board, depth, is_maximizing):
        """Algorithme minimax (pour l'IA 'O' - maximisante)"""
        winner = self.check_winner(board)

        if winner == 'O':
            return 10 - depth  # L'IA gagne, meilleure si plus tôt
        elif winner == 'X':
            return depth - 10  # Le joueur gagne, pire si plus tôt
        elif self.is_board_full(board):
            return 0  # Nul

        if is_maximizing:  # C'est le tour de l'IA (O)
            best_score = -math.inf
            for i in range(9):
                if board[i] == '':
                    board[i] = 'O'
                    score = self.minimax(board, depth + 1,
                                         False)  # Après le coup de l'IA, c'est le tour du joueur (min)
                    board[i] = ''
                    best_score = max(score, best_score)
            return best_score
        else:  # C'est le tour du joueur (X)
            best_score = math.inf
            for i in range(9):
                if board[i] == '':
                    board[i] = 'X'
                    score = self.minimax(board, depth + 1, True)  # Après le coup du joueur, c'est le tour de l'IA (max)
                    board[i] = ''
                    best_score = min(score, best_score)
            return best_score

    def check_winner(self, board):
        """Vérifier s'il y a un gagnant"""
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # lignes
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # colonnes
            [0, 4, 8], [2, 4, 6]  # diagonales
        ]

        for combo in winning_combinations:
            if (board[combo[0]] == board[combo[1]] == board[combo[2]] != ''):
                return board[combo[0]]
        return None

    def is_board_full(self, board):
        """Vérifier si le plateau est plein"""
        return '' not in board

    def check_game_over(self):
        """Vérifier si le jeu est terminé"""
        winner = self.check_winner(self.board)
        if winner:
            self.game_over = True
            self.winner = winner
            if winner == 'X':
                self.player_score += 1
            else:
                self.ai_score += 1
        elif self.is_board_full(self.board):
            self.game_over = True
            self.winner = None
            self.draws += 1

    def new_game(self):
        """Commencer une nouvelle partie"""
        self.board = ['' for _ in range(9)]
        self.player_turn = True
        self.game_over = False
        self.winner = None
        self.ai_thinking = False

    def reset_scores(self):
        """Réinitialiser les scores"""
        self.player_score = 0
        self.ai_score = 0
        self.draws = 0

    def handle_click(self, mouse_pos):
        """Gérer les clics de souris"""
        # Clic sur le plateau
        cell = self.get_cell_from_mouse(mouse_pos)
        if cell is not None:
            self.player_move(cell)
            return

        # Clic sur les boutons
        if self.new_game_btn['rect'].collidepoint(mouse_pos):
            self.new_game()
        elif self.reset_scores_btn['rect'].collidepoint(mouse_pos):
            self.reset_scores()

        # Clic sur les boutons de difficulté
        for btn in self.difficulty_buttons:
            if btn['rect'].collidepoint(mouse_pos):
                self.difficulty = btn['difficulty']
                # Si le jeu n'est pas terminé et c'est le tour de l'IA après un changement de difficulté
                if not self.game_over and not self.player_turn:
                    self.ai_thinking = True
                    self.ai_think_timer = pygame.time.get_ticks()

    def run(self):
        """Boucle principale du jeu"""
        running = True
        print("🎮 Jeu Tic-Tac-Toe avec Modèle ML démarré!")
        print(f"🧠 Modèle ML: {'Chargé' if self.ml_model.is_loaded else 'Non trouvé/Erreur'}")

        while running:
            current_time = pygame.time.get_ticks()
            mouse_pos = pygame.mouse.get_pos()

            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic gauche
                        self.handle_click(mouse_pos)

            # IA fait son mouvement après réflexion
            # Condition ajoutée: vérifie que le modèle est chargé si la difficulté est ML_MODEL
            if (self.ai_thinking and not self.game_over and
                    current_time - self.ai_think_timer > 1000):  # 1 seconde de réflexion

                if self.difficulty == Difficulty.ML_MODEL and not self.ml_model.is_loaded:
                    print("Impossible pour l'IA ML de jouer: Modèle non chargé. Reviens au mode Aléatoire.")# Fallback
                    self.ai_thinking = False  # Arrête de penser à cause de l'erreur
                    self.ai_move()  # Fais un move aléatoire tout de suite
                else:
                    self.ai_move()

            # Dessiner l'écran
            self.screen.fill(LIGHT_GRAY)
            self.draw_board()
            self.draw_ui()
            self.draw_buttons(mouse_pos)

            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = TicTacToeAI()
    game.run()