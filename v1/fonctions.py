from random import choice
from random import randint
from matplotlib import pyplot as plt


liste_2d = list[list[int]]


def charger_fichier(fichier: str) -> liste_2d:
    """
    Récupère la grille dans le fichier csv et la retourne sous forme de liste 2D d'entiers

    Params:
        fichier (str) : le nom du fichier à charger

    Returns:
        grille (liste 2D) : liste 2D de str

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


def generer_grille(m: int, n: int, nb_couleurs: int = 4) -> liste_2d:
    """
    Génère une grille de hauteur m et de largeur n avec nb_couleurs au max et retourne cette grille sous forme de liste 2D d'entiers

    Params:
        m (int) : hauteur de la grille
        n (int) : largeur de la grille
        nb_couleurs (int) : nombre maxmimum de couleur différentes dans la grille

    Returns:
        grille (liste 2D) : liste 2D d'entiers

    """

    if m < 3 or n < 3:
        raise ValueError("Le nombre minimum de ligne et de colonne est 2")

    if nb_couleurs < 3 or nb_couleurs > 6:
        raise ValueError(
            "Le nombre min de couleurs pour une grille est 3 et le max est 6"
        )

    grille = []
    for y in range(m):
        ligne = []
        for x in range(n):
            couleurs = list(range(n))

            if x >= 2:
                if ligne[x - 2] == ligne[x - 1] and ligne[x - 1] in couleurs:
                    couleurs.remove(ligne[x - 1])

            if y >= 2:
                if (
                    grille[y - 2][x] == grille[y - 1][x]
                    and grille[y - 1][x] in couleurs
                ):
                    couleurs.remove(grille[y - 1][x])

            ligne.append(choice(couleurs))
        grille.append(ligne)
    return grille


def echanger_deux_bonbons(grille: liste_2d, pos_i, pos_f):
    """
    Modifie la grille pour échanger les deux bonbons sélectionnés par l'utilisateur

    Params:
        pos_i (int, int) : position en x et y du bonbon à échanger.
        pos_f (int, int) : position en x et y d'arrivée du bonbon.

    Returns:

    """

    x_i, y_i = pos_i
    x_f, y_f = pos_f

    grille[y_i][x_i], grille[y_f][x_f] = grille[y_f][x_f], grille[y_i][x_i]


def afficher_grille(grille: liste_2d, nb_type_bonbons: int):
    """
    Affiche la grille de jeu "grille" contenant au maximum nb_type_bonbons (
    entier) couleurs de bonbons différentes. Les bonbons sont codés entre
    et nb_type_bonbons-1.

    Params:
        grille (liste 2D) : liste 2D de int
        nb_type_bonbons (int) : nombre de types de bonbons possibles

    Returns:
        None

    """

    plt.imshow(grille, vmin=0, vmax=nb_type_bonbons - 1, cmap="jet")
    plt.draw()  # force l'affichage immédiat
    plt.pause(0.2)


def demander_mouvement():
    """
    Demande à l'utilisateur le mouvement qu'il veut réaliser pour bouger deux bonbons

    Params:

    Returns:
        (pos_i, pos_f) ((int, int), (int, int)) :
        - liste des deux positions contenant deux entiers pour les coordonnées initiales et finales du bonbon à déplacer

    """
    pos_i = []
    pos_f = []

    # on entre l'abscisse du bonbon qu'on souhaite échanger
    colone_i = input("Entrez la colonne du bonbon que vous voulez changer de place : ")
    pos_i.append(int(colone_i))
    # on entre l'ordonné du bonbon qu'on souhaite changer
    ligne_i = input("Entrez la ligne du bonbon que vous voulez changer de place : ")
    pos_i.append(int(ligne_i))
    # on entre l'abscisse de la case qu'on vise
    colone_f = input("Entrez la colonne du bonbon avec lequel vous voulez échanger : ")
    pos_f.append(int(colone_f))
    # on entre l'ordonné de la case qu'on vise
    ligne_f = input("Entrez la ligne du bonbon avec lequel vous voulez échanger : ")
    pos_f.append(int(ligne_f))

    return pos_i, pos_f


def grille_est_stable(grille: liste_2d, nouvelle_grille: liste_2d) -> bool:
    """
    Vérifie qu'il n'y a pas plus de mouvements possible après le remplissage de la grille par de nouveaux bonbons en comparant les deux dernières grilles

    Params:
        grille (liste 2D) : liste 2D d'entiers représentant la grille actuelle
        nouvelle_grille (liste 2D) : liste 2D d'entiers représentant la nouvelle grille

    Returns:
        est_stable (boolean) : True si elles sont identiques et False sinon

    """
    est_stable = False
    # On compare à la nouvelle grille créer : si elle est identique, c'est que la grille est stable
    if grille == nouvelle_grille:
        est_stable = True
    return est_stable


def dupliquer_grille(grille: liste_2d) -> liste_2d:
    """
    Créé une nouvelle grille identique à la première

    Params:
        grille (liste 2D) : la grille d'origine

    Returns:
        nouvelle_grille (liste 2D) : copie de la grille d'origine

    """
    nouvelle_grille = []
    for i in range(len(grille)):
        ligne = []
        for j in range(len(grille[i])):
            ligne.append(grille[i][j])
        nouvelle_grille.append(ligne)
    return nouvelle_grille


def appliquer_gravite(grille: liste_2d):
    """
    Modifie la grille donnée pour faire descendre tout les bonbons avec des emplacements vide en dessous comme si l'on appliquait la gravité à la grille

    Params:
        grille (liste 2D) : la grille 2D d'entiers

    Returns:

    """
    for j in range(len(grille[0])):
        for i in range(len(grille) - 1):
            if grille[i + 1][j] == -1:
                for k in range(i + 1, 0, -1):
                    echanger_deux_bonbons(grille, [j, k - 1], [j, k])


def obtenir_alignement_horizontal(grille, x, y):
    """Retourne la liste des coordonnées (x, y) des bonbons alignés horizontalement."""

    # Cherche tous les bonbons identiques à gauche et à droite de (x, y)
    couleur = grille[y][x]
    alignement = [(x, y)]

    # Vers la gauche
    nx = x - 1
    while nx >= 0 and grille[y][nx] == couleur:
        alignement.append((nx, y))
        nx -= 1

    # Vers la droite
    nx = x + 1
    while nx < len(grille[0]) and grille[y][nx] == couleur:
        alignement.append((nx, y))
        nx += 1

    if len(alignement) < 3:
        alignement = []

    return alignement


def obtenir_alignement_vertical(grille, x, y):
    """Retourne la liste des coordonnées (x, y) des bonbons alignés verticalement."""

    # Cherche tous les bonbons identiques en haut et en bas de (x, y)
    couleur = grille[y][x]
    alignement = [(x, y)]

    # Vers le haut
    ny = y - 1
    while ny >= 0 and grille[ny][x] == couleur:
        alignement.append((ny, x))  # Attention : format (x, y) pour cohérence
        alignement[-1] = (x, ny)  # Correction de l'ordre
        ny -= 1

    # Vers le bas
    ny = y + 1
    while ny < len(grille) and grille[ny][x] == couleur:
        alignement.append((x, ny))
        ny += 1

    if len(alignement) < 3:
        alignement = []

    return alignement


def test_bonbon_alignee(grille: liste_2d):
    nouvelle_grille, bonbons_supprimes = supprimer_bonbons_en_ligne(grille)
    return not grille_est_stable(grille, nouvelle_grille)


# complexité n^3
def supprimer_bonbons_en_ligne(grille: liste_2d):
    """
    Supprime tous les bonbons dans une nouvelle grille, formant une ligne verticale ou horizontale d'au moins 3 bonbons alignés
    Supprime les bonbons par rapport à la grille de référence qui à été dupliqué.
    Retourne la nouvelle grille sans les bonbons formant des lignes (ils sont remplacés par des -1)

    Params:
        grille (liste 2D) : la grille d'origine

    Returns:
        nouvelle_grille (liste 2D) : la grille sans les bonbons formant des lignes
        total_bonbons_supprimes (int) : le total de bonbons supprimés

    """
    nouvelle_grille = dupliquer_grille(grille)
    hauteur = len(grille)
    largeur = len(grille[0])
    total_bonbons_supprimes = 0

    # Analyse des alignements verticaux et horizontaux
    for y in range(hauteur):
        for x in range(largeur):
            h_match = obtenir_alignement_horizontal(grille, x, y)
            v_match = obtenir_alignement_vertical(grille, x, y)

            if not h_match and not v_match:
                continue

            for c in h_match + v_match:
                if nouvelle_grille[c[1]][c[0]] != -1:
                    nouvelle_grille[c[1]][c[0]] = -1
                    total_bonbons_supprimes += 1

    return nouvelle_grille, total_bonbons_supprimes


def jeu_est_bloque(grille: liste_2d) -> bool:
    """
    Analyse la grille est renvoie True si grille bloquée, False sinon (non bloquée)

    Params:
        grille (liste 2D) : grille du jeu à analyser

    Returns:
        bloque (bool) : True si grille bloquée, False grille non bloquée
    """
    # Création de raccourcis pour le reste du code
    g = grille
    w_g = len(g[0])
    h_g = len(g)

    # Pour chaque bonbon, on test son échange avec un bonbon à droite et un bonbon en dessous
    for y in range(h_g):
        for x in range(w_g):
            # Échange vers la droite
            if x + 1 < w_g:
                # 1) Bonbon échangé vers la droite
                # Ligne verticale en haut
                if y - 2 >= 0:
                    if g[y - 2][x + 1] == g[y - 1][x + 1] == g[y][x]:
                        return False
                # Ligne verticale milieu
                if y - 1 >= 0 and y + 1 < h_g:
                    if g[y - 1][x + 1] == g[y][x] == g[y + 1][x + 1]:
                        return False
                # Ligne verticale en bas
                if y + 2 < h_g:
                    if g[y][x] == g[y + 1][x + 1] == g[y + 2][x + 1]:
                        return False
                # Ligne horizontale à droite
                if x + 3 < w_g:
                    if g[y][x] == g[y][x + 2] == g[y][x + 3]:
                        return False
                # 2) Bonbon échangé vers la gauche
                # Ligne verticale en haut
                if y - 2 >= 0:
                    if g[y - 2][x] == g[y - 1][x] == g[y][x + 1]:
                        return False
                # Ligne verticale milieu
                if y - 1 >= 0 and y + 1 < h_g:
                    if g[y - 1][x] == g[y][x + 1] == g[y + 1][x]:
                        return False
                # Ligne verticale en bas
                if y + 2 < h_g:
                    if g[y][x + 1] == g[y + 1][x] == g[y + 2][x]:
                        return False
                # Ligne horizontale à gauche
                if x - 2 < w_g:
                    if g[y][x + 1] == g[y][x - 1] == g[y][x - 2]:
                        return False
            # Échange vers le bas
            if y + 1 < h_g:
                # 1) Bonbon échangé vers le bas
                # Ligne horizontale à droite
                if x + 2 < w_g:
                    if g[y][x] == g[y + 1][x + 1] == g[y + 1][x + 2]:
                        return False
                # Ligne horizontale milieu
                if x - 1 >= 0 and x + 1 < w_g:
                    if g[y + 1][x - 1] == g[y][x] == g[y + 1][x + 1]:
                        return False
                # Ligne horizontale à gauche
                if x - 2 >= 0:
                    if g[y + 1][x - 2] == g[y + 1][x - 1] == g[y][x]:
                        return False
                # Ligne verticale en bas
                if y + 3 < h_g:
                    if g[y][x] == g[y + 2][x] == g[y + 3][x]:
                        return False
                # 2) Bonbon échangé vers le haut
                # Ligne horizontale à droite
                if x + 2 < w_g:
                    if g[y + 1][x] == g[y][x + 1] == g[y][x + 2]:
                        return False
                # Ligne horizontale milieu
                if x - 1 >= 0 and x + 1 < w_g:
                    if g[y][x - 1] == g[y + 1][x] == g[y][x + 1]:
                        return False
                # Ligne horizontale à gauche
                if x - 2 >= 0:
                    if g[y][x - 2] == g[y][x - 1] == g[y + 1][x]:
                        return False
                # Ligne verticale en haut
                if y - 2 >= 0:
                    if g[y - 2][x] == g[y - 1][x] == g[y + 1][x]:
                        return False
    return True


def ajouter_bonbons_aleatoires(grille: liste_2d, nb_type_bonbons: int):
    """
    Modifie la grille donnée pour ajouter des bonbons aléatoires aux emplacements vides

    Params:
        grille (liste 2D) : la grille 2D d'entiers
        nb_type_bonbons (int) : nombre de types de bonbons possibles

    Returns:

    """
    # Parcours de chaque colonne
    for i in range(len(grille[0])):
        j = 0
        # Ajout de bonbons dans la colonne i dans les emplacements vides (dans les premières positions)
        while j < len(grille) and grille[j][i] == -1:
            grille[j][i] = randint(0, nb_type_bonbons - 1)
            j += 1


def calculer_nouvelle_grille(grille: liste_2d, nb_type_bonbons: int) -> liste_2d:
    """
    Supprime les bonbons en ligne, fait tomber les bonbons et complète les trous avec des nouveaux bonbons
    Renvoie la nouvelle grille et le nombre de bonbons supprimés

    Params:
        grille (liste 2D) : la grille d'origine
        nb_type_bonbons (int) : nombre de types de bonbons possibles

    Returns:
        nouvelle_grille (liste 2D) : la grille transformée
        bonbons_supprimes (int) : nombre de bonbons supprimés

    """
    nouvelle_grille, bonbons_supprimes = supprimer_bonbons_en_ligne(grille)
    appliquer_gravite(nouvelle_grille)
    ajouter_bonbons_aleatoires(nouvelle_grille, nb_type_bonbons)
    return nouvelle_grille, bonbons_supprimes


if __name__ == "__main__":
    g = charger_fichier("data/exemple_grille.csv")

    nb_type_bonbons = 6
    afficher_grille(g, nb_type_bonbons)
    input()
