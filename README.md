# Candy Crush

> Projet ISN S2
>
> Groupe :
>
> - Matthieu
> - Théo
> - Arthur

Pour le moment, nous allons partir sur le niveau 1, mais on va surement rajouter des petites améliorations dans le résultat final.

Convention pour la grille :

- Le premier caractère donne la couleur, "_" si case vide ou "r" si bonbon arc-en-ciel

- Le deuxième caractère donne le bonnus, "_" si aucun

- Les bonus sons : v - vertical / h - horizontal / p - explosif

Exemple :

- "0_" le bonbon est normal de la première couleur

- "2v" le bonbon à un bonus vertical et est de la deuxème couleur

- "r_" c'est un bonbon arc-en-ciel, par convention on met sa couleur à "r" et on ne lui met pas de bonus

- "__" est une case vide

## Algorithme en pseudo code

L'algorithme suivant sera ensuite placé dans la fonction `candy_crush`.

```txt
Charger la grille depuis le fichier csv
Afficher la grille
Tant que le jeu n'est pas bloqué et que l'utilisateur n'a pas atteint le nombre max d'iter :
    Demander à l'utilisateur un mouvement
    Jouer le coup
    Enlever 1 aux coups restants
    Tant que la grille n'est pas stable :
        Calculer la nouvelle grille
        Afficher la grille
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
| charger_grille             | Tout le monde            | Oui     |
| jeu_est_bloque             | Matthieu                 | Oui     |
| afficher_grille            | Arthur                   | Oui     |
| demander_mouvement         | Théo                     | Oui     |
| echanger_deux_bonbons      | Matthieu                 | Oui     |
| grille_est_stable          | Théo                     | Oui     |
| calculer_nouvelle_grille   | Arthur                   | Oui     |
| dupliquer_grille           | Théo                     | Oui     |
| supprimer_bonbons_en_ligne | Matthieu                 | Oui     |
| appliquer_gravite          | Théo                     | Oui     |
| ajouter_bonbons_aleatoires | Arthur                   | Oui     |

## Sous tâches

### charger_grille

```py
def charger_grille(fichier: str) -> list[list[str]]:
    """
    Récupère la grille dans le fichier csv et la retourne sous forme de liste 2D de str

    Params:
        fichier (str) : le nom du fichier à charger

    Returns:
        grille (liste 2D) : liste 2D de str

    """
```

### jeu_est_bloque

```py
def jeu_est_bloque(grille):
    """
    Analyse la grille est renvoie True si grille bloquée, False sinon (non bloquée)

    Params:
        grille (liste 2D) : grille du jeu à analyser

    Returns:
        bloque (bool) : True si grille bloquée, False grille non bloquée
    """
```

### afficher_grille

```py
def afficher_grille(grille):
    """
    Réalise l'affichage dans le terminal de la liste 2D mis en paramètre.

    Params:
        grille (liste 2D) : liste 2D de str

    Returns:

    """
```

### demander_mouvement

```py
def demander_mouvement():
    """
    Demande à l'utilisateur le mouvement qu'il veut réaliser pour bouger deux bonbons

    Params:

    Returns:
        pos_i (int, int) : liste de deux entiers pour les coordonnées initiales du bonbon à déplacer
        pos_f (int, int) : liste de deux entiers pour les coordonnées finales du bonbon à déplacer

    """
```

### echanger_deux_bonbons

```py
def echanger_deux_bonbons(grille, pos_i, pos_f):
    """
    Modifie la grille pour échanger les deux bonbons sélectionnés par l'utilisateur

    Params:
        grille (liste 2D) : liste 2D de str
        pos_i (int, int) : position en x et y du bonbon à échanger.
        pos_f (int, int) : position en x et y d'arrivée du bonbon.

    Returns:

    """
```

### grille_est_stable

```py
def grille_est_stable(grille, nouvelle_grille) :
    """
    Vérifie qu'il n'y a pas plus de mouvements possible après le remplissage de la grille par de nouveaux bonbons en comparant les deux dernières grilles

    Params:
        grille (liste 2D) : liste 2D de str représentant la grille actuelle
        nouvelle_grille (liste 2D) : liste 2D de str représentant la nouvelle grille

    Returns:
        est_stable (boolean) : True si elles sont identiques et False sinon

    """
```

### calculer_nouvelle_grille

```py
def calculer_nouvelle_grille(grille: list[list[int]], nb_type_bonbons: int) -> list[list[int]]:
    """
    Applique les transformations sur la grille, jusqu'à ce qu'elle soit stable et renvoie la nouvelle

    Params:
        grille (liste 2D) : la grille d'origine
        nb_type_bonbons (int) : nombre de types de bonbons possibles

    Returns:
        nouvelle_grille (liste 2D) : copie de la grille d'origine avec transformations

    """
```

### dupliquer_grille

```py
def dupliquer_grille(grille: list[list[int]]) -> list[list[int]]:
    """
    Créé une nouvelle grille identique à la première

    Params:
        grille (liste 2D) : la grille d'origine

    Returns:
        nouvelle_grille (liste 2D) : copie de la grille d'origine

    """
```

### supprimer_bonbons_en_ligne

```py
def supprimer_bonbons_en_ligne(grille: list[list[int]]) -> list[list[int]]:
    """
    Duplique la grille et supprime tous les bonbons formant une ligne verticale ou horizontale d'au moins 3 bonbons alignés. Supprime les bonbons par rapport à la grille de référence qui à été dupliqué. Retourne la nouvelle grille sans les bonbons formant des lignes

    Params:
        grille (liste 2D) : la grille d'origine

    Returns:
        nouvelle_grille (liste 2D) : la grille sans les bonbons formant des lignes

    """
```

### appliquer_gravite

```py
def appliquer_gravite(grille: list[list[int]]):
    """
    Modifie la grille donnée pour faire descendre tout les bonbons avec des emplacements vide en dessous comme si l'on appliquait la gravité à la grille

    Params:
        grille (liste 2D) : la grille 2D de bonbons

    Returns:

    """
```

### ajouter_bonbons_aleatoires

```py
def ajouter_bonbons_aleatoires(grille: list[list[int]], nb_type_bonbons):
    """
    Modifie la grille donnée pour ajouter des bonbons aléatoires aux emplacements vides

    Params:
        grille (liste 2D) : la grille 2D de bonbons
        nb_type_bonbons (int) : nombre de types de bonbons possibles

    Returns:

    """
```
