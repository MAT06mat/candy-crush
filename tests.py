from unittest import TestCase, main
from fonctions import *


class ChargerGrille(TestCase):
    def test_chargement_default(self):
        grille = charger_grille("data/exemple_grille.csv")
        self.assertEqual(
            grille,
            [
                [2, 3, 4, 2, 3, 4, 2],
                [3, 4, 2, 3, 1, 2, 3],
                [4, 2, 3, 4, 1, 3, 1],
                [2, 0, 0, 1, 0, 1, 1],
                [3, 4, 2, 3, 1, 1, 3],
                [4, 2, 3, 4, 1, 3, 4],
                [2, 3, 4, 2, 3, 4, 2],
                [3, 4, 2, 3, 4, 2, 3],
            ],
        )

    def test_chargement_vide(self):
        grille = charger_grille("data/grille_vide.csv")
        self.assertEqual(
            grille,
            [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
            ],
        )


class EchangerDeuxBonbons(TestCase):
    def test_1(self):
        grille_1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        grille_2 = [[1, 2, 3], [5, 4, 6], [7, 8, 9]]
        echanger_deux_bonbons(grille_1, (0, 1), (1, 1))
        self.assertEqual(grille_1, grille_2)

    def test_2(self):
        grille_1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        grille_2 = [[1, 2, 3], [4, 5, 9], [7, 8, 6]]
        echanger_deux_bonbons(grille_1, (2, 1), (2, 2))
        self.assertEqual(grille_1, grille_2)

    def test_3(self):
        grille_1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        grille_2 = [[1, 7, 3], [4, 5, 6], [2, 8, 9]]
        echanger_deux_bonbons(grille_1, (1, 0), (0, 2))
        self.assertEqual(grille_1, grille_2)


class SupprimerBonbonsLigne(TestCase):
    def test_defaut(self):
        grille_1 = [[1, 2, 3], [4, 5, 3], [4, 5, 3]]
        grille_2 = [[1, 2, -1], [4, 5, -1], [4, 5, -1]]
        self.assertEqual(grille_2, supprimer_bonbons_en_ligne(grille_1))

    def test_plusieurs(self):
        grille_1 = [[1, 1, 1], [2, 3, 4], [2, 3, 2], [2, 3, 2]]
        grille_2 = [[-1, -1, -1], [-1, -1, 4], [-1, -1, 2], [-1, -1, 2]]
        self.assertEqual(grille_2, supprimer_bonbons_en_ligne(grille_1))

    def test_plusieurs_2(self):
        grille_1 = [[1, 1, 1], [2, 3, 1], [1, 4, 1]]
        grille_2 = [[-1, -1, -1], [2, 3, -1], [1, 4, -1]]
        self.assertEqual(grille_2, supprimer_bonbons_en_ligne(grille_1))


class JeuBloque(TestCase):
    def test_defaut(self):
        grille = [[1, 1, 0], [4, 5, 1], [3, 4, 2]]
        self.assertFalse(jeu_est_bloque(grille))

    def test_defaut_1(self):
        grille = [[1, 2, 0], [4, 2, 1], [3, 4, 2]]
        self.assertFalse(jeu_est_bloque(grille))

    def test_defaut_2(self):
        grille = [[1, 2, 0], [0, 2, 4], [1, 0, 3]]
        self.assertFalse(jeu_est_bloque(grille))

    def test_defaut_3(self):
        grille = charger_grille("data/exemple_grille.csv")
        self.assertFalse(jeu_est_bloque(grille))

    def test_defaut_4(self):
        grille = charger_grille("data/grille_vide.csv")
        self.assertFalse(jeu_est_bloque(grille))

    def test_defaut_5(self):
        grille = [[1, 2, 0], [2, 0, 1], [0, 1, 2]]
        self.assertTrue(jeu_est_bloque(grille))


class CalculNouvelleGrille(TestCase):
    def test_grille_stable(self):
        grille = [[0, 1, 2], [1, 2, 3], [2, 3, 4]]
        nouvelle_grille = calculer_nouvelle_grille(grille, 1)
        self.assertTrue(grille_est_stable(grille, nouvelle_grille))

    def test_grille_instable(self):
        grille = [[1, 2, 3], [2, 3, 4], [0, 0, 0]]
        ng = calculer_nouvelle_grille(grille, 1)
        self.assertTrue(ng[2][0] == 2 and ng[2][1] == 3 and ng[2][2] == 4)


class AjouterBonbonsAleatoire(TestCase):
    def test_grille_vide(self):
        grille = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
        grille_attendue = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        ajouter_bonbons_aleatoires(grille, 1)
        self.assertTrue(grille_est_stable(grille, grille_attendue))

    def test_grille_complete(self):
        grille = [[1, 2, 3], [2, 3, 4], [0, 0, 0]]
        grille_attendue = [[1, 2, 3], [2, 3, 4], [0, 0, 0]]
        ajouter_bonbons_aleatoires(grille, 1)
        self.assertTrue(grille_est_stable(grille, grille_attendue))

    def test_grille_partielle(self):
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
        self.assertFalse(erreur)


if __name__ == "__main__":
    main()
