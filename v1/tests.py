from unittest import TestCase, main
from fonctions import *


def test_charger_grille_chargement_default():
    grille = charger_fichier("data/exemple_grille.csv")
    return grille == [
        ["2_", "3_", "4_", "2_", "3_", "4_", "2_"],
        ["3_", "4_", "2_", "3_", "1_", "2_", "3_"],
        ["4_", "2_", "3_", "4_", "1_", "3_", "1_"],
        ["2_", "0_", "0_", "1_", "0_", "1_", "1_"],
        ["3_", "4_", "2_", "3_", "1_", "1_", "3_"],
        ["4_", "2_", "3_", "4_", "1_", "3_", "4_"],
        ["2_", "3_", "4_", "2_", "3_", "4_", "2_"],
        ["3_", "4_", "2_", "3_", "4_", "2_", "3_"],
    ]


def test_charger_grille_chargement_vide():
    grille = charger_fichier("data/grille_vide.csv")
    return grille == [
        ["0_", "0_", "0_", "0_", "0_", "0_", "0_"],
        ["0_", "0_", "0_", "0_", "0_", "0_", "0_"],
        ["0_", "0_", "0_", "0_", "0_", "0_", "0_"],
        ["0_", "0_", "0_", "0_", "0_", "0_", "0_"],
        ["0_", "0_", "0_", "0_", "0_", "0_", "0_"],
        ["0_", "0_", "0_", "0_", "0_", "0_", "0_"],
        ["0_", "0_", "0_", "0_", "0_", "0_", "0_"],
        ["0_", "0_", "0_", "0_", "0_", "0_", "0_"],
    ]


def test_charger_grille_chargement_avec_bonus():
    grille = charger_fichier("data/exemple_bonus.csv")
    return grille == [
        ["1_", "0p", "2_", "4v"],
        ["2v", "1_", "1_", "5v"],
        ["2_", "5h", "3_", "1_"],
        ["4v", "r_", "1_", "2v"],
    ]


def test_echanger_deux_bonbons_1():
    grille_1 = [["1_", "2_", "3_"], ["4_", "5_", "6_"], ["7_", "8_", "9_"]]
    grille_2 = [["1_", "2_", "3_"], ["5_", "4_", "6_"], ["7_", "8_", "9_"]]
    echanger_deux_bonbons(grille_1, (0, 1), (1, 1))
    return grille_1 == grille_2


def test_echanger_deux_bonbons_2():
    grille_1 = [["1_", "2_", "3_"], ["4_", "5_", "6_"], ["7_", "8_", "9_"]]
    grille_2 = [["1_", "2_", "3_"], ["4_", "5_", "9_"], ["7_", "8_", "6_"]]
    echanger_deux_bonbons(grille_1, (2, 1), (2, 2))
    return grille_1 == grille_2


def test_echanger_deux_bonbons_3():
    grille_1 = [["1_", "2_", "3_"], ["4_", "5_", "6_"], ["7_", "8_", "9_"]]
    grille_2 = [["1_", "7_", "3_"], ["4_", "5_", "6_"], ["2_", "8_", "9_"]]
    echanger_deux_bonbons(grille_1, (1, 0), (0, 2))
    return grille_1 == grille_2


# --- TESTS D'ALIGNEMENTS DE BASE ---


def test_supprimer_bonbons_ligne_alignement_3_vertical():
    grille_1 = [["1_", "2_"], ["1_", "3_"], ["1_", "4_"]]
    grille_2 = [["__", "2_"], ["__", "3_"], ["__", "4_"]]
    return grille_2 == supprimer_bonbons_en_ligne(grille_1)


def test_supprimer_bonbons_ligne_alignement_3_horizontal():
    grille_1 = [["2_", "2_", "2_"], ["4_", "5_", "6_"]]
    grille_2 = [["__", "__", "__"], ["4_", "5_", "6_"]]
    return grille_2 == supprimer_bonbons_en_ligne(grille_1)


