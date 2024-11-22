import pygame
from ajoutTexte import ajouttexte

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (70, 130, 180)


def dessinergrille(ecran, largeurecran, font, grille, taille):
    ecran.fill(WHITE)
    taille_tuile = largeurecran // taille
    for i, row in enumerate(grille):
        for j, tile in enumerate(row):
            x = j * taille_tuile
            y = i * taille_tuile
            if tile != 0:  # Ne pas dessiner l'espace vide
                pygame.draw.rect(ecran, BLUE, (x, y, taille_tuile, taille_tuile))
                ajouttexte(ecran, font, str(tile), WHITE, x + taille_tuile // 2, y + taille_tuile // 2)
            pygame.draw.rect(ecran, BLACK, (x, y, taille_tuile, taille_tuile), 2)