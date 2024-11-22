# Ajout de texte pour l'interface

def ajouttexte(ecran, font, text, color, x, y, center=True):
    texte_rendu = font.render(text, True, color)
    bouton = texte_rendu.get_rect()
    if center:
        bouton.center = (x, y)
    else:
        bouton.topleft = (x, y)
    ecran.blit(texte_rendu, bouton)