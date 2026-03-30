from unittest import TestCase, main
from fonctions import *


class ChargerGrille(TestCase):
    def test_chargement_default(self):
        grille = charger_fichier("data/exemple_grille.csv")
        self.assertEqual(
            grille,
            [
                ["2_", "3_", "4_", "2_", "3_", "4_", "2_"],
                ["3_", "4_", "2_", "3_", "1_", "2_", "3_"],
                ["4_", "2_", "3_", "4_", "1_", "3_", "1_"],
                ["2_", "0_", "0_", "1_", "0_", "1_", "1_"],
                ["3_", "4_", "2_", "3_", "1_", "1_", "3_"],
                ["4_", "2_", "3_", "4_", "1_", "3_", "4_"],
                ["2_", "3_", "4_", "2_", "3_", "4_", "2_"],
                ["3_", "4_", "2_", "3_", "4_", "2_", "5_"],
            ],
        )

    def test_chargement_vide(self):
        grille = charger_fichier("data/grille_vide.csv")
        self.assertEqual(
            grille,
            [
                ["0_", "0_", "0_", "0_", "0_", "0_", "0_"],
                ["0_", "0_", "0_", "0_", "0_", "0_", "0_"],
                ["0_", "0_", "0_", "0_", "0_", "0_", "0_"],
                ["0_", "0_", "0_", "0_", "0_", "0_", "0_"],
                ["0_", "0_", "0_", "0_", "0_", "0_", "0_"],
                ["0_", "0_", "0_", "0_", "0_", "0_", "0_"],
                ["0_", "0_", "0_", "0_", "0_", "0_", "0_"],
                ["0_", "0_", "0_", "0_", "0_", "0_", "0_"],
            ],
        )

    def test_chargement_avec_bonus(self):
        grille = charger_fichier("data/exemple_bonus.csv")
        self.assertEqual(
            grille,
            [
                ["1_", "0p", "2_", "4v"],
                ["2v", "1_", "1_", "5v"],
                ["2_", "5h", "3_", "1_"],
                ["4v", "r_", "1_", "2v"],
            ],
        )


class EchangerDeuxBonbons(TestCase):
    def test_1(self):
        grille_1 = [["1_", "2_", "3_"], ["4_", "5_", "6_"], ["7_", "8_", "9_"]]
        grille_2 = [["1_", "2_", "3_"], ["5_", "4_", "6_"], ["7_", "8_", "9_"]]
        echanger_deux_bonbons(grille_1, (0, 1), (1, 1))
        self.assertEqual(grille_1, grille_2)

    def test_2(self):
        grille_1 = [["1_", "2_", "3_"], ["4_", "5_", "6_"], ["7_", "8_", "9_"]]
        grille_2 = [["1_", "2_", "3_"], ["4_", "5_", "9_"], ["7_", "8_", "6_"]]
        echanger_deux_bonbons(grille_1, (2, 1), (2, 2))
        self.assertEqual(grille_1, grille_2)

    def test_3(self):
        grille_1 = [["1_", "2_", "3_"], ["4_", "5_", "6_"], ["7_", "8_", "9_"]]
        grille_2 = [["1_", "7_", "3_"], ["4_", "5_", "6_"], ["2_", "8_", "9_"]]
        echanger_deux_bonbons(grille_1, (1, 0), (0, 2))
        self.assertEqual(grille_1, grille_2)


