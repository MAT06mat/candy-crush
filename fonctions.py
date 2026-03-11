def charger_grille(fichier: str):
    grille = []
    with open(fichier, "r", encoding="UTF-8") as f:
        for ligne_str in f.read().split("\n"):
            ligne = []
            for numero in ligne_str.split():
                ligne.append(int(numero))
            if len(ligne):
                grille.append(ligne)
    return grille


def afficher_grille(grille):
    for ligne in grille:
        print(*ligne)


if __name__ == "__main__":
    g = charger_grille("exemple_grille.csv")
    afficher_grille(g)
