import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import re

from DatasetMorpionMinimax import generate_dataset, GameResult
# --- Fonctions pour la préparation des données de classification ---

def parse_moves_string(moves_string: str) -> list[tuple[str, int]]:
    """
    Analyse la chaîne de coups pour extraire le joueur et le numéro de coup.
    Ex: "X1 O5 X2" -> [('X', 1), ('O', 5), ('X', 2)]
    """
    parsed_moves = []
    if not moves_string:
        return parsed_moves

    # Utilise une expression régulière pour trouver chaque coup (ex: X1, O5)
    # [XO]\d+ : commence par X ou O, suivi d'un ou plusieurs chiffres
    matches = re.findall(r'([XO])(\d+)', moves_string)
    for player_char, move_code_str in matches:
        parsed_moves.append((player_char, int(move_code_str)))
    return parsed_moves


def preprocess_game_data(dataset: list[tuple[str, GameResult]]) -> tuple[pd.DataFrame, pd.Series]:
    """
    Prépare le dataset pour l'entraînement du modèle.
    Crée des caractéristiques basées sur les coups et encode les résultats.
    """
    max_moves = 9  # Une partie de Tic-Tac-Toe a au maximum 9 coups
    features = []
    labels = []

    for moves_string, result_enum in dataset:
        parsed_moves = parse_moves_string(moves_string)

        # Initialise un vecteur de caractéristiques pour cette partie
        # Chaque coup possible (1-9) pour X et O.
        # Ex: X_1, X_2, ..., X_9, O_1, O_2, ..., O_9
        # Nous allons marquer 1 si ce coup a été joué, 0 sinon.
        game_features = [0] * (max_moves * 2)  # 9 coups pour X, 9 pour O

        for i, (player_char, move_code) in enumerate(parsed_moves):
            # Le move_code est de 1 à 9. Convertir en index 0 à 8.
            feature_index = move_code - 1
            if player_char == 'O':
                feature_index += max_moves  # Les coups de O commencent après les coups de X

            if 0 <= feature_index < len(game_features):  # S'assurer que l'index est valide
                game_features[feature_index] = 1  # Marque que ce coup a été joué

        features.append(game_features)
        labels.append(result_enum.value)  # Utilise la valeur de l'énumération comme étiquette

    # Convertit en DataFrame pour Scikit-learn
    X = pd.DataFrame(features)
    y = pd.Series(labels)

    # Nomme les colonnes pour une meilleure lisibilité (optionnel)
    col_names = []
    for i in range(1, max_moves + 1):
        col_names.append(f'X_move_{i}')
    for i in range(1, max_moves + 1):
        col_names.append(f'O_move_{i}')
    X.columns = col_names

    return X, y


# --- Main execution block for dataset generation and model training ---
if __name__ == "__main__":
    # 1. Générer le dataset
    print("Étape 1: Génération du dataset des parties de Tic-Tac-Toe...")
    # Vous pouvez ajuster le nombre de parties ici
    dataset = generate_dataset(num_games=10000, optimal_ratio=0.7)
    print("Génération du dataset terminée.")

    # 2. Préparer les données pour le modèle
    print("\nÉtape 2: Préparation des données pour l'entraînement du modèle...")
    X, y = preprocess_game_data(dataset)
    print(f"Forme des caractéristiques (X): {X.shape}")
    print(f"Forme des étiquettes (y): {y.shape}")
    print("Aperçu des caractéristiques (X.head()):")
    print(X.head())
    print("\nAperçu des étiquettes (y.head()):")
    print(y.head())

    # 3. Diviser les données en ensembles d'entraînement et de test
    # Nous utilisons 80% pour l'entraînement et 20% pour le test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    print(f"\nForme de l'ensemble d'entraînement (X_train): {X_train.shape}")
    print(f"Forme de l'ensemble de test (X_test): {X_test.shape}")

    # 4. Choisir et entraîner le modèle
    print("\nÉtape 3: Entraînement du modèle Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42,
                                   n_jobs=-1)  # n_jobs=-1 utilise tous les cœurs disponibles
    model.fit(X_train, y_train)
    print("Entraînement du modèle terminé.")

    # 5. Évaluer le modèle
    print("\nÉtape 4: Évaluation du modèle...")
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f"Précision du modèle sur l'ensemble de test: {accuracy:.4f}")

    print("\nRapport de classification:")
    print(classification_report(y_test, y_pred))

    # Vous pouvez également sauvegarder le modèle si vous le souhaitez
    import joblib
    joblib.dump(model, 'tic_tac_toe_classifier.pkl')
    print("\nModèle sauvegardé sous 'tic_tac_toe_classifier.pkl'")

    print("\nProcessus d'implémentation et d'apprentissage du modèle terminé.")