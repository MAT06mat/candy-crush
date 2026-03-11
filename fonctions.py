from random import choice
from copy import deepcopy


def charger_grille(fichier: str):
    """
    Récupère la grille dans le fichier csv et la retourne sous forme de liste 2D d'entiers

    Params:
        - fichier (str) : le nom du fichier à charger

    Return:
        - grille (liste 2D) : liste 2D d'entiers

    """

    grille = []
    with open(fichier, "r", encoding="UTF-8") as f:
        for ligne_str in f.read().split("\n"):
            ligne = []
            for numero in ligne_str.split():
                ligne.append(int(numero))
            if len(ligne):
                grille.append(ligne)
    return grille


def generer_grille(m: int, n: int, nb_couleurs: int = 4):
    """
    Génère une grille de hauteur m et de largeur n avec nb_couleurs au max et retourne cette grille sous forme de liste 2D

    Params:
        - m (int) : hauteur de la grille
        - n (int) : largeur de la grille
        - nb_couleurs (int) : nombre maxmimum de couleur différentes dans la grille

    Return:
        - grille (liste 2D) : liste 2D d'entiers

    """

    if m < 3 or n < 3:
        raise ValueError("Le nombre minimum de ligne et de colonne est 2")

    if nb_couleurs < 3:
        raise ValueError("Le nombre minimum de couleurs pour une grille est 3")

    grille = []
    for y in range(m):
        ligne = []
        for x in range(n):
            colors = list(range(nb_couleurs))

            if x >= 2 and ligne[x - 1] in colors:
                if ligne[x - 2] == ligne[x - 1]:
                    colors.remove(ligne[x - 1])

            if y >= 2 and grille[y - 1][x] in colors:
                if grille[y - 2][x] == grille[y - 1][x]:
                    colors.remove(grille[y - 1][x])

            ligne.append(choice(colors))
        grille.append(ligne)
    return grille


def echanger_deux_bonbons(grille, pos_i, pos_f):
    """
    Modifie la grille pour échanger les deux bonbons sélectionnés par l'utilisateur

    Params :
        - pos_i (int, int) : position en x et y du bonbon à échanger.
        - pos_f (int, int) : position en x et y d'arrivée du bonbon.

    Return :
        None.

    """

    x_i, y_i = pos_i
    x_f, y_f = pos_f

    grille[y_i][x_i], grille[y_f][x_f] = grille[y_f][x_f], grille[y_i][x_i]


def afficher_grille(grille):
    """
    Réalise l'affichage dans le terminal de la liste 2D mis en paramètre.

    Params :
        - grille (liste 2D) : liste 2D d'entiers

    Returns :
        None.
    """

    for ligne in grille:
        print(*ligne)


def supprimer_bonbons_en_ligne(grille: list[list[int]]) -> list[list[int]]:
    """
    Duplique la grille et supprime tous les bonbons formant une ligne verticale ou horizontale d'au moins 3 bonbons alignés. Supprime les bonbons par rapport à la grille de référence qui à été dupliqué. Retourne la nouvelle grille sans les bonbons formant des lignes

    Params:
        - grille (liste 2D) : la grille d'origine

    Return:
        - nouvelle_grille (liste 2D) : la grille sans les bonbons formant des lignes

    """
    # À remplacer par la fonction de copie de la grille
    nouvelle_grille = deepcopy(grille)

    for y in range(len(grille)):
        for x in range(len(grille[y])):
            if x >= 2:
                if grille[y][x - 2] == grille[y][x - 1] == grille[y][x]:
                    nouvelle_grille[y][x - 2] = -1
                    nouvelle_grille[y][x - 1] = -1
                    nouvelle_grille[y][x] = -1
            if y >= 2:
                if grille[y - 2][x] == grille[y - 1][x] == grille[y][x]:
                    nouvelle_grille[y - 2][x] = -1
                    nouvelle_grille[y - 1][x] = -1
                    nouvelle_grille[y][x] = -1
    return nouvelle_grille


if __name__ == "__main__":
    g = charger_grille("exemple_grille.csv")
    afficher_grille(g)
