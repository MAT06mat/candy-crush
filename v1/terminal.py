import fonctions as f
from time import sleep


def candy_crush(un_fichier, nb_iter):
    # Choix de la grille de départ
    choix_grille = input(
        "Tapez :\n"
        "    - f pour charger le fichier par défaut\n"
        "    - a pour générer une grille aléatoire\n"
        "    - un autre caractère pour quitter le programme\n"
        ">>> "
    )

    # Initialisation des variables
    score = 0
    nb_type_bonbons = 5
    grille = [[]]

    if choix_grille == "f":
        grille = f.charger_fichier(un_fichier)
    elif choix_grille == "a":
        grille = f.generer_grille(8, 7, nb_type_bonbons)

    # On execute le programme uniquement si une grille a été chargée
    if choix_grille == "f" or choix_grille == "a":
        print("\nBienvenue dans le super Candy Crush (v1) !\n")
        f.afficher_grille(grille, nb_type_bonbons)
        sleep(0.5)

        # Boucle pour chaque tour de jeu
        while nb_iter > 0 and not f.jeu_est_bloque(grille):
            print(f"Score actuel : {score}\nIl reste {nb_iter} coup(s)")

            # Gestion du déplacement
            pos_i, pos_f = f.demander_mouvement()
            f.echanger_deux_bonbons(grille, pos_i, pos_f)

            # Si le coup ne créé pas un alignement ou que le coup déplace de plus de 1 le bonbon
            if (
                not f.test_bonbon_alignee(grille)
                or abs(pos_f[0] - pos_i[0]) + abs(pos_f[1] - pos_i[1]) != 1
            ):
                # Annuler l'échange
                f.echanger_deux_bonbons(grille, pos_i, pos_f)
                print("L'échange n'est pas possible")
                continue  # Relance la boucle

            # Affiche la grille avec les bonbons échangés avant résolution
            print("Action en cours...")
            f.afficher_grille(grille, nb_type_bonbons)
            sleep(0.5)
            nb_iter -= 1

            # Résolution de la grille
            grille_stable = False
            while not grille_stable:
                nouvelle_grille, bonbons_supprimes = f.calculer_nouvelle_grille(
                    grille, nb_type_bonbons
                )
                score += bonbons_supprimes
                grille_stable = f.grille_est_stable(grille, nouvelle_grille)
                grille = nouvelle_grille

                # Affiche chaque nouvelle grille suite à chaque résolution
                if not grille_stable:
                    f.afficher_grille(grille, nb_type_bonbons)
                    sleep(0.5)

        f.afficher_grille(grille, nb_type_bonbons)

        print("\nJeu terminé...\n")
        print(f"Score final : {score}\n")
        input("<Entrer> pour fermer ")


candy_crush("data/exemple_grille.csv", 30)
