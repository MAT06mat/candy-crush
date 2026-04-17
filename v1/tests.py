from fonctions import charger_fichier
from fonctions import echanger_deux_bonbons
from fonctions import supprimer_bonbons_en_ligne
from fonctions import jeu_est_bloque
from fonctions import calculer_nouvelle_grille
from fonctions import grille_est_stable
from fonctions import ajouter_bonbons_aleatoires
from fonctions import dupliquer_grille
from fonctions import appliquer_gravite


def test_charger_grille_chargement_default():
    grille = charger_fichier("data/exemple_grille.csv")
    return grille == [
        [2, 3, 4, 2, 3, 4, 2],
        [3, 4, 2, 3, 1, 2, 3],
        [4, 2, 3, 4, 1, 3, 1],
        [2, 0, 0, 1, 0, 1, 1],
        [3, 4, 2, 3, 1, 1, 3],
        [4, 2, 3, 4, 1, 3, 4],
        [2, 3, 4, 2, 3, 4, 2],
        [3, 4, 2, 3, 4, 2, 5],
    ]


def test_charger_grille_chargement_vide():
    grille = charger_fichier("data/grille_vide.csv")
    return grille == [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]


def test_echanger_deux_bonbons_1():
    grille_1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    grille_2 = [[1, 2, 3], [5, 4, 6], [7, 8, 9]]
    echanger_deux_bonbons(grille_1, (0, 1), (1, 1))
    return grille_1 == grille_2


def test_echanger_deux_bonbons_2():
    grille_1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    grille_2 = [[1, 2, 3], [4, 5, 9], [7, 8, 6]]
    echanger_deux_bonbons(grille_1, (2, 1), (2, 2))
    return grille_1 == grille_2


def test_echanger_deux_bonbons_3():
    grille_1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    grille_2 = [[1, 7, 3], [4, 5, 6], [2, 8, 9]]
    echanger_deux_bonbons(grille_1, (1, 0), (0, 2))
    return grille_1 == grille_2


# --- TESTS D'ALIGNEMENTS DE BASE ---


def test_supprimer_bonbons_ligne_alignement_3_vertical():
    grille_1 = [[1, 2], [1, 3], [1, 4]]
    grille_2 = [[-1, 2], [-1, 3], [-1, 4]]
    return (grille_2, 3) == supprimer_bonbons_en_ligne(grille_1)


def test_supprimer_bonbons_ligne_alignement_3_horizontal():
    grille_1 = [[2, 2, 2], [4, 5, 6]]
    grille_2 = [[-1, -1, -1], [4, 5, 6]]
    return (grille_2, 3) == supprimer_bonbons_en_ligne(grille_1)


def test_supprimer_bonbons_ligne_alignement_3_vertical_2():
    grille_1 = [[0, 1], [2, 1], [3, 1]]
    grille_2 = [[0, -1], [2, -1], [3, -1]]
    return (grille_2, 3) == supprimer_bonbons_en_ligne(grille_1)


# --- TESTS DE CAS LIMITES ---


def test_supprimer_bonbons_ligne_double_alignement_independant():
    grille_1 = [
        [0, 0, 0, 4, 5],
        [1, 2, 3, 1, 5],
        [5, 4, 3, 1, 5],
    ]
    grille_2 = [
        [-1, -1, -1, 4, -1],
        [1, 2, 3, 1, -1],
        [5, 4, 3, 1, -1],
    ]
    return supprimer_bonbons_en_ligne(grille_1) == (grille_2, 6)


def test_supprimer_bonbons_ligne_aucun_alignement():
    grille_1 = [[1, 2, 1], [2, 1, 2]]
    grille_2 = [[1, 2, 1], [2, 1, 2]]
    return (grille_2, 0) == supprimer_bonbons_en_ligne(grille_1)


def test_jeu_bloque_defaut():
    grille = [[1, 1, 0], [4, 5, 1], [3, 4, 2]]
    return jeu_est_bloque(grille) == False


def test_jeu_bloque_defaut_1():
    grille = [[1, 2, 0], [4, 2, 1], [3, 4, 2]]
    return jeu_est_bloque(grille) == False


def test_jeu_bloque_defaut_2():
    grille = [[1, 2, 0], [0, 2, 4], [1, 0, 3]]
    return jeu_est_bloque(grille) == True


def test_jeu_bloque_defaut_3():
    grille = charger_fichier("data/exemple_grille.csv")
    return jeu_est_bloque(grille) == False


def test_jeu_bloque_defaut_4():
    grille = charger_fichier("data/grille_vide.csv")
    return not jeu_est_bloque(grille)


def test_jeu_bloque_defaut_5():
    grille = [[1, 2, 0], [2, 0, 1], [0, 1, 2]]
    return jeu_est_bloque(grille)