def test_supprimer_bonbons_ligne_alignement_3_vertical_bord_bas():
    grille_1 = [["0_", "1_"], ["2_", "1_"], ["3_", "1_"]]
    grille_2 = [["0_", "__"], ["2_", "__"], ["3_", "__"]]
    return grille_2 == supprimer_bonbons_en_ligne(grille_1)


def test_supprimer_bonbons_ligne_double_alignement_independant():
    grille_1 = [
        ["0_", "0_", "0_", "4_", "5_"],
        ["1_", "2_", "3_", "1_", "5_"],
        ["5_", "4_", "3_", "1_", "5_"],
    ]
    grille_2 = [
        ["__", "__", "__", "4_", "__"],
        ["1_", "2_", "3_", "1_", "__"],
        ["5_", "4_", "3_", "1_", "__"],
    ]
    return supprimer_bonbons_en_ligne(grille_1) == grille_2


# --- TESTS DE CRÉATION DE BONUS ---


def test_supprimer_bonbons_ligne_creation_raye_vertical():
    grille_1 = [["1_", "1_", "1_", "1_"], ["2_", "3_", "4_", "5_"]]
    grille_2 = [["1v", "__", "__", "__"], ["2_", "3_", "4_", "5_"]]
    return grille_2 == supprimer_bonbons_en_ligne(grille_1, (1, 0), (0, 0))


def test_supprimer_bonbons_ligne_creation_raye_horizontal():
    grille_1 = [["1_"], ["1_"], ["1_"], ["1_"]]
    grille_2 = [["__"], ["__"], ["__"], ["1h"]]
    return grille_2 == supprimer_bonbons_en_ligne(grille_1, (0, 0), (0, 3))


def test_supprimer_bonbons_ligne_creation_paquet_en_L():
    grille_1 = [["1_", "1_", "1_"], ["1_", "2_", "3_"], ["1_", "4_", "5_"]]
    grille_2 = [["1p", "__", "__"], ["__", "2_", "3_"], ["__", "4_", "5_"]]
    return grille_2 == supprimer_bonbons_en_ligne(grille_1)


def test_supprimer_bonbons_ligne_creation_arc_en_ciel():
    grille_1 = [["1_", "1_", "1_", "1_", "1_"]]
    grille_2 = [["__", "__", "r_", "__", "__"]]
    return grille_2 == supprimer_bonbons_en_ligne(grille_1)


def test_supprimer_bonbons_ligne_creation_raye_h_depuis_echange():
    grille_1 = [["0_", "2_"], ["1_", "2_"], ["1_", "2_"], ["1_", "2_"]]
    grille_2 = [["0_", "2h"], ["__", "__"], ["__", "__"], ["__", "__"]]
    return supprimer_bonbons_en_ligne(grille_1, (0, 0), (0, 1)) == grille_2


def test_supprimer_bonbons_ligne_creation_arc_en_ciel_cascade():
    grille_1 = [["3_", "3_", "3_", "3_", "3_"]]
    grille_2 = [["__", "__", "r_", "__", "__"]]
    return supprimer_bonbons_en_ligne(grille_1) == grille_2


# --- TESTS DE RÉACTIONS EN CHAÎNE ---


def test_supprimer_bonbons_ligne_explosion_raye_v():
    grille_1 = [["1v", "2_"], ["1_", "3_"], ["1_", "4_"]]
    grille_2 = [["__", "2_"], ["__", "3_"], ["__", "4_"]]
    return grille_2 == supprimer_bonbons_en_ligne(grille_1)


def test_supprimer_bonbons_ligne_explosion_paquet_p():
    grille_1 = [["1p", "1_", "1_"], ["2_", "2_", "3_"], ["3_", "4_", "3_"]]
    grille_2 = [["__", "__", "__"], ["__", "__", "3_"], ["3_", "4_", "3_"]]
    return grille_2 == supprimer_bonbons_en_ligne(grille_1)


# --- TESTS DE COMBINAISONS SPÉCIALES ---


def test_supprimer_bonbons_ligne_combinaison_double_raye():
    grille_1 = [["1v", "2h", "3_"], ["4_", "5_", "6_"], ["7_", "8_", "9_"]]
    grille_2 = [["__", "__", "__"], ["4_", "__", "6_"], ["7_", "__", "9_"]]
    return grille_2 == supprimer_bonbons_en_ligne(grille_1, (0, 0), (1, 0))


