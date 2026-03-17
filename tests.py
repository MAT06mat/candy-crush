from unittest import TestCase, main
from fonctions import *


class ChargerGrille(TestCase):
    def test_chargement_default(self):
        grille = charger_grille("data/exemple_grille.csv")
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
                ["3_", "4_", "2_", "3_", "4_", "2_", "3_"],
            ],
        )

    def test_chargement_vide(self):
        grille = charger_grille("data/grille_vide.csv")
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
        grille = charger_grille("data/exemple_bonus.csv")
        self.assertEqual(
            grille,
            [
                ["1_", "0p", "2_", "4v"],
                ["2v", "1_", "1_", "5v"],
                ["2_", "5h", "3_", "1_"],
                ["4v", "1_", "1_", "2v"],
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
    def test_defaut(self):
        grille_1 = [["1_", "2_", "3_"], ["4_", "5_", "3_"], ["4_", "5_", "3_"]]
        grille_2 = [["1_", "2_", "__"], ["4_", "5_", "__"], ["4_", "5_", "__"]]
        self.assertEqual(grille_2, supprimer_bonbons_en_ligne(grille_1))

    def test_plusieurs(self):
        grille_1 = [
            ["1_", "1_", "1_"],
            ["2_", "3_", "4_"],
            ["2_", "3_", "2_"],
            ["2_", "3_", "2_"],
        ]
        grille_2 = [
            ["__", "__", "__"],
            ["__", "__", "4_"],
            ["__", "__", "2_"],
            ["__", "__", "2_"],
        ]
        self.assertEqual(grille_2, supprimer_bonbons_en_ligne(grille_1))

    def test_plusieurs_2(self):
        grille_1 = [["1_", "1_", "1_"], ["2_", "3_", "1_"], ["1_", "4_", "1_"]]
        grille_2 = [["__", "__", "__"], ["2_", "3_", "__"], ["1_", "4_", "__"]]
        self.assertEqual(grille_2, supprimer_bonbons_en_ligne(grille_1))


class JeuBloque(TestCase):
    def test_defaut(self):
        grille = [["1_", "1_", "0_"], ["4_", "5_", "1_"], ["3_", "4_", "2_"]]
        self.assertFalse(jeu_est_bloque(grille))

    def test_defaut_1(self):
        grille = [["1_", "2_", "0_"], ["4_", "2_", "1_"], ["3_", "4_", "2_"]]
        self.assertFalse(jeu_est_bloque(grille))

    def test_defaut_2(self):
        grille = [["1_", "2_", "0_"], ["0_", "2_", "4_"], ["1_", "0_", "3_"]]
        self.assertFalse(jeu_est_bloque(grille))

    def test_defaut_3(self):
        grille = charger_grille("data/exemple_grille.csv")
        self.assertFalse(jeu_est_bloque(grille))

    def test_defaut_4(self):
        grille = charger_grille("data/grille_vide.csv")
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


if __name__ == "__main__":
    main()