def test_calcul_nouvelle_grille_grille_instable():
    grille = [[1, 2, 3], [2, 3, 4], [0, 0, 0]]
    ng, _ = calculer_nouvelle_grille(grille, 1)
    return ng[2][0] == 2 and ng[2][1] == 3 and ng[2][2] == 4


def test_calcul_nouvelle_grille_grille_stable():
    grille = [[0, 1, 2], [1, 2, 3], [2, 3, 4]]
    nouvelle_grille, _ = calculer_nouvelle_grille(grille, 1)
    return grille_est_stable(grille, nouvelle_grille)


def test_ajouter_bonbons_aleatoire_grille_vide():
    grille = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
    grille_attendue = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    ajouter_bonbons_aleatoires(grille, 1)
    return grille_est_stable(grille, grille_attendue) == True


def test_ajouter_bonbons_aleatoire_grille_complete():
    grille = [[1, 2, 3], [2, 3, 4], [0, 0, 0]]
    grille_attendue = [[1, 2, 3], [2, 3, 4], [0, 0, 0]]
    ajouter_bonbons_aleatoires(grille, 1)
    return grille_est_stable(grille, grille_attendue) == True


def test_ajouter_bonbons_aleatoire_grille_partielle():
    grille = [[1, -1, -1], [2, 3, -1], [0, 0, 0]]
    ajouter_bonbons_aleatoires(grille, 4)
    erreur = False
    i = 0
    while i < len(grille) and not erreur:
        j = 0
        while j < len(grille[0]) and not erreur:
            if grille[i][j] < 0 or grille[i][j] > 3:
                erreur = True
            j += 1
        i += 1
    return erreur == False


def test_dupliquer_grille_1():
    grille_1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    grille_2 = dupliquer_grille(grille_1)
    return grille_1 == grille_2


def test_dupliquer_grille_2():
    grille_1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    grille_2 = dupliquer_grille(grille_1)
    return grille_1 == grille_2


def test_dupliquer_grille_3():
    grille_1 = []
    grille_2 = dupliquer_grille(grille_1)
    return grille_1 == grille_2


def test_grille_est_stable_1():
    grille_1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    grille_2 = dupliquer_grille(grille_1)
    return grille_est_stable(grille_1, grille_2)


def test_grille_est_stable_2():
    grille_1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    grille_2 = []
    return not grille_est_stable(grille_1, grille_2)


def test_grille_est_stable_3():
    grille_1 = []
    grille_2 = []
    return grille_est_stable(grille_1, grille_2)


def test_appliquer_gravite_1():
    grille_1 = [[1, 2, 3], [4, -1, 6], [7, 8, -1]]
    grille_2 = [[1, -1, -1], [4, 2, 3], [7, 8, 6]]
    appliquer_gravite(grille_1)
    return grille_1 == grille_2


def test_appliquer_gravite_2():
    grille_1 = [[-1, 2, -1], [1, -1, 6], [-1, 8, -1]]
    grille_2 = [[-1, -1, -1], [-1, 2, -1], [1, 8, 6]]
    appliquer_gravite(grille_1)
    return grille_1 == grille_2


assert test_charger_grille_chargement_default()
assert test_charger_grille_chargement_vide()
assert test_echanger_deux_bonbons_1()
assert test_echanger_deux_bonbons_2()
assert test_echanger_deux_bonbons_3()
assert test_supprimer_bonbons_ligne_alignement_3_vertical()
assert test_supprimer_bonbons_ligne_alignement_3_horizontal()
assert test_supprimer_bonbons_ligne_alignement_3_vertical_2()
assert test_supprimer_bonbons_ligne_double_alignement_independant()
assert test_supprimer_bonbons_ligne_aucun_alignement()
assert test_jeu_bloque_defaut()
assert test_jeu_bloque_defaut_1()
assert test_jeu_bloque_defaut_2()
assert test_jeu_bloque_defaut_3()
assert test_jeu_bloque_defaut_4()
assert test_jeu_bloque_defaut_5()
assert test_calcul_nouvelle_grille_grille_stable()
assert test_calcul_nouvelle_grille_grille_instable()
assert test_ajouter_bonbons_aleatoire_grille_vide()
assert test_ajouter_bonbons_aleatoire_grille_complete()
assert test_ajouter_bonbons_aleatoire_grille_partielle()
assert test_dupliquer_grille_1()
assert test_dupliquer_grille_2()
assert test_dupliquer_grille_3()
assert test_grille_est_stable_1()
assert test_grille_est_stable_2()
assert test_grille_est_stable_3()
assert test_appliquer_gravite_1()
assert test_appliquer_gravite_2()

print("Tous les tests sont passés avec succès")