def test_supprimer_bonbons_ligne_combinaison_arc_en_ciel_simple():
    grille_1 = [["r_", "1_"], ["2_", "1_"]]
    grille_2 = [["__", "__"], ["2_", "__"]]
    return grille_2 == supprimer_bonbons_en_ligne(grille_1, (0, 0), (1, 0))


def test_supprimer_bonbons_ligne_combinaison_arc_en_ciel_plus_raye():
    grille_1 = [["r_", "1v"], ["1_", "2_"], ["1_", "3_"]]
    grille_2 = [["__", "__"], ["__", "__"], ["__", "__"]]
    return grille_2 == supprimer_bonbons_en_ligne(grille_1, (0, 0), (1, 0))


def test_supprimer_bonbons_ligne_combinaison_double_paquet():
    grille_1 = [
        ["1_", "4_", "3_", "2_", "0_"],
        ["0_", "2_", "4_", "0_", "2_"],
        ["1_", "3_", "1p", "2p", "0_"],
        ["2_", "5_", "5_", "1_", "4_"],
        ["0_", "1_", "1_", "5_", "3_"],
    ]
    grille_2 = [
        ["1_", "__", "__", "__", "__"],
        ["0_", "__", "__", "__", "__"],
        ["1_", "__", "__", "__", "__"],
        ["2_", "__", "__", "__", "__"],
        ["0_", "__", "__", "__", "__"],
    ]
    return grille_2 == supprimer_bonbons_en_ligne(grille_1, (2, 2), (3, 2))


def test_supprimer_bonbons_ligne_combinaison_double_arc_en_ciel():
    grille_1 = [["r_", "r_", "3_", "4_"], ["1_", "2_", "3_", "4_"]]
    grille_2 = [["__", "__", "__", "__"], ["__", "__", "__", "__"]]
    return grille_2 == supprimer_bonbons_en_ligne(grille_1, (0, 0), (1, 0))


def test_supprimer_bonbons_ligne_combo_raye_plus_paquet():
    grille_1 = [
        ["0_", "0_", "0_", "0_", "0_"],
        ["0_", "0_", "0_", "0_", "0_"],
        ["0_", "0_", "1v", "2p", "0_"],
        ["0_", "0_", "0_", "0_", "0_"],
        ["0_", "0_", "0_", "0_", "0_"],
    ]
    res = supprimer_bonbons_en_ligne(grille_1, (2, 2), (3, 2))
    return res[2][3] == "__"


def test_supprimer_bonbons_ligne_arc_en_ciel_plus_paquet():
    grille_1 = [["r_", "1p"], ["0_", "0_"], ["0_", "1_"]]
    grille_2 = [["__", "__"], ["__", "__"], ["__", "__"]]
    return supprimer_bonbons_en_ligne(grille_1, (0, 0), (1, 0)) == grille_2


def test_supprimer_bonbons_ligne_arc_en_ciel_sans_cible():
    grille_1 = [["r_", "0_", "1_"], ["1_", "2_", "0_"]]
    grille_2 = [["r_", "0_", "1_"], ["1_", "2_", "0_"]]
    return supprimer_bonbons_en_ligne(grille_1) == grille_2


# --- TESTS DE CAS LIMITES ---


def test_supprimer_bonbons_ligne_aucun_alignement():
    grille_1 = [["1_", "2_", "1_"], ["2_", "1_", "2_"]]
    grille_2 = [["1_", "2_", "1_"], ["2_", "1_", "2_"]]
    return grille_2 == supprimer_bonbons_en_ligne(grille_1)


def test_supprimer_bonbons_ligne_alignement_complexe_chaine():
    grille_1 = [["1_", "1_", "1v"], ["2_", "3_", "2p"], ["4_", "5_", "6_"]]
    grille_2 = [["__", "__", "__"], ["2_", "__", "__"], ["4_", "__", "__"]]
    return grille_2 == supprimer_bonbons_en_ligne(grille_1)


# --- TESTS DE PRIORITÉ ET CONFLITS ---


