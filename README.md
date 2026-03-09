# candy-crush

Projet ISN S2

## Algorithme en pseudo code

```txt
Charger la grille depuis le fichier csv
Tant que le jeu n'est pas bloqué et que l'utilisateur n'a pas atteint le nombre max d'iter :
    Afficher la grille
    Demander à l'utilisateur un mouvement
    Jouer le coup
    Enlever 1 aux coups restants
    Tant que la grille n'est pas stable :
        Calculer la nouvelle grille
```

## Découpage fonctionnel

- M charger_grille
- A jeu_est_bloque
- T afficher_grille
- M demander_mouvement
- A echanger_deux_bonbons
- T grille_est_stable
- M calculer_nouvelle_grille

## Sous tâches

### charger_grille

```py
def charger_grille(fichier: str) -> list[list[int]]:
    """
    Récupère la grille dans le fichier csv et la retourne sous forme de liste 2D d'entiers

    Params:
        - fichier (str) : le nom du fichier à charger

    Return:
        - grille (liste 2D) : liste 2D d'entiers

    """
```

### jeu_est_bloque

```py
def jeu_est_bloque(grille):
    """
    Analyse la grille est renvoie True si grille bloquée, False sinon (non bloquée)

    Params :
        - grille (liste 2D) : grille du jeu à analyser

    Return :
        - bloquée (bool) : True si grille bloquée, False grille non bloquée
    """
```

### afficher_grille

```py
def afficher_grille(grille):
    """
    Réalise l'affichage dans le terminal de la liste 2D mis en paramètre.

    Params :
        - grille (liste 2D) : liste 2D d'entiers

    Returns :
        None.
    """
```

### demander_mouvement

```py
def demander_mouvement():
    """
    Demande à l'utilisateur le mouvement qu'il veut réaliser pour bouger deux bonbons

    Params:
        None.

    Return:
        - pos_i (int, int) : liste de deux entiers pour les coordonnées initiales du bonbon à déplacer
        - pos_f (int, int) : liste de deux entiers pour les coordonnées finales du bonbon à déplacer

    """
```

### echanger_deux_bonbons

```py
def echanger_deux_bonbons(grille, pos_i, pos_f):
    """
    Modifie la grille pour échanger les deux bonbons sélectionnés par l'utilisateur

    Params :
        - pos_i (int, int) : position en x et y du bonbon à échanger.
        - pos_f (int, int) : position en x et y d'arrivée du bonbon.

    Return :
        None.

    """
```

### grille_est_stable

```py
def grille_est_stable(grille, nouvelle_grille) :
    """
    Vérifie qu'il n'y a pas plus de mouvements possible après le remplissage de la grille par de nouveaux bonbons en comparant les deux dernières grilles

    Params :
        grille (liste 2D) : liste 2D d'entiers représentant la grille actuelle
        nouvelle_grille (liste 2D) : liste 2D d'entiers représentant la nouvelle grille

    Return :
        est_stable (boolean) : True si elles sont identiques et False sinon

    """
```

### calculer_nouvelle_grille

```py
def calculer_nouvelle_grille(grille: list[list[int]]) -> list[list[int]]:
    """
    Applique les transformations sur la grille et renvoie la nouvelle

    Params:
        - grille (liste 2D) : la grille d'origine

    Return:
        - nouvelle_grille (liste 2D) : copie de la grille d'origine avec transformations

    """
```