class SupprimerBonbonsLigne(TestCase):
    # --- TESTS D'ALIGNEMENTS DE BASE ---

    def test_alignement_3_vertical(self):
        grille_1 = [["1_", "2_"], ["1_", "3_"], ["1_", "4_"]]
        grille_2 = [["__", "2_"], ["__", "3_"], ["__", "4_"]]
        self.assertEqual(grille_2, supprimer_bonbons_en_ligne(grille_1))

    def test_alignement_3_horizontal(self):
        grille_1 = [["2_", "2_", "2_"], ["4_", "5_", "6_"]]
        grille_2 = [["__", "__", "__"], ["4_", "5_", "6_"]]
        self.assertEqual(grille_2, supprimer_bonbons_en_ligne(grille_1))

    def test_alignement_3_vertical_bord_bas(self):
        grille_1 = [["0_", "1_"], ["2_", "1_"], ["3_", "1_"]]
        grille_2 = [["0_", "__"], ["2_", "__"], ["3_", "__"]]
        self.assertEqual(supprimer_bonbons_en_ligne(grille_1), grille_2)

    def test_double_alignement_independant(self):
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
        self.assertEqual(supprimer_bonbons_en_ligne(grille_1), grille_2)

    # --- TESTS DE CRÉATION DE BONUS ---

    def test_creation_raye_vertical(self):
        grille_1 = [["1_", "1_", "1_", "1_"], ["2_", "3_", "4_", "5_"]]
        grille_2 = [["1v", "__", "__", "__"], ["2_", "3_", "4_", "5_"]]
        self.assertEqual(grille_2, supprimer_bonbons_en_ligne(grille_1, (1, 0), (0, 0)))

    def test_creation_raye_horizontal(self):
        grille_1 = [["1_"], ["1_"], ["1_"], ["1_"]]
        grille_2 = [["__"], ["__"], ["__"], ["1h"]]
        self.assertEqual(grille_2, supprimer_bonbons_en_ligne(grille_1, (0, 0), (0, 3)))

    def test_creation_paquet_en_L(self):
        grille_1 = [["1_", "1_", "1_"], ["1_", "2_", "3_"], ["1_", "4_", "5_"]]
        grille_2 = [["1p", "__", "__"], ["__", "2_", "3_"], ["__", "4_", "5_"]]
        self.assertEqual(grille_2, supprimer_bonbons_en_ligne(grille_1))

    def test_creation_arc_en_ciel(self):
        grille_1 = [["1_", "1_", "1_", "1_", "1_"]]
        grille_2 = [["__", "__", "r_", "__", "__"]]
        self.assertEqual(grille_2, supprimer_bonbons_en_ligne(grille_1))

    def test_creation_raye_h_depuis_echange(self):
        grille_1 = [["0_", "2_"], ["1_", "2_"], ["1_", "2_"], ["1_", "2_"]]
        grille_2 = [["0_", "2h"], ["__", "__"], ["__", "__"], ["__", "__"]]
        self.assertEqual(supprimer_bonbons_en_ligne(grille_1, (0, 0), (0, 1)), grille_2)

    def test_creation_arc_en_ciel_cascade(self):
        grille_1 = [["3_", "3_", "3_", "3_", "3_"]]
        grille_2 = [["__", "__", "r_", "__", "__"]]
        self.assertEqual(supprimer_bonbons_en_ligne(grille_1), grille_2)

    # --- TESTS DE RÉACTIONS EN CHAÎNE ---

    def test_explosion_raye_v(self):
        grille_1 = [["1v", "2_"], ["1_", "3_"], ["1_", "4_"]]
        grille_2 = [["__", "2_"], ["__", "3_"], ["__", "4_"]]
        self.assertEqual(grille_2, supprimer_bonbons_en_ligne(grille_1))

    def test_explosion_paquet_p(self):
        grille_1 = [["1p", "1_", "1_"], ["2_", "2_", "3_"], ["3_", "4_", "3_"]]
        grille_2 = [["__", "__", "__"], ["__", "__", "3_"], ["3_", "4_", "3_"]]
        self.assertEqual(grille_2, supprimer_bonbons_en_ligne(grille_1))

    # --- TESTS DE COMBINAISONS SPÉCIALES ---

    def test_combinaison_double_raye(self):
        grille_1 = [["1v", "2h", "3_"], ["4_", "5_", "6_"], ["7_", "8_", "9_"]]
        grille_2 = [["__", "__", "__"], ["4_", "__", "6_"], ["7_", "__", "9_"]]
        self.assertEqual(grille_2, supprimer_bonbons_en_ligne(grille_1, (0, 0), (1, 0)))

    def test_combinaison_arc_en_ciel_simple(self):
        grille_1 = [["r_", "1_"], ["2_", "1_"]]
        grille_2 = [["__", "__"], ["2_", "__"]]
        self.assertEqual(grille_2, supprimer_bonbons_en_ligne(grille_1, (0, 0), (1, 0)))

    def test_combinaison_arc_en_ciel_plus_raye(self):
        grille_1 = [["r_", "1v"], ["1_", "2_"], ["1_", "3_"]]
        grille_2 = [["__", "__"], ["__", "__"], ["__", "__"]]
        self.assertEqual(grille_2, supprimer_bonbons_en_ligne(grille_1, (0, 0), (1, 0)))

    def test_combinaison_double_paquet(self):
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
        self.assertEqual(grille_2, supprimer_bonbons_en_ligne(grille_1, (2, 2), (3, 2)))

    def test_combinaison_double_arc_en_ciel(self):
        grille_1 = [["r_", "r_", "3_", "4_"], ["1_", "2_", "3_", "4_"]]
        grille_2 = [["__", "__", "__", "__"], ["__", "__", "__", "__"]]
        self.assertEqual(grille_2, supprimer_bonbons_en_ligne(grille_1, (0, 0), (1, 0)))

    def test_combo_raye_plus_paquet(self):
        grille_1 = [
            ["0_", "0_", "0_", "0_", "0_"],
            ["0_", "0_", "0_", "0_", "0_"],
            ["0_", "0_", "1v", "2p", "0_"],
            ["0_", "0_", "0_", "0_", "0_"],
            ["0_", "0_", "0_", "0_", "0_"],
        ]
        res = supprimer_bonbons_en_ligne(grille_1, (2, 2), (3, 2))
        self.assertEqual(res[2][3], "__")
        self.assertEqual(res[0][3], "__")

    def test_arc_en_ciel_plus_paquet(self):
        grille_1 = [["r_", "1p"], ["0_", "0_"], ["0_", "1_"]]
        grille_2 = [["__", "__"], ["__", "__"], ["__", "__"]]
        self.assertEqual(supprimer_bonbons_en_ligne(grille_1, (0, 0), (1, 0)), grille_2)

    def test_arc_en_ciel_sans_cible(self):
        grille_1 = [["r_", "0_", "1_"], ["1_", "2_", "0_"]]
        grille_2 = [["r_", "0_", "1_"], ["1_", "2_", "0_"]]
        self.assertEqual(supprimer_bonbons_en_ligne(grille_1), grille_2)

    # --- TESTS DE CAS LIMITES ---

    def test_aucun_alignement(self):
        grille_1 = [["1_", "2_", "1_"], ["2_", "1_", "2_"]]
        grille_2 = [["1_", "2_", "1_"], ["2_", "1_", "2_"]]
        self.assertEqual(grille_2, supprimer_bonbons_en_ligne(grille_1))

    def test_alignement_complexe_chaine(self):
        grille_1 = [["1_", "1_", "1v"], ["2_", "3_", "2p"], ["4_", "5_", "6_"]]
        grille_2 = [["__", "__", "__"], ["2_", "__", "__"], ["4_", "__", "__"]]
        self.assertEqual(grille_2, supprimer_bonbons_en_ligne(grille_1))

    # --- TESTS DE PRIORITÉ ET CONFLITS ---

    def test_priorite_arc_en_ciel_sur_raye(self):
        grille_1 = [["1_", "1_", "1_", "1_", "1_"]]
        res = supprimer_bonbons_en_ligne(grille_1)
        flatten = [item for sublist in res for item in sublist]
        self.assertEqual(flatten.count("r_"), 1)
        self.assertEqual(flatten.count("1v"), 0)
        self.assertEqual(flatten.count("1h"), 0)

    def test_destruction_bonus_par_un_autre(self):
        grille_1 = [["0v", "0_", "0_"], ["1_", "4_", "5_"], ["1_", "4_", "5_"]]
        grille_2 = [["__", "__", "__"], ["__", "4_", "5_"], ["__", "4_", "5_"]]
        self.assertEqual(supprimer_bonbons_en_ligne(grille_1), grille_2)

    def test_alignement_croise_simple_T(self):
        grille_1 = [["1_", "1_", "1_"], ["4_", "1_", "5_"], ["6_", "1_", "7_"]]
        grille_2 = [["__", "1p", "__"], ["4_", "__", "5_"], ["6_", "__", "7_"]]
        self.assertEqual(supprimer_bonbons_en_ligne(grille_1), grille_2)


