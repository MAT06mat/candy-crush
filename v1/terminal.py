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
while nombre_coups > 0 and not f.jeu_est_bloque(grille):
    # Gestion du déplacement
    deplacement = f.demander_mouvement()
    f.echanger_deux_bonbons(grille, deplacement[0], deplacement[1])
    f.afficher_grille(grille, dico_bonbon, dico_bonus)
    nombre_coups -= 1
    # Résolution de la grille
    grille_stable = False
    while not grille_stable:
        grille_ancienne = f.dupliquer_grille(grille)
        grille = f.calculer_nouvelle_grille(grille, len(dico_bonbon) - 1)
        grille_stable = f.grille_est_stable(grille, grille_ancienne)
        if not grille_stable:
            f.afficher_grille(grille, dico_bonbon, dico_bonus)
