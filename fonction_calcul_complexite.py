from fonctions import *


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
            if pos_f in h_match or pos_f in v_match:
                pos_bonus = pos_f
            elif pos_i in h_match or pos_i in v_match:
                pos_bonus = pos_i

            # Détection Arc-en-ciel (5 alignés)
            if len(h_match) >= 5 or len(v_match) >= 5:
                match = h_match if len(h_match) >= 5 else v_match
                for c in match:
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

    # Gestion des réactions en chaîne
    deja_traites = set()
    analyse_en_cours = True
    while analyse_en_cours:
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
