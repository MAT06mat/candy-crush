from random import choice


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

    if nb_couleurs < 3:
        raise ValueError("Le nombre de couleurs minimum pour une grille est 3")

    grille = []
    for y in range(m):
        ligne = []
        for x in range(n):
            colors = list(range(nb_couleurs))
            if x >= 2 and ligne[x - 1] == ligne[x - 2]:
                colors.remove(ligne[x - 1])
            if (
                y >= 2
                and grille[y - 1][x] == grille[y - 2][x]
                and grille[y - 1][x] in colors
            ):
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


if __name__ == "__main__":
    g = charger_grille("exemple_grille.csv")
    afficher_grille(g)
