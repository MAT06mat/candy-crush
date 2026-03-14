# Candy Crush

> Projet ISN S2
>
> Groupe :
>
> - Matthieu
> - Théo
> - Arthur

Pour le moment, nous allons partir sur le niveau 1, mais on va surement rajouter des petites améliorations dans le résultat final.

## Algorithme en pseudo code

L'algorithme suivant sera ensuite placé dans la fonction `candy_crush`.

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

Décomposition du calcul de la nouvelle grille :

```txt
Créer une nouvelle grille (duplication de la première)
Supprimer tous les bonbons qui forment une ligne de 3 par rapport à la première grille
Appliquer la gravité et descendre tous les bonbons volants
Remplir les emplacements vides par de nouveux bonbons aléatoires
```

## Découpage fonctionnel (liste des fonctions)

| Fonction                   | Chargé de la réalisation | Terminé |
| -------------------------- | ------------------------ | ------- |
| charger_grille             | Tout le monde            | Non     |
| jeu_est_bloque             | Matthieu                 | Oui     |
| afficher_grille            | Arthur                   | Oui     |
| demander_mouvement         | Théo                     | Non     |
| echanger_deux_bonbons      | Matthieu                 | Oui     |
| grille_est_stable          | Théo                     | Non     |
| calculer_nouvelle_grille   | Arthur                   | Non     |
| dupliquer_grille           | Théo                     | Non     |
| supprimer_bonbons_en_ligne | Matthieu                 | Oui     |
| appliquer_gravite          | Théo                     | Non     |
| ajouter_bonbons_aleatoires | Arthur                   | Non     |

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

### dupliquer_grille

```py
def dupliquer_grille(grille: list[list[int]]) -> list[list[int]]:
    """
    Créé une nouvelle grille identique à la première

    Params:
        - grille (liste 2D) : la grille d'origine

    Return:
        - nouvelle_grille (liste 2D) : copie de la grille d'origine

    """
```

### supprimer_bonbons_en_ligne

```py
def supprimer_bonbons_en_ligne(grille: list[list[int]]) -> list[list[int]]:
    """
    Duplique la grille et supprime tous les bonbons formant une ligne verticale ou horizontale d'au moins 3 bonbons alignés. Supprime les bonbons par rapport à la grille de référence qui à été dupliqué. Retourne la nouvelle grille sans les bonbons formant des lignes

    Params:
        - grille (liste 2D) : la grille d'origine

    Return:
        - nouvelle_grille (liste 2D) : la grille sans les bonbons formant des lignes

    """
```

### appliquer_gravite

```py
def appliquer_gravite(grille: list[list[int]]):
    """
    Modifie la grille donnée pour faire descendre tout les bonbons avec des emplacements vide en dessous comme si l'on appliquait la gravité à la grille

    Params:
        - grille (liste 2D) : la grille 2D de bonbons

    Return:
        None.

    """
```

### ajouter_bonbons_aleatoires

```py
def ajouter_bonbons_aleatoires(grille: list[list[int]]):
    """
    Modifie la grille donnée pour ajouter des bonbons aléatoires aux emplacements vides

    Params:
        - grille (liste 2D) : la grille 2D de bonbons

    Return:
        None.

    """
```
