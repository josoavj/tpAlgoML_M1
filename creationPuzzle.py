import random
from testResolutionPuzzle import siresolvable

# Création d'un Puzzle glissant résolvable
def creation_puzzle(taille):
    tuile = list(range(taille * taille))
    while True:
        random.shuffle(tuile)
        grille = [tuile[i,i] for i in range(0, len(tuile), taille)]
        if siresolvable(grille):
            return grille
