from random import choice
from random import randint


liste_2d = list[list[int]]


def charger_grille(fichier: str) -> liste_2d:
    """
    Récupère la grille dans le fichier csv et la retourne sous forme de liste 2D d'entiers

    Params:
        fichier (str) : le nom du fichier à charger

    Returns:
        grille (liste 2D) : liste 2D d'entiers

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
    Génère une grille de hauteur m et de largeur n avec nb_couleurs au max et retourne cette grille sous forme de liste 2D

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


def afficher_grille(grille: liste_2d):
    """
    Réalise l'affichage dans le terminal de la liste 2D mis en paramètre.

    Params:
        grille (liste 2D) : liste 2D d'entiers

    Returns:

    """

    for ligne in grille:
        for i in ligne:
            print(i, end=" ")
        print()


def demander_mouvement():
    """
    Demande à l'utilisateur le mouvement qu'il veut réaliser pour bouger deux bonbons

    Params:

    Returns:
        pos_i (int, int) : liste de deux entiers pour les coordonnées initiales du bonbon à déplacer
        pos_f (int, int) : liste de deux entiers pour les coordonnées finales du bonbon à déplacer

    """
    pos_i = []
    pos_f = []
    pos_i.append(
        int(
            input("Entrez la colonne du bonbon que vous souhaitez changer de place : ")
        )  # on entre l'abscisse du bonbon qu'on souhaite échanger
    )
    pos_i.append(
        int(
            input("Entrez la ligne du bonbon que vous souhaitez changer de place : ")
        )  # on entre l'ordonné du bonbon qu'on souhaite changer
    )
    pos_f.append(
        int(input("Entrez la colonne du bonbon avec lequel vous voulez échanger : "))
    )  # on entre l'abscisse de la case qu'on vise
    pos_f.append(
        int(input("Entrez la ligne du bonbon avec lequel vous voulez échanger : "))
    )  # on entre l'ordonné de la case qu'on vise

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
    # On compare à la nouvelle grille créer : si elle est identique, c'est que la grille est
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
        grille (liste 2D) : la grille 2D de bonbons

    Returns:

    """
    for j in range(len(grille[0])):
        for i in range(len(grille) - 1):
            if grille[i + 1][j] == -1:
                for k in range(i + 1, 0, -1):
                    echanger_deux_bonbons(grille, [j, k - 1], [j, k])


def supprimer_bonbons_en_ligne(grille: liste_2d) -> liste_2d:
    """
    Duplique la grille et supprime tous les bonbons formant une ligne verticale ou horizontale d'au moins 3 bonbons alignés
    Supprime les bonbons par rapport à la grille de référence qui à été dupliqué.
    Retourne la nouvelle grille sans les bonbons formant des lignes (ils sont remplacés par des -1)

    Params:
        grille (liste 2D) : la grille d'origine

    Returns:
        nouvelle_grille (liste 2D) : la grille sans les bonbons formant des lignes

    """
    nouvelle_grille = dupliquer_grille(grille)

    for y in range(len(grille)):
        for x in range(len(grille[y])):
            if x >= 2 and grille[y][x - 2] == grille[y][x - 1] == grille[y][x]:
                nouvelle_grille[y][x - 2] = -1
                nouvelle_grille[y][x - 1] = -1
                nouvelle_grille[y][x] = -1
                # TODO
                # Si bonbon spécial, faire l'action
                # TODO
                # if x >= 4 and grille[y][x - 4] == grille[y][x - 3] == grille[y][x]:
                #     # Ajout du bonbon arc-en-ciel
                #     pass
                # elif x >= 3 and grille[y][x - 3] == grille[y][x]:
                #     # Ajout du bonbon -h
                #     pass
            if y >= 2 and grille[y - 2][x] == grille[y - 1][x] == grille[y][x]:
                nouvelle_grille[y - 2][x] = -1
                nouvelle_grille[y - 1][x] = -1
                nouvelle_grille[y][x] = -1
                # TODO
                # Si bonbon spécial, faire l'action
                # TODO
                # if y >= 4 and grille[y - 4][x] == grille[y - 3][x] == grille[y][x]:
                #     # Ajout du bonbon arc-en-ciel
                #     pass
                # elif y >= 3 and grille[y - 3][x] == grille[y][x]:
                #     # Ajout du bonbon -v
                #     pass
    return nouvelle_grille


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
                    if g[y][x] == g[y - 1][x + 1] == g[y - 1][x + 2]:
                        return False
                # Ligne horizontale milieu
                if x - 1 >= 0 and x + 1 < w_g:
                    if g[y - 1][x - 1] == g[y][x] == g[y - 1][x + 1]:
                        return False
                # Ligne horizontale à gauche
                if x - 2 >= 0:
                    if g[y - 1][x - 2] == g[y - 1][x - 1] == g[y][x]:
                        return False
                # Ligne verticale en bas
                if y - 3 < h_g:
                    if g[y][x] == g[y - 2][x] == g[y - 3][x]:
                        return False
                # 2) Bonbon échangé vers le haut
                # Ligne horizontale à droite
                if x + 2 < w_g:
                    if g[y + 1][x] == g[y][x + 1] == g[y + 1][x + 2]:
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
        grille (liste 2D) : la grille 2D de bonbons
        nb_type_bonbons (int) : nombre de types de bonbons possibles

    Returns:

    """
    for i in range(len(grille[0])):
        j = 0
        while j < len(grille) and grille[j][i] == -1:
            grille[j][i] = randint(0, nb_type_bonbons - 1)
            j += 1


def calculer_nouvelle_grille(grille: liste_2d, nb_type_bonbons: int) -> liste_2d:
    """
    Applique les transformations sur la grille, jusqu'à ce qu'elle soit stable et renvoie la nouvelle

    Params:
        grille (liste 2D) : la grille d'origine
        nb_type_bonbons (int) : nombre de types de bonbons possibles

    Returns:
        nouvelle_grille (liste 2D) : copie de la grille d'origine avec transformations

    """
    nouvelle_grille = supprimer_bonbons_en_ligne(grille)
    appliquer_gravite(nouvelle_grille)
    ajouter_bonbons_aleatoires(nouvelle_grille, nb_type_bonbons)
    return nouvelle_grille


if __name__ == "__main__":
    g = charger_grille("data/exemple_grille.csv")
    afficher_grille(g)