class JeuBloque(TestCase):
    def test_defaut(self):
        grille = [["1_", "1_", "0_"], ["4_", "5_", "1_"], ["3_", "4_", "2_"]]
        self.assertFalse(jeu_est_bloque(grille))

    def test_defaut_1(self):
        grille = [["1_", "2_", "0_"], ["4_", "2_", "1_"], ["3_", "4_", "2_"]]
        self.assertFalse(jeu_est_bloque(grille))

    def test_defaut_2(self):
        grille = [["1_", "2_", "0_"], ["0_", "2_", "4_"], ["1_", "0_", "3_"]]
        self.assertTrue(jeu_est_bloque(grille))

    def test_defaut_3(self):
        grille = charger_fichier("data/exemple_grille.csv")
        self.assertFalse(jeu_est_bloque(grille))

    def test_defaut_4(self):
        grille = charger_fichier("data/grille_vide.csv")
        self.assertFalse(jeu_est_bloque(grille))

    def test_defaut_5(self):
        grille = [["1_", "2_", "0_"], ["2_", "0_", "1_"], ["0_", "1_", "2_"]]
        self.assertTrue(jeu_est_bloque(grille))


class CalculNouvelleGrille(TestCase):
    def test_grille_stable(self):
        grille = [["0_", "1_", "2_"], ["1_", "2_", "3_"], ["2_", "3_", "4_"]]
        nouvelle_grille = calculer_nouvelle_grille(grille, 1)
        self.assertTrue(grille_est_stable(grille, nouvelle_grille))

    def test_grille_instable(self):
        grille = [["1_", "2_", "3_"], ["2_", "3_", "4_"], ["0_", "0_", "0_"]]
        ng = calculer_nouvelle_grille(grille, 1)
        self.assertTrue(ng[2][0] == "2_" and ng[2][1] == "3_" and ng[2][2] == "4_")


