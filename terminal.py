# TODO
import fonctions as f

grille = f.charger_fichier("data/exemple_grille.csv")
dico_bonbon = {
    "0": "🍎",
    "1": "🍋",
    "2": "🥝",
    "3": "🍉",
    "4": "🍇",
    "5": "🍒",
    "r": "🎂",
}
dico_bonus = {"h": "-", "v": "|", "p": "+", "_": " "}
f.afficher_grille(grille, dico_bonbon, dico_bonus)
nombre_coups = 30
while f.jeu_est_bloque(grille) == False and nombre_coups > 0:
    grille_ancienne = f.dupliquer_grille(grille)
    deplacement = f.demander_mouvement()
    f.echanger_deux_bonbons(grille, deplacement[0], deplacement[1])
    f.afficher_grille(grille, dico_bonbon, dico_bonus)
    nombre_coups -= 1
    grille = f.calculer_nouvelle_grille(grille, len(dico_bonbon))
    f.afficher_grille(grille, dico_bonbon, dico_bonus)
    while not f.grille_est_stable(grille, grille_ancienne):
        grille = f.calculer_nouvelle_grille(grille, len(dico_bonbon))
        f.afficher_grille(grille, dico_bonbon, dico_bonus)