def test_supprimer_bonbons_ligne_priorite_arc_en_ciel_sur_raye():
    grille_1 = [["1_", "1_", "1_", "1_", "1_"]]
    res = supprimer_bonbons_en_ligne(grille_1)
    flatten = [item for sublist in res for item in sublist]
    return flatten.count("r_") == 1


def test_supprimer_bonbons_ligne_destruction_bonus_par_un_autre():
    grille_1 = [["0v", "0_", "0_"], ["1_", "4_", "5_"], ["1_", "4_", "5_"]]
    grille_2 = [["__", "__", "__"], ["__", "4_", "5_"], ["__", "4_", "5_"]]
    return supprimer_bonbons_en_ligne(grille_1) == grille_2


def test_supprimer_bonbons_ligne_alignement_croise_simple_T():
    grille_1 = [["1_", "1_", "1_"], ["4_", "1_", "5_"], ["6_", "1_", "7_"]]
    grille_2 = [["__", "1p", "__"], ["4_", "__", "5_"], ["6_", "__", "7_"]]
    return supprimer_bonbons_en_ligne(grille_1) == grille_2


def test_jeu_bloque_defaut():
    grille = [["1_", "1_", "0_"], ["4_", "5_", "1_"], ["3_", "4_", "2_"]]
    return jeu_est_bloque(grille) == False


def test_jeu_bloque_defaut_1():
    grille = [["1_", "2_", "0_"], ["4_", "2_", "1_"], ["3_", "4_", "2_"]]
    return jeu_est_bloque(grille) == False


def test_jeu_bloque_defaut_2():
    grille = [["1_", "2_", "0_"], ["0_", "2_", "4_"], ["1_", "0_", "3_"]]
    return jeu_est_bloque(grille) == True


def test_jeu_bloque_defaut_3():
    grille = charger_fichier("data/exemple_grille.csv")
    return jeu_est_bloque(grille) == False


def test_jeu_bloque_defaut_4():
    grille = charger_fichier("data/grille_vide.csv")
    return jeu_est_bloque(grille) == False


def test_jeu_bloque_defaut_5():
    grille = [["1_", "2_", "0_"], ["2_", "0_", "1_"], ["0_", "1_", "2_"]]
    return jeu_est_bloque(grille) == True


def test_calcul_nouvelle_grille_grille_instable():
    grille = [["1_", "2_", "3_"], ["2_", "3_", "4_"], ["0_", "0_", "0_"]]
    ng = calculer_nouvelle_grille(grille, 1)
    return ng[2][0] == "2_" and ng[2][1] == "3_" and ng[2][2] == "4_"


def test_calcul_nouvelle_grille_grille_stable():
    grille = [["0_", "1_", "2_"], ["1_", "2_", "3_"], ["2_", "3_", "4_"]]
    nouvelle_grille = calculer_nouvelle_grille(grille, 1)
    return grille_est_stable(grille, nouvelle_grille)


def test_ajouter_bonbons_aleatoire_grille_vide():
    grille = [["__", "__", "__"], ["__", "__", "__"], ["__", "__", "__"]]
    grille_attendue = [["0_", "0_", "0_"], ["0_", "0_", "0_"], ["0_", "0_", "0_"]]
    ajouter_bonbons_aleatoires(grille, 1)
    return grille_est_stable(grille, grille_attendue) == True


def test_ajouter_bonbons_aleatoire_grille_complete():
    grille = [["1_", "2_", "3_"], ["2_", "3_", "4_"], ["0_", "0_", "0_"]]
    grille_attendue = [["1_", "2_", "3_"], ["2_", "3_", "4_"], ["0_", "0_", "0_"]]
    ajouter_bonbons_aleatoires(grille, 1)
    return grille_est_stable(grille, grille_attendue) == True


def test_ajouter_bonbons_aleatoire_grille_partielle():
    grille = [["1_", "__", "__"], ["2_", "3_", "__"], ["0_", "0_", "0_"]]
    ajouter_bonbons_aleatoires(grille, 4)
    erreur = False
    i = 0
    while i < len(grille) and not erreur:
        j = 0
        while j < len(grille[0]) and not erreur:
            if int(grille[i][j][0]) < 0 or int(grille[i][j][0]) > 3:
                erreur = True
            j += 1
        i += 1
    return erreur == False