class AjouterBonbonsAleatoire(TestCase):
    def test_grille_vide(self):
        grille = [["__", "__", "__"], ["__", "__", "__"], ["__", "__", "__"]]
        grille_attendue = [["0_", "0_", "0_"], ["0_", "0_", "0_"], ["0_", "0_", "0_"]]
        ajouter_bonbons_aleatoires(grille, 1)
        self.assertTrue(grille_est_stable(grille, grille_attendue))

    def test_grille_complete(self):
        grille = [["1_", "2_", "3_"], ["2_", "3_", "4_"], ["0_", "0_", "0_"]]
        grille_attendue = [["1_", "2_", "3_"], ["2_", "3_", "4_"], ["0_", "0_", "0_"]]
        ajouter_bonbons_aleatoires(grille, 1)
        self.assertTrue(grille_est_stable(grille, grille_attendue))

    def test_grille_partielle(self):
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
        self.assertFalse(erreur)


class DupliquerGrille(TestCase):
    def test_1(self):
        grille_1 = [["1_", "2_", "3_"], ["4_", "5_", "6_"], ["7_", "8_", "9_"]]
        grille_2 = dupliquer_grille(grille_1)
        self.assertEqual(grille_1, grille_2)

    def test_2(self):
        grille_1 = [["11_", "12_", "13_"], ["14_", "15_", "16_"], ["17_", "18_", "19_"]]
        grille_2 = dupliquer_grille(grille_1)
        self.assertEqual(grille_1, grille_2)

    def test_2(self):
        grille_1 = []
        grille_2 = dupliquer_grille(grille_1)
        self.assertEqual(grille_1, grille_2)


class GrilleEstStable(TestCase):
    def test_1(self):
        grille_1 = [["1_", "2_", "3_"], ["4_", "5_", "6_"], ["7_", "8_", "9_"]]
        grille_2 = dupliquer_grille(grille_1)
        self.assertEqual(grille_1, grille_2)

    def test_2(self):
        grille_1 = [["11_", "12_", "13_"], ["14_", "15_", "16_"], ["17_", "18_", "19_"]]
        grille_2 = []
        self.assertEqual(grille_1, grille_2)

    def test_2(self):
        grille_1 = []
        grille_2 = []
        self.assertEqual(grille_1, grille_2)


class AppliquerGravite(TestCase):
    def test_1(self):
        grille_1 = [["1_", "2_", "3_"], ["4_", "__", "6_"], ["7_", "8_", "__"]]
        grille_2 = [["1_", "__", "__"], ["4_", "2_", "3_"], ["7_", "8_", "6_"]]
        appliquer_gravite(grille_1)
        self.assertEqual(grille_1, grille_2)


if __name__ == "__main__":
    main()
