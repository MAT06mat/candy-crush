from random import choice
from random import randint


liste_2d = list[list[str]]


def charger_fichier(fichier: str) -> liste_2d:
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
                # Si numéro seul, on met un _ pour la convention
                if len(numero) == 1:
                    ligne.append(numero + "_")
                # Sinon on ajoute l'élément à la liste
                else:
                    ligne.append(numero)
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
            couleurs = "012345"[0:nb_couleurs]

            if x >= 2:
                if ligne[x - 2][0] == ligne[x - 1][0]:
                    couleurs = couleurs.replace(ligne[x - 1][0], "")

            if y >= 2:
                if grille[y - 2][x][0] == grille[y - 1][x][0]:
                    couleurs = couleurs.replace(grille[y - 1][x][0], "")

            ligne.append(choice(couleurs) + "_")
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
        print(*ligne)


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
        grille (liste 2D) : la grille 2D de bonbons

    Returns:

    """
    for j in range(len(grille[0])):
        for i in range(len(grille) - 1):
            if grille[i + 1][j][0] == "_":
                for k in range(i + 1, 0, -1):
                    echanger_deux_bonbons(grille, [j, k - 1], [j, k])


def obtenir_zone_speciale(grille, x, y, bonbon):
    zone_impactee = []
    hauteur = len(grille)
    largeur = len(grille[0])

    if bonbon[1] == "v":
        for i in range(hauteur):
            zone_impactee.append((x, i))

    elif bonbon[1] == "h":
        for i in range(largeur):
            zone_impactee.append((i, y))

    elif bonbon[1] == "p":
        for i in range(max(0, y - 1), min(hauteur, y + 2)):
            for j in range(max(0, x - 1), min(largeur, x + 2)):
                zone_impactee.append((j, i))

    return zone_impactee


def obtenir_alignement_horizontal(grille, x, y):
    # Cherche tous les bonbons identiques à gauche et à droite de (x, y)
    couleur = grille[y][x][0]
    alignement = [(x, y)]

    # Vers la gauche
    nx = x - 1
    while nx >= 0 and grille[y][nx][0] == couleur:
        alignement.append((nx, y))
        nx -= 1

    # Vers la droite
    nx = x + 1
    while nx < len(grille[0]) and grille[y][nx][0] == couleur:
        alignement.append((nx, y))
        nx += 1

    if len(alignement) < 3:
        alignement = []

    return alignement


def obtenir_alignement_vertical(grille, x, y):
    # Cherche tous les bonbons identiques en haut et en bas de (x, y)
    couleur = grille[y][x][0]
    alignement = [(x, y)]

    # Vers le haut
    ny = y - 1
    while ny >= 0 and grille[ny][x][0] == couleur:
        alignement.append((ny, x))  # Attention : format (x, y) pour cohérence
        alignement[-1] = (x, ny)  # Correction de l'ordre
        ny -= 1

    # Vers le bas
    ny = y + 1
    while ny < len(grille) and grille[ny][x][0] == couleur:
        alignement.append((x, ny))
        ny += 1

    if len(alignement) < 3:
        alignement = []

    return alignement


def supprimer_bonbons_en_ligne(grille: liste_2d, pos_i=None, pos_f=None):
    """
    Supprime tous les bonbons formant une ligne verticale ou horizontale d'au moins 3 bonbons alignés
    Supprime les bonbons par rapport à la grille de référence qui à été dupliqué.
    Retourne la nouvelle grille sans les bonbons formant des lignes (ils sont remplacés par des "__")
    Retourne aussi un booléen indiquant si la grille à été modifiée.

    Params:
        grille (liste 2D) : la grille d'origine
        pos_i (list[int] | None) : position du bonbon à échanger
        pos_f (list[int] | None) : position du bonbon échangé

    Returns:
        nouvelle_grille (liste 2D) : la grille sans les bonbons formant des lignes

    """
    nouvelle_grille = dupliquer_grille(grille)

    hauteur = len(grille)
    largeur = len(grille[0])
    a_supprimer = set()
    # On utilise un dictionnaire pour ne garder qu'un seul bonus prioritaire
    # par zone de suppression (clé: coordonnée, valeur: type de bonbon)
    bonus_potentiels = {}

    colonnes_a_supprimer = set()
    lignes_a_supprimer = set()

    # Combinaison de bonus
    if pos_i and pos_f:
        xi, yi = pos_i
        xf, yf = pos_f

        if grille[yi][xi][1] in "vh" and grille[yf][xf][1] in "vh":
            grille[yi][xi] = grille[yi][xi][0] + "_"
            grille[yf][xf] = grille[yf][xf][0] + "_"

            # Supprimer ligne et colonne de la position finale
            colonnes_a_supprimer.add(xf)
            lignes_a_supprimer.add(yf)

        elif grille[yi][xi][1] == "p" and grille[yf][xf][1] == "p":
            grille[yi][xi] = grille[yi][xi][0] + "_"
            grille[yf][xf] = grille[yf][xf][0] + "_"

            # Supprimer carré de 5x5 avec la position finale comme centre
            for i in range(max(0, yf - 2), min(hauteur, yf + 3)):
                for j in range(max(0, xf - 2), min(largeur, xf + 3)):
                    a_supprimer.add((j, i))

        elif grille[yi][xi][1] in "vhp" and grille[yf][xf][1] in "vhp":
            grille[yi][xi] = grille[yi][xi][0] + "_"
            grille[yf][xf] = grille[yf][xf][0] + "_"

            # Supprimer 3 lignes et 3 colonnes avec pour centre la position finale
            colonnes_a_supprimer.add(xf - 1)
            colonnes_a_supprimer.add(xf)
            colonnes_a_supprimer.add(xf + 1)
            lignes_a_supprimer.add(yf - 1)
            lignes_a_supprimer.add(yf)
            lignes_a_supprimer.add(yf + 1)

    # Analyse des alignements verticaux et horizontaux
    for y in range(hauteur):
        for x in range(largeur):
            couleur_actuelle = grille[y][x][0]
            if couleur_actuelle == "_":
                continue

            if y in lignes_a_supprimer:
                a_supprimer.add((x, y))
            elif x in colonnes_a_supprimer:
                a_supprimer.add((x, y))

            h_match = obtenir_alignement_horizontal(grille, x, y)
            v_match = obtenir_alignement_vertical(grille, x, y)

            if not h_match and not v_match:
                continue

            couleur = grille[y][x][0]
            # La position où on va créer le bonus (priorité au clic de l'utilisateur)
            pos_creation = (x, y)
            if pos_f and (pos_f in h_match or pos_f in v_match):
                pos_creation = pos_f
            elif pos_i and (pos_i in h_match or pos_i in v_match):
                pos_creation = pos_i

            # --- DETECTION DES FORMES ---

            if len(h_match) >= 5:
                # Horizontal >= 5 -> Bonbon arc-en-ciel
                for coord in h_match:
                    a_supprimer.add(coord)
                    bonus_potentiels.pop(coord, None)

                bonus_potentiels[h_match[len(h_match) // 2]] = "r_"

            elif len(v_match) >= 5:
                # Vertical >= 5 -> Bonbon arc-en-ciel
                for coord in v_match:
                    a_supprimer.add(coord)
                    bonus_potentiels.pop(coord, None)

                bonus_potentiels[v_match[len(v_match) // 2]] = "r_"

            # Intersection (T, L, +) : match horizontal ET vertical
            elif h_match and v_match:
                for coord in h_match + v_match:
                    a_supprimer.add(coord)
                    bonus_potentiels.pop(coord, None)

                bonus_potentiels[(h_match[0][0], v_match[0][1])] = couleur + "p"

            # Ligne de 4 ou plus
            elif len(h_match) >= 4:
                # Horizontal >= 4 -> Bonbon à rayures Verticales
                if pos_creation not in a_supprimer:
                    bonus_potentiels[pos_creation] = couleur + "v"

                for coord in h_match:
                    a_supprimer.add(coord)

            elif len(v_match) >= 4:
                # Vertical >= 4 -> Bonbon à rayures Horizontales
                if pos_creation not in a_supprimer:
                    bonus_potentiels[pos_creation] = couleur + "h"

                for coord in v_match:
                    a_supprimer.add(coord)

            # Match de 3 simple
            else:
                for coord in h_match + v_match:
                    a_supprimer.add(coord)

    # Gestion des réactions en chaîne
    deja_traites = set()
    doit_analyser = True
    while doit_analyser:
        nouveaux = set()
        for x, y in a_supprimer:
            if (x, y) not in deja_traites:
                bonbon = grille[y][x]
                if len(bonbon) > 1 and bonbon[1] in "vhp":
                    zone = obtenir_zone_speciale(grille, x, y, bonbon)
                    for c in zone:
                        if c not in a_supprimer:
                            nouveaux.add(c)
                deja_traites.add((x, y))

        if len(nouveaux) == 0:
            doit_analyser = False
        else:
            a_supprimer.update(nouveaux)

    for x, y in a_supprimer:
        nouvelle_grille[y][x] = "__"

    # On place les bonus. On vérifie que la position du bonus
    # n'a pas été elle-même soufflée par une réaction en chaîne.
    for pos, type_bonus in bonus_potentiels.items():
        nouvelle_grille[pos[1]][pos[0]] = type_bonus

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
                    if g[y - 2][x + 1][0] == g[y - 1][x + 1][0] == g[y][x][0]:
                        return False
                # Ligne verticale milieu
                if y - 1 >= 0 and y + 1 < h_g:
                    if g[y - 1][x + 1][0] == g[y][x][0] == g[y + 1][x + 1][0]:
                        return False
                # Ligne verticale en bas
                if y + 2 < h_g:
                    if g[y][x][0] == g[y + 1][x + 1][0] == g[y + 2][x + 1][0]:
                        return False
                # Ligne horizontale à droite
                if x + 3 < w_g:
                    if g[y][x][0] == g[y][x + 2][0] == g[y][x + 3][0]:
                        return False
                # 2) Bonbon échangé vers la gauche
                # Ligne verticale en haut
                if y - 2 >= 0:
                    if g[y - 2][x][0] == g[y - 1][x][0] == g[y][x + 1][0]:
                        return False
                # Ligne verticale milieu
                if y - 1 >= 0 and y + 1 < h_g:
                    if g[y - 1][x][0] == g[y][x + 1][0] == g[y + 1][x][0]:
                        return False
                # Ligne verticale en bas
                if y + 2 < h_g:
                    if g[y][x + 1][0] == g[y + 1][x][0] == g[y + 2][x][0]:
                        return False
                # Ligne horizontale à gauche
                if x - 2 < w_g:
                    if g[y][x + 1][0] == g[y][x - 1][0] == g[y][x - 2][0]:
                        return False
            # Échange vers le bas
            if y + 1 < h_g:
                # 1) Bonbon échangé vers le bas
                # Ligne horizontale à droite
                if x + 2 < w_g:
                    if g[y][x][0] == g[y + 1][x + 1][0] == g[y + 1][x + 2][0]:
                        return False
                # Ligne horizontale milieu
                if x - 1 >= 0 and x + 1 < w_g:
                    if g[y + 1][x - 1][0] == g[y][x][0] == g[y + 1][x + 1][0]:
                        return False
                # Ligne horizontale à gauche
                if x - 2 >= 0:
                    if g[y + 1][x - 2][0] == g[y + 1][x - 1][0] == g[y][x][0]:
                        return False
                # Ligne verticale en bas
                if y + 3 < h_g:
                    if g[y][x][0] == g[y + 2][x][0] == g[y + 3][x][0]:
                        return False
                # 2) Bonbon échangé vers le haut
                # Ligne horizontale à droite
                if x + 2 < w_g:
                    if g[y + 1][x][0] == g[y][x + 1][0] == g[y][x + 2][0]:
                        return False
                # Ligne horizontale milieu
                if x - 1 >= 0 and x + 1 < w_g:
                    if g[y][x - 1][0] == g[y + 1][x][0] == g[y][x + 1][0]:
                        return False
                # Ligne horizontale à gauche
                if x - 2 >= 0:
                    if g[y][x - 2][0] == g[y][x - 1][0] == g[y + 1][x][0]:
                        return False
                # Ligne verticale en haut
                if y - 2 >= 0:
                    if g[y - 2][x][0] == g[y - 1][x][0] == g[y + 1][x][0]:
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
        while j < len(grille) and grille[j][i] == "__":
            grille[j][i] = str(randint(0, nb_type_bonbons - 1)) + "_"
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
    g = charger_fichier("data/exemple_grille.csv")
    afficher_grille(g)
