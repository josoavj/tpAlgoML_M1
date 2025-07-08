import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, f1_score, precision_score, recall_score
import re
import joblib
import time
from DatasetMorpionMinimax import generate_dataset, GameResult, PLAYER_X, PLAYER_O, EMPTY_CELL, \
    BOARD_SIZE


# --- Fonctions pour la préparation des données de classification ---
def parse_moves_string(moves_string: str) -> list[tuple[str, int]]:
    """
    Analyse la chaîne de coups pour extraire le joueur et le numéro de coup.
    Ex: "X1 O5 X2" -> [('X', 1), ('O', 5), ('X', 2)]
    """
    parsed_moves = []
    if not moves_string:
        return parsed_moves

    matches = re.findall(r'([XO])(\d+)', moves_string)
    for player_char, move_code_str in matches:
        parsed_moves.append((player_char, int(move_code_str)))
    return parsed_moves


def preprocess_game_data(dataset: list[tuple[str, GameResult]]) -> tuple[pd.DataFrame, pd.Series]:
    """
    Prépare le dataset pour l'entraînement du modèle.
    Crée des caractéristiques basées sur les coups et encode les résultats.
    """
    max_moves = 9
    features = []
    labels = []

    for moves_string, result_enum in dataset:
        # Initialiser un plateau vide pour suivre l'état de la partie coup par coup
        current_board = ['' for _ in range(9)]
        parsed_moves = parse_moves_string(moves_string)

        # Pour chaque coup dans la partie, enregistrer l'état du plateau
        # et le résultat final de la partie comme label
        for i, (player_char, move_code) in enumerate(parsed_moves):
            # Appliquer le coup à l'état actuel du plateau
            cell_index = move_code - 1
            current_board[cell_index] = player_char

            # Extraire les features de cet état du plateau
            game_features = [0] * (max_moves * 2)
            for j in range(max_moves):  # Pour chaque case du plateau
                if current_board[j] == 'X':
                    game_features[j] = 1  # Case j jouée par X
                elif current_board[j] == 'O':
                    game_features[j + max_moves] = 1  # Case j jouée par O

            features.append(game_features)
            labels.append(result_enum.value)  # Le label est le résultat final de la partie

    X = pd.DataFrame(features)
    y = pd.Series(labels)

    col_names = []
    for i in range(1, max_moves + 1):
        col_names.append(f'X_move_{i}')
    for i in range(1, max_moves + 1):
        col_names.append(f'O_move_{i}')
    X.columns = col_names  # Assigner les noms de colonnes pour éviter les avertissements sklearn

    return X, y


if __name__ == "__main__":
    print("🚀 Début du processus d'entraînement du modèle de classification 🚀")

    # 1. Générer le dataset
    print("\nÉtape 1: Génération du dataset des parties de Tic-Tac-Toe...")
    # Augmentons le nombre de jeux pour un meilleur entraînement et une meilleure démonstration
    start_time = time.time()
    dataset = generate_dataset(num_games=20000, optimal_ratio=0.7)  # Augmenté à 20000 jeux
    end_time = time.time()
    print(f"Génération du dataset terminée en {end_time - start_time:.2f} secondes.")
    print(f"Nombre de parties générées: {len(dataset)}")

    # 2. Préparer les données pour le modèle
    print("\nÉtape 2: Préparation des données pour l'entraînement du modèle...")
    start_time = time.time()
    X, y = preprocess_game_data(dataset)
    end_time = time.time()
    print(f"Préparation des données terminée en {end_time - start_time:.2f} secondes.")
    print(f"Forme des caractéristiques (X): {X.shape}")
    print(f"Forme des étiquettes (y): {y.shape}")
    print("Aperçu des caractéristiques (X.head()):")
    print(X.head())
    print("\nAperçu des étiquettes (y.head()):")
    print(y.head())
    print("\nDistribution des classes d'étiquettes:")
    print(y.value_counts())

    # 3. Diviser les données en ensembles d'entraînement et de test
    print("\nÉtape 3: Division des données en ensembles d'entraînement et de test (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    print(f"Forme de l'ensemble d'entraînement (X_train): {X_train.shape}")
    print(f"Forme de l'ensemble de test (X_test): {X_test.shape}")

    # 4. Choisir et entraîner le modèle
    print("\nÉtape 4: Entraînement du modèle RandomForestClassifier...")
    # Ajouter oob_score=True pour obtenir l'estimation d'erreur out-of-bag
    start_time = time.time()
    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1, oob_score=True,
                                   verbose=1)  # verbose pour plus d'infos pendant l'entraînement
    model.fit(X_train, y_train)
    end_time = time.time()
    print(f"Entraînement du modèle terminé en {end_time - start_time:.2f} secondes.")

    # 5. Évaluer le modèle
    print("\nÉtape 5: Évaluation du modèle...")

    # Précision sur l'ensemble d'entraînement
    y_train_pred = model.predict(X_train)
    train_accuracy = accuracy_score(y_train, y_train_pred)
    train_f1 = f1_score(y_train, y_train_pred, average='weighted')  # weighted pour les classes déséquilibrées
    print(f"\n📈 Métriques d'entraînement :")
    print(f"   Précision (Accuracy) sur l'entraînement: {train_accuracy:.4f}")
    print(f"   F1-Score sur l'entraînement: {train_f1:.4f}")
    if model.oob_score_:
        print(f"   OOB Score (Erreur d'estimation de généralisation): {model.oob_score_:.4f}")
        print(f"   OOB Erreur: {1 - model.oob_score_:.4f}")

    # Précision sur l'ensemble de test
    y_pred = model.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_pred)
    test_precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    test_recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    test_f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

    print(f"\n📊 Métriques d'évaluation sur l'ensemble de test :")
    print(f"   Précision (Accuracy): {test_accuracy:.4f}")
    print(f"   Précision (Precision): {test_precision:.4f}")
    print(f"   Rappel (Recall): {test_recall:.4f}")
    print(f"   F1-Score: {test_f1:.4f}")

    print("\nDetailed Classification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))

    # Affichage des importances des caractéristiques
    print("\nImportance des caractéristiques (Top 10) :")
    feature_importances = pd.Series(model.feature_importances_, index=X_train.columns)
    print(feature_importances.nlargest(10))

    # 6. Sauvegarder le modèle
    print("\nÉtape 6: Sauvegarde du modèle entraîné...")
    joblib.dump(model, 'tic_tac_toe_classifier.pkl')
    print("Modèle sauvegardé sous 'tic_tac_toe_classifier.pkl'")

    print("\n✅ Processus d'entraînement et d'évaluation du modèle terminé. ✅")