import fonctions as f
from time import sleep


def candy_crush(un_fichier, nb_iter):
    choix_grille = input(
        """Taper :
        - f pour charger le fichier par défaut 
        - a pour générer une grille aléatoire
        - un autre caractère pour quitter le programme
    """
    )
    # Initialisation des variables
    nb_type_bonbons = 6
    if choix_grille == "f":
        grille = f.charger_fichier(un_fichier)
    elif choix_grille == "a":
        grille = f.generer_grille(8, 7, nb_type_bonbons)

    if choix_grille == "f" or choix_grille == "a":
        print("\nBienvenue dans le super Candy Crush (v1) !\n")

        f.afficher_grille(grille, nb_type_bonbons)
        sleep(0.5)
        while nb_iter > 0 and not f.jeu_est_bloque(grille):
            print(f"Il reste {nb_iter} coup(s)")

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

            print("Action en cours...")
            f.afficher_grille(grille, nb_type_bonbons)
            sleep(0.5)
            nb_iter -= 1

            # Résolution de la grille
            grille_stable = False
            while not grille_stable:
                nouvelle_grille = f.calculer_nouvelle_grille(grille, nb_type_bonbons)
                grille_stable = f.grille_est_stable(grille, nouvelle_grille)
                grille = nouvelle_grille

                if not grille_stable:
                    f.afficher_grille(grille, nb_type_bonbons)
                    sleep(0.5)

        print("\nJeu terminé...\n")
        input("<Entrer> pour fermer")


candy_crush("data/exemple_grille.csv", 30)
