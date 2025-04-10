# MACHINE LEARNING

- **Thème:** Classification et Clustering
- **TP du:** 25 Janvier 2025
- **Langage:** Python
- **Membres du groupe:**  [Voir plus](https://github.com/josoavj/tpAlgoML_M1/blob/master/README.md)
- **Notice :** Veuillez ouvrir les fichier ".ipynb" dans [Google Collab](https://colab.research.google.com/)

## Réponses aux questions

## Exercice 1: Classification - Etude du Dataset Iris

1. Description du dataset Iris: 
   - C'est une classification des fleurs d'Iris selon leurs sépales et pétales.
   - **Origine:** Exemple d'application de l'analyse discriminante linéaire à partir du fleur d'Iris de trois espèces. 
   - Les trois espèces d'Iris sont:
     - Setosa
     - Versicolor
     - Virginica
   - **Variables:** 
     - Largeur sépale, 
     - Longeur sépale, 
     - Largeur pétale, 
     - Longueur pétale, 
     - Espèce
   - **Objectif d'étude:** Classification des fleurs d'Iris selon leurs espèces respectives en fonction de leurs sépales et pétales.

2. Visualisation pour explorer les relations entre les variables:

   ![Visuel](https://github.com/josoavj/tpAlgoML_M1/blob/master/TP2/assets/IrisVisual.png)

3. Discussion des observations importantes à partir des visualisations:
   Cette visualisation représente la distribution des différentes espèces de la dataset Iris en fonction de la *longueur des sépales* (SepalLengthCm) et de leur *largeur* (SepalWidthCm). Voici les principales observations :
   1. *Classification par espèce :*
       - Les points *bleus* représentent Iris-setosa, *verts* pour Iris-versicolor, et *rouges* pour Iris-virginica.
       - Les couleurs montrent que Iris-setosa se distingue nettement des deux autres espèces, formant un groupe séparé (à gauche, avec des sépales courts mais larges).

   2. *Chevauchement des espèces :*
       - Les points verts (Iris-versicolor) et rouges (Iris-virginica) se chevauchent partiellement, suggérant que ces deux espèces ont des caractéristiques de sépales plus similaires que celles de Iris-setosa.

   3. *Tendances générales :*
      - Iris-setosa a généralement des sépales plus courts (autour de 4,5 à 5,5 cm) et plus larges (entre 3 et 4,5 cm).
      - Iris-versicolor a des sépales de longueur intermédiaire (5,5 à 7 cm) et de largeur légèrement plus étroite (2,5 à 3,5 cm).
      - Iris-virginica a les sépales les plus longs (6 à 8 cm) mais pas nécessairement les plus larges (2 à 3,5 cm).
   4. Cette visualisation illustre bien les différences morphologiques entre les trois espèces, avec une séparation nette pour Iris-setosa mais un chevauchement pour Iris-versicolor et Iris-virginica

4. Application de deux modèles de classification au dataset Iris:
   - Après l'application de la Régression logistique:  
     ![RegLinear](https://github.com/josoavj/tpAlgoML_M1/blob/master/TP2/assets/Regression%20logistique.png)
   - Recherche de K (KNearest Neighbour):
   
     ![K](https://github.com/josoavj/tpAlgoML_M1/blob/master/TP2/assets/Recherche%20de%20k.png)
   - Après l'application de KNN sur le modèle:
     
     ![KNN](https://github.com/josoavj/tpAlgoML_M1/blob/master/TP2/assets/KNN.png)

5. Comparaison des performances des deux modèles: 
   - En utilisant la régression logistique, on a pu avoir une précision (Accuracy) de 97,78
   - Puis en utilisant KNN, on a pu avoir une précision (Accuracy) de 100%
   - **Conclusion:** On conclue que la meilleure option est d'utiliser KNN

## Exercice 2: Clustering – Données INSTAT

1. Introduction des données fournies: 
   - **Structure:** Tableau
   - **Organisation:** Les données sont divisées par catégories telles que "Urbain" et "Rural", 
   puis par genre ("Masculin", "Feminin", etc.), et incluent des sous-sections basées sur des quintiles de bien-être économique.
   - **Variables:**
     - Région
     - Données Urbaines
     - Données Rurales
     - Quintiles économiques
   - **Interêt:** 
     - Analyse socio-économique : Les données permettent de comparer les caractéristiques démographiques et économiques entre régions, zones urbaines et rurales.
     - Visualisation régionale : Comparaison des zones selon les indicateurs fournis.
   