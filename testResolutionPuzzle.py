# Teste si le puzzle est résolvable en comptant à l'inverse

def siresolvable(grille):
    plan_grille = [tuile for ligne in grille for tuile in ligne if tuile != 0]
    inversion = 0
    for ligneGrille in range(len(plan_grille)):
        for colonneGrille in range(ligneGrille + 1, len(plan_grille)):
            if plan_grille[ligneGrille] > plan_grille[colonneGrille]:
                inversion += 1
    return inversion % 2 == 0
