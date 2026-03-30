import fonctions as f

grille = f.charger_fichier("data/exemple_grille.csv")
nb_type_bonbons = 6
f.afficher_grille(grille, nb_type_bonbons)
nombre_coups = 30
while nombre_coups > 0 and not f.jeu_est_bloque(grille):
    # Gestion du déplacement
    pos_i, pos_f = f.demander_mouvement()
    f.echanger_deux_bonbons(grille, pos_i, pos_f)

    if (
        not f.test_bonbon_alignee(grille)
        or abs(pos_f[0] - pos_i[0]) + abs(pos_f[1] - pos_i[1]) != 1
    ):
        f.echanger_deux_bonbons(grille, pos_i, pos_f)
        print("L'échange n'est pas possible")
        continue  # Relance la boucle

    f.afficher_grille(grille, nb_type_bonbons)
    nombre_coups -= 1

    # Résolution de la grille
    grille_stable = False
    while not grille_stable:
        nouvelle_grille = f.calculer_nouvelle_grille(grille, nb_type_bonbons)
        grille_stable = f.grille_est_stable(grille, nouvelle_grille)
        grille = nouvelle_grille

        if not grille_stable:
            f.afficher_grille(grille, nb_type_bonbons)
