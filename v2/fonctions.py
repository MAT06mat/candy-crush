from random import choice
from random import randint


liste_2d = list[list[str]]

dico_bonbon = {
    "0": "🍎",
    "1": "🍋",
    "2": "🥝",
    "3": "🍉",
    "4": "🍇",
    "5": "🍒",
    "r": "🎂",
    "_": "・",
}
dico_bonus = {"h": "-", "v": "|", "p": "+", "_": " "}


def charger_fichier(fichier: str) -> liste_2d:
    """
    Récupère la grille dans le fichier csv et la retourne sous forme de liste 2D de str

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
        grille (liste 2D) : liste 2D de str

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
        grille (liste 2D) : liste 2D de str
        dico_bonbon (dictionnaire) : dictionnaire associant chaque type de bonbon à son icône correspondante
        dico_bonus (dictionnaire) : dictionnaire associant chaque bonus à son caractère correspondant

    Returns:
        None

    """

    for ligne in grille:
        for bonbon in ligne:
            type_bonbon = bonbon[0]
            bonus_bonbon = bonbon[1]
            print(
                dico_bonus[bonus_bonbon]
                + dico_bonbon[type_bonbon]
                + dico_bonus[bonus_bonbon],
                end=" ",
            )
        print()
    print()
    print()


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
        grille (liste 2D) : liste 2D de str représentant la grille actuelle
        nouvelle_grille (liste 2D) : liste 2D de str représentant la nouvelle grille

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
    """Retourne la liste des coordonnées (x, y) des bonbons se trouvant dans une zonne spéciale."""

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
    """Retourne la liste des coordonnées (x, y) des bonbons alignés horizontalement."""

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
    """Retourne la liste des coordonnées (x, y) des bonbons alignés verticalement."""

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
    Supprime tous les bonbons dans une nouvelle grille, formant une ligne verticale ou horizontale d'au moins 3 bonbons alignés
    Supprime les bonbons par rapport à la grille de référence qui à été dupliqué.
    Retourne la nouvelle grille sans les bonbons formant des lignes (ils sont remplacés par des "__")
    Applique les interactions bonus entre les deux bonbons échangés, si les deux positions de ces bonbons sont mis en paramètre. Par exemple, si deux bonbons "v" ou "h" sont échangés, alors cela supprimera la ligne et la colonne de la position finale.

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

    # Gestion de combinaison de bonus
    if pos_i and pos_f:
        xi, yi = pos_i
        xf, yf = pos_f
        b1, b2 = grille[yi][xi], grille[yf][xf]

        # Cas Arc-en-ciel + Arc-en-ciel : On vide toute la grille
        if b1 == "r_" and b2 == "r_":
            grille[yi][xi] = "__"
            grille[yf][xf] = "__"

            for y in range(hauteur):
                for x in range(largeur):
                    a_supprimer.add((x, y))

        # Cas Arc-en-ciel + Autre bonbon
        elif b1 == "r_" or b2 == "r_":
            # On identifie lequel est l'arc-en-ciel et lequel est la cible
            cible = b2 if b1 == "r_" else b1
            couleur_cible = cible[0]
            type_special_cible = cible[1] if len(cible) > 1 else "_"

            grille[yi][xi] = grille[yi][xi][0] + "_"
            grille[yf][xf] = grille[yf][xf][0] + "_"

            a_supprimer.add((xi, yi))
            a_supprimer.add((xf, yf))

            for y in range(hauteur):
                for x in range(largeur):
                    if grille[y][x][0] == couleur_cible:
                        # Si on échange r_ avec un bonus (v, h, p),
                        # tous les bonbons de cette couleur deviennent ce bonus
                        if type_special_cible in "vhp":
                            grille[y][x] = couleur_cible + type_special_cible
                        a_supprimer.add((x, y))

            return finaliser_suppression(
                nouvelle_grille, a_supprimer, bonus_potentiels, grille
            )

        # Cas Rayé/Paquet + Rayé/Paquet (vh + vh, vh + p, p + p)
        elif len(b1) > 1 and b1[1] in "vhp" and len(b2) > 1 and b2[1] in "vhp":
            grille[yi][xi] = grille[yi][xi][0] + "_"
            grille[yf][xf] = grille[yf][xf][0] + "_"

            a_supprimer.add((xi, yi))
            a_supprimer.add((xf, yf))

            # Combinaison vh + vh : Grande Croix (1 ligne + 1 colonne)
            if b1[1] in "vh" and b2[1] in "vh":
                for i in range(largeur):
                    a_supprimer.add((i, yf))
                for i in range(hauteur):
                    a_supprimer.add((xf, i))

            # Combinaison p + p : Explosion géante (5x5)
            elif b1[1] == "p" and b2[1] == "p":
                for i in range(max(0, yf - 2), min(hauteur, yf + 3)):
                    for j in range(max(0, xf - 2), min(largeur, xf + 3)):
                        a_supprimer.add((j, i))

            # Combinaison vh + p : Triple Croix (3 lignes + 3 colonnes)
            else:
                grille[yi][xi] = grille[yi][xi][0] + "_"
                grille[yf][xf] = grille[yf][xf][0] + "_"

                for dy in [-1, 0, 1]:
                    for i in range(largeur):
                        if 0 <= yf + dy < hauteur:
                            a_supprimer.add((i, yf + dy))
                for dx in [-1, 0, 1]:
                    for i in range(hauteur):
                        if 0 <= xf + dx < largeur:
                            a_supprimer.add((xf + dx, i))

            return finaliser_suppression(
                nouvelle_grille, a_supprimer, bonus_potentiels, grille
            )

    # Analyse des alignements verticaux et horizontaux
    for y in range(hauteur):
        for x in range(largeur):
            # On ignore les vides et les arc-en-ciel déjà là
            if grille[y][x][0] in "_r":
                continue

            h_match = obtenir_alignement_horizontal(grille, x, y)
            v_match = obtenir_alignement_vertical(grille, x, y)
            if not h_match and not v_match:
                continue

            couleur = grille[y][x][0]
            # Déterminer le point de création du bonus
            pos_bonus = (x, y)
            match_total = set(h_match + v_match)
            if pos_f in match_total:
                pos_bonus = pos_f
            elif pos_i in match_total:
                pos_bonus = pos_i

            # Détection Arc-en-ciel (5 alignés)
            if len(h_match) >= 5 or len(v_match) >= 5:
                for c in match_total:
                    a_supprimer.add(c)
                    bonus_potentiels.pop(c, None)
                # On place l'arc-en-ciel au milieu du match
                if len(h_match) >= 5:
                    bonus_potentiels[h_match[len(h_match) // 2]] = "r_"
                else:
                    bonus_potentiels[v_match[len(v_match) // 2]] = "r_"

            # Détection Paquet (L ou T)
            elif h_match and v_match:
                for c in h_match + v_match:
                    a_supprimer.add(c)
                    bonus_potentiels.pop(c, None)
                bonus_potentiels[pos_bonus] = couleur + "p"

            # Détection Rayé (4 alignés)
            elif len(h_match) == 4:
                # horizontal -> rayures verticales
                if pos_bonus not in a_supprimer:
                    bonus_potentiels[pos_bonus] = couleur + "v"

                for c in h_match:
                    a_supprimer.add(c)

            elif len(v_match) == 4:
                # vertical -> rayures horizontales
                if pos_bonus not in a_supprimer:
                    bonus_potentiels[pos_bonus] = couleur + "h"

                for c in v_match:
                    a_supprimer.add(c)

            # Alignement de 3 standard
            else:
                for c in h_match + v_match:
                    a_supprimer.add(c)

    return finaliser_suppression(nouvelle_grille, a_supprimer, bonus_potentiels, grille)


def finaliser_suppression(
    nouvelle_grille, a_supprimer, bonus_potentiels, grille_origine
):
    """Gère les réactions en chaîne des bonus existants et nettoie la grille."""

    deja_traites = set()
    analyse_en_cours = True
    while analyse_en_cours:
        nouveaux = set()
        for x, y in a_supprimer:
            if (x, y) not in deja_traites:
                bonbon = grille_origine[y][x]
                if len(bonbon) > 1 and bonbon[1] in "vhp":
                    zone = obtenir_zone_speciale(grille_origine, x, y, bonbon)
                    for c in zone:
                        if c not in a_supprimer:
                            nouveaux.add(c)
                deja_traites.add((x, y))

        if not nouveaux:
            analyse_en_cours = False
        else:
            a_supprimer.update(nouveaux)

    for x, y in a_supprimer:
        nouvelle_grille[y][x] = "__"

    # Placement des nouveaux bonus (si la case n'est pas déjà marquée pour suppression)
    for (px, py), type_b in bonus_potentiels.items():
        nouvelle_grille[py][px] = type_b

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
    g = charger_fichier("data/exemple_bonus.csv")
    afficher_grille(g)
