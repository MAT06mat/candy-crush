import tkinter as tk
from tkinter import Tk, ttk
from fonctions import generer_grille, echanger_deux_bonbons, supprimer_bonbons_en_ligne

COLORS = ["#f15000", "#026edb", "#00d000", "#E3E300", "#be00ee", "#ee9700"]
COLORS_OUTLINE = ["#5d1f00", "#002f60", "#005d00", "#5B5B00", "#450056", "#573700"]
P = 10
SIZE = 50


class Grille:
    def __init__(self, conteneur, grille):
        self.conteneur = conteneur
        self.grille = grille
        self.bonbon_choisi = None  # None ou position sous forme (x, y)

        self.creer_canvas()

    def creer_canvas(self):
        g = self.grille
        w_g = len(g[0])
        h_g = len(g)

        w_canvas = P + (P + SIZE) * w_g
        h_canvas = P + (P + SIZE) * h_g
        canvas = tk.Canvas(self.conteneur, width=w_canvas, height=h_canvas, bg="white")

        def create_callback(x, y):
            def callback(e):
                if self.bonbon_choisi == (x, y):
                    self.bonbon_choisi = None
                elif self.bonbon_choisi:
                    echanger_deux_bonbons(self.grille, (x, y), self.bonbon_choisi)
                    self.bonbon_choisi = None
                else:
                    self.bonbon_choisi = (x, y)
                self.grille = supprimer_bonbons_en_ligne(self.grille)
                canvas.destroy()
                self.creer_canvas()

            return callback

        for y in range(len(g)):
            for x in range(len(g[y])):
                x_debut = P + (SIZE + P) * x
                x_fin = (SIZE + P) * (x + 1)
                y_debut = P + (SIZE + P) * y
                y_fin = (SIZE + P) * (y + 1)

                if self.bonbon_choisi == (x, y):
                    color = COLORS_OUTLINE[g[y][x]]
                else:
                    color = COLORS[g[y][x]]
                bonbon = canvas.create_oval(
                    (x_debut, y_debut),
                    (x_fin, y_fin),
                    fill=color,
                    activewidth=4,
                    activeoutline=COLORS_OUTLINE[g[y][x]],
                )
                canvas.tag_bind(bonbon, "<Button-1>", create_callback(x, y))
        canvas.pack()
        return canvas


root = Tk()
root.title("Candy Crush")
frame = ttk.Frame(root, padding=10)
# g = charger_grille("exemple_grille.csv")
g = generer_grille(7, 6)
frame2 = ttk.Frame(frame, padding=10)
Grille(frame2, g)
frame2.pack()
ttk.Button(frame, text="Click me !", command=print).pack()
frame.pack()
root.mainloop()