def test_dupliquer_grille_1():
    grille_1 = [["1_", "2_", "3_"], ["4_", "5_", "6_"], ["7_", "8_", "9_"]]
    grille_2 = dupliquer_grille(grille_1)
    return grille_1 == grille_2


def test_dupliquer_grille_2():
    grille_1 = [["11_", "12_", "13_"], ["14_", "15_", "16_"], ["17_", "18_", "19_"]]
    grille_2 = dupliquer_grille(grille_1)
    return grille_1 == grille_2


def test_dupliquer_grille_3():
    grille_1 = []
    grille_2 = dupliquer_grille(grille_1)
    return grille_1 == grille_2


def test_grille_est_stable_1():
    grille_1 = [["1_", "2_", "3_"], ["4_", "5_", "6_"], ["7_", "8_", "9_"]]
    grille_2 = dupliquer_grille(grille_1)
    return grille_1 == grille_2


def test_grille_est_stable_2():
    grille_1 = [["11_", "12_", "13_"], ["14_", "15_", "16_"], ["17_", "18_", "19_"]]
    grille_2 = []
    return grille_1 != grille_2


def test_grille_est_stable_3():
    grille_1 = []
    grille_2 = []
    return grille_1 == grille_2


def test_appliquer_gravite_1():
    grille_1 = [["1_", "2_", "3_"], ["4_", "__", "6_"], ["7_", "8_", "__"]]
    grille_2 = [["1_", "__", "__"], ["4_", "2_", "3_"], ["7_", "8_", "6_"]]
    appliquer_gravite(grille_1)
    return grille_1 == grille_2


assert test_charger_grille_chargement_default()
assert test_charger_grille_chargement_vide()
assert test_charger_grille_chargement_avec_bonus()
assert test_echanger_deux_bonbons_1()
assert test_echanger_deux_bonbons_2()
assert test_echanger_deux_bonbons_3()
assert test_supprimer_bonbons_ligne_alignement_3_vertical()
assert test_supprimer_bonbons_ligne_alignement_3_horizontal()
assert test_supprimer_bonbons_ligne_alignement_3_vertical_bord_bas()
assert test_supprimer_bonbons_ligne_double_alignement_independant()
assert test_supprimer_bonbons_ligne_creation_raye_vertical()
assert test_supprimer_bonbons_ligne_creation_raye_horizontal()
assert test_supprimer_bonbons_ligne_creation_paquet_en_L()
assert test_supprimer_bonbons_ligne_creation_arc_en_ciel()
assert test_supprimer_bonbons_ligne_creation_raye_h_depuis_echange()
assert test_supprimer_bonbons_ligne_creation_arc_en_ciel_cascade()
assert test_supprimer_bonbons_ligne_explosion_raye_v()
assert test_supprimer_bonbons_ligne_explosion_paquet_p()
assert test_supprimer_bonbons_ligne_combinaison_double_raye()
assert test_supprimer_bonbons_ligne_combinaison_arc_en_ciel_simple()
assert test_supprimer_bonbons_ligne_combinaison_arc_en_ciel_plus_raye()
assert test_supprimer_bonbons_ligne_combinaison_double_paquet()
assert test_supprimer_bonbons_ligne_combinaison_double_arc_en_ciel()
assert test_supprimer_bonbons_ligne_combo_raye_plus_paquet()
assert test_supprimer_bonbons_ligne_arc_en_ciel_plus_paquet()
assert test_supprimer_bonbons_ligne_arc_en_ciel_sans_cible()
assert test_supprimer_bonbons_ligne_aucun_alignement()
assert test_supprimer_bonbons_ligne_alignement_complexe_chaine()
assert test_supprimer_bonbons_ligne_priorite_arc_en_ciel_sur_raye()
assert test_supprimer_bonbons_ligne_destruction_bonus_par_un_autre()
assert test_supprimer_bonbons_ligne_alignement_croise_simple_T()
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
