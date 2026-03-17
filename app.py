import tkinter as tk
from tkinter import Tk, ttk, PhotoImage
from fonctions import *
from time import sleep
import math

PX = 200
PY = 120
GAP = 4
SIZE = 72

COLOR_PATH = {
    "0": "red",
    "1": "blue",
    "2": "green",
    "3": "yellow",
    "4": "purple",
    "5": "orange",
}
TUILES_PATH = ["TL", "T", "TR", "L", "C", "R", "BL", "B", "BR"]


class CandyCrush:
    def __init__(self, x=7, y=6, nb_bonbons=6, background="forest"):
        self.root = Tk()
        self.root.title("Candy Crush")
        self.frame = ttk.Frame(self.root, padding=10)
        self.frame.root = self.root

        g = generer_grille(y, x, nb_bonbons)
        Grille(self.frame, g, nb_bonbons, background)

        ttk.Button(self.frame, text="Click !!!!").pack()

        self.frame.pack()

    def main(self):
        self.root.mainloop()


class Grille:
    def __init__(self, conteneur, grille, nb_bonbons, background):
        self.conteneur = conteneur
        self.grille: liste_2d = grille
        self.nb_bonbons = nb_bonbons
        self.bonbon_choisi = None  # None ou position sous forme (x, y)
        self.canvas = None
        self.assets_cache = {}

        # Chargement des images (d'abord le fond puis les bonbons et la grille)
        self.charger_background(f"assets/backgrounds/{background}.png")
        self.charger_assets()

        # Initialise et affiche la grille
        self.initialiser_canvas()
        self.actualiser_bonbons()

    def charger_assets(self):
        """Chargement des différentes images"""

        # Chargement des bonbons
        for _, color in COLOR_PATH.items():
            for bonus in ["", "-h", "-v", "-p"]:
                path = f"assets/candies/{color + bonus}.png"
                self.get_asset(color + bonus, path)
        self.get_asset("rainbow", "assets/candies/rainbow.png")

        # Chargement des tuiles pour la grille
        for tuile in TUILES_PATH:
            self.get_asset(tuile, f"assets/grid/{tuile}.png", size=SIZE + GAP)

        # Chargement du selecteur de bonbon
        self.get_asset("selected", "assets/selected.png", SIZE + 2 * GAP)

    def charger_background(self, path):
        """Charge et redimensionne le fond aux dimensions de la grille"""

        self.bg_image = None
        try:
            # Load the original large image
            raw_bg = PhotoImage(file=path)
            orig_w = raw_bg.width()
            orig_h = raw_bg.height()

            # Target canvas dimensions
            w_g, h_g = len(self.grille[0]), len(self.grille)
            target_w = 2 * PX - GAP + (GAP + SIZE) * w_g
            target_h = 2 * PY - GAP + (GAP + SIZE) * h_g

            # Calculate the subsample factor
            # We use integer division to find how many times the target fits in the original
            ratio_w = orig_w // target_w
            ratio_h = orig_h // target_h

            # We take the smaller ratio to ensure the image covers the canvas
            # (it will be slightly larger or equal, but never smaller)
            factor = max(1, min(ratio_w, ratio_h))

            # Only subsample, no zoom to avoid memory crash
            if factor > 1:
                self.bg_image = raw_bg.subsample(factor)
            else:
                self.bg_image = raw_bg
        except Exception as e:
            print(f"Erreur chargement background: {e}")

    def get_asset(self, index, file=None, size=SIZE):
        """Retourne l'image redimensionné, ou créé l'image pour la mettre dans le cache si elle n'y est pas déjà"""

        if index not in self.assets_cache and file:
            raw_image = PhotoImage(file=file)

            # Cette opération est très lourde, mais n'est fait qu'une seule fois au démarrage de l'app
            orig_size = raw_image.width()
            common = math.gcd(orig_size, size)
            zoom_val = size // common
            subsample_val = orig_size // common

            # Rajoute l'image au cache
            if subsample_val == zoom_val == 1:
                self.assets_cache[index] = raw_image
            else:
                self.assets_cache[index] = raw_image.zoom(zoom_val).subsample(
                    subsample_val
                )

        return self.assets_cache[index]

    def initialiser_canvas(self):
        """Créé le canvas et dessiner le fond et la grille"""

        # Calcule la largeur et la hauteur du canvas
        w_g, h_g = len(self.grille[0]), len(self.grille)
        w_canvas = 2 * PX - GAP + (GAP + SIZE) * w_g - 4
        h_canvas = 2 * PY - GAP + (GAP + SIZE) * h_g - 4

        # Créé le canvas
        self.canvas = tk.Canvas(self.conteneur, width=w_canvas, height=h_canvas)
        self.canvas.pack()

        # Dessine le background
        if self.bg_image:
            offset_x = (self.bg_image.width() - w_canvas) // 2
            offset_y = (self.bg_image.height() - h_canvas) // 2
            self.canvas.create_image(
                -offset_x, -offset_y, image=self.bg_image, anchor="nw"
            )

        # Dessine la grille
        for y in range(len(self.grille)):
            for x in range(len(self.grille[y])):
                x_pos = PX + (SIZE + GAP) * x
                y_pos = PY + (SIZE + GAP) * y

                tuile_type = ""
                if y == 0:
                    tuile_type += "T"
                elif y == len(self.grille) - 1:
                    tuile_type += "B"
                if x == 0:
                    tuile_type += "L"
                elif x == len(self.grille[0]) - 1:
                    tuile_type += "R"
                if tuile_type == "":
                    tuile_type = "C"

                tuile = self.get_asset(tuile_type)
                self.canvas.create_image(
                    x_pos - GAP / 2, y_pos - GAP / 2, image=tuile, anchor="nw"
                )

    def actualiser_bonbons(self, grille=None, bind_events=True):
        """Dessine ou actualise les bonbons"""

        # Supprime tous les éléments qui ont le tag dynamic
        self.canvas.delete("dynamic")

        if grille:
            g = grille
        else:
            g = self.grille

        # Affiche le selecteur de bonbon autour du bonbon choisi
        if self.bonbon_choisi:
            x_sel = PX - GAP + (SIZE + GAP) * self.bonbon_choisi[0]
            y_sel = PY - GAP + (SIZE + GAP) * self.bonbon_choisi[1]
            sel_img = self.get_asset("selected")
            self.canvas.create_image(
                x_sel, y_sel, image=sel_img, anchor="nw", tags="dynamic"
            )

        # Affiche les bonbons dans la grille
        for y in range(len(g)):
            for x in range(len(g[y])):
                if g[y][x] == "__":
                    continue

                x_pos = PX + (SIZE + GAP) * x
                y_pos = PY + (SIZE + GAP) * y

                if g[y][x][1] in "vhp":
                    bonbon_img = self.get_asset(
                        f"{COLOR_PATH[g[y][x][0]]}-{g[y][x][1]}"
                    )
                else:
                    bonbon_img = self.get_asset(COLOR_PATH[g[y][x][0]])

                bonbon = self.canvas.create_image(
                    x_pos, y_pos, image=bonbon_img, anchor="nw", tags="dynamic"
                )

                if bind_events:
                    self.canvas.tag_bind(
                        bonbon, "<Button-1>", self.create_callback(x, y)
                    )

        self.conteneur.root.update()

    def play_move(self):
        self.actualiser_bonbons(bind_events=False)
        stable = False
        while not stable:
            sleep(0.3)
            nouvelle_grille = supprimer_bonbons_en_ligne(self.grille)
            self.actualiser_bonbons(nouvelle_grille, bind_events=False)
            sleep(0.3)
            appliquer_gravite(nouvelle_grille)
            self.actualiser_bonbons(nouvelle_grille, bind_events=False)
            sleep(0.3)
            ajouter_bonbons_aleatoires(nouvelle_grille, self.nb_bonbons)
            self.actualiser_bonbons(nouvelle_grille, bind_events=False)
            stable = grille_est_stable(self.grille, nouvelle_grille)
            self.grille = nouvelle_grille
        self.actualiser_bonbons()

    def create_callback(self, x, y):
        def callback(e):
            if self.bonbon_choisi == (x, y):
                self.bonbon_choisi = None
            elif self.bonbon_choisi:
                echanger_deux_bonbons(self.grille, (x, y), self.bonbon_choisi)
                self.bonbon_choisi = None
                self.play_move()
            else:
                self.bonbon_choisi = (x, y)

            if jeu_est_bloque(self.grille):
                print("Le jeu est bloqué !")
            self.actualiser_bonbons()

        return callback


if __name__ == "__main__":
    jeu = CandyCrush(nb_bonbons=5, background="forest")
    jeu.main()
