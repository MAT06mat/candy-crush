import tkinter as tk
from tkinter import Tk, ttk, PhotoImage
import math
from fonctions import (
    generer_grille,
    echanger_deux_bonbons,
    supprimer_bonbons_en_ligne,
    jeu_est_bloque,
)

COLORS = ["#f15000", "#026edb", "#00d000", "#E3E300", "#be00ee", "#ee9700"]
COLORS_OUTLINE = ["#5d1f00", "#002f60", "#005d00", "#5B5B00", "#450056", "#573700"]
P = 8
SIZE = 50

COLOR_PATH = ["red", "blue", "green", "yellow", "purple", "orange"]
TUILES_PATH = ["TL", "T", "TR", "L", "C", "R", "BL", "B", "BR"]


class Grille:
    def __init__(self, conteneur, grille, background):
        self.conteneur = conteneur
        self.grille = grille
        self.bonbon_choisi = None  # None ou position sous forme (x, y)
        self.canvas = None
        self.assets_cache = {}

        self.bg_image = None
        self.charger_background(f"assets/backgrounds/{background}.png")
        self.charger_tuiles_grille()

        self.creer_canvas()

    def charger_background(self, path):
        """Charge et redimensionne le fond aux dimensions de la grille"""
        try:
            # Load the original large image
            raw_bg = PhotoImage(file=path)
            orig_w = raw_bg.width()
            orig_h = raw_bg.height()

            # Target canvas dimensions
            w_g, h_g = len(self.grille[0]), len(self.grille)
            target_w = P + (P + SIZE) * w_g
            target_h = P + (P + SIZE) * h_g

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

    def get_resized_asset(self, index, file=None, size=SIZE):
        """Returns the resized image from cache, or creates it if missing"""
        if index not in self.assets_cache and file:
            raw_image = PhotoImage(file=file)

            # Perform the heavy resizing logic only once per color
            orig_size = raw_image.width()
            common = math.gcd(orig_size, size)
            zoom_val = size // common
            subsample_val = orig_size // common

            self.assets_cache[index] = raw_image.zoom(zoom_val).subsample(subsample_val)

        return self.assets_cache[index]

    def charger_tuiles_grille(self):
        for tuile in TUILES_PATH:
            self.get_resized_asset(tuile, f"assets/grid/{tuile}.png", size=SIZE + P)

    def creer_canvas(self):
        g = self.grille
        w_g, h_g = len(g[0]), len(g)
        w_canvas = P + (P + SIZE) * w_g
        h_canvas = P + (P + SIZE) * h_g
        if self.canvas:
            self.canvas.delete("all")
        else:
            self.canvas = tk.Canvas(self.conteneur, width=w_canvas, height=h_canvas)
            self.canvas.pack()

        if self.bg_image:
            offset_x = (self.bg_image.width() - w_canvas) // 2
            offset_y = (self.bg_image.height() - h_canvas) // 2
            self.canvas.create_image(
                -offset_x, -offset_y, image=self.bg_image, anchor="nw"
            )

        if self.bonbon_choisi:
            selection_image = self.get_resized_asset(
                "selected", "assets/selected.png", SIZE + 2 * P
            )
            x_pos = (SIZE + P) * self.bonbon_choisi[0]
            y_pos = (SIZE + P) * self.bonbon_choisi[1]
            self.canvas.create_image(x_pos, y_pos, image=selection_image, anchor="nw")

        for y in range(len(g)):
            for x in range(len(g[y])):
                x_pos = P + (SIZE + P) * x
                y_pos = P + (SIZE + P) * y

                tuile_type = ""
                if y == 0:
                    tuile_type += "T"
                elif y == len(g) - 1:
                    tuile_type += "B"
                if x == 0:
                    tuile_type += "L"
                elif x == len(g[0]) - 1:
                    tuile_type += "R"
                if tuile_type == "":
                    tuile_type = "C"

                tuile = self.get_resized_asset(tuile_type)
                self.canvas.create_image(
                    x_pos - P / 2, y_pos - P / 2, image=tuile, anchor="nw"
                )

                if g[y][x] == -1:
                    continue

                img_path = f"assets/candies/{COLOR_PATH[g[y][x]]}.png"
                bonbon_image = self.get_resized_asset(g[y][x], img_path)

                bonbon = self.canvas.create_image(
                    x_pos, y_pos, image=bonbon_image, anchor="nw"
                )

                self.canvas.tag_bind(bonbon, "<Button-1>", self.create_callback(x, y))

    def create_callback(self, x, y):
        def callback(e):
            if self.bonbon_choisi == (x, y):
                self.bonbon_choisi = None
            elif self.bonbon_choisi:
                echanger_deux_bonbons(self.grille, (x, y), self.bonbon_choisi)
                self.bonbon_choisi = None
            else:
                self.bonbon_choisi = (x, y)
            self.grille = supprimer_bonbons_en_ligne(self.grille)
            jeu_est_bloque(self.grille)
            self.creer_canvas()

        return callback


root = Tk()
root.title("Candy Crush")
frame = ttk.Frame(root, padding=10)
# g = charger_grille("data/exemple_grille.csv")
g = generer_grille(10, 16, 3)
frame2 = ttk.Frame(frame, padding=10)
Grille(frame2, g, background="forest")
frame2.pack()
ttk.Button(frame, text="Click me !", command=lambda: print("Button click !")).pack()
frame.pack()
root.mainloop()
