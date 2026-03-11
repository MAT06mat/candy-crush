import tkinter as tk
from tkinter import Tk, ttk
from fonctions import charger_grille

COLORS = ["#f15000", "#0065d0", "#00d000", "#E3E300", "#be00ee"]
COLORS_OUTLINE = ["#5d1f00", "#002f60", "#005d00", "#5B5B00", "#450056"]
P = 10
SIZE = 50


def creer_canvas(r, g):
    w_g = len(g[0])
    h_g = len(g)

    w_canvas = P + (P + SIZE) * w_g
    h_canvas = P + (P + SIZE) * h_g
    canvas = tk.Canvas(r, width=w_canvas, height=h_canvas, bg="white")

    def callback(event):
        x = (event.x - P) // (SIZE + P)
        y = (event.y - P) // (SIZE + P)
        color = g[y][x]
        print("Click at:", x, y, "Color:", color)

    for y in range(len(g)):
        for x in range(len(g[y])):
            x_debut = P + (SIZE + P) * x
            x_fin = (SIZE + P) * (x + 1)
            y_debut = P + (SIZE + P) * y
            y_fin = (SIZE + P) * (y + 1)
            canvas.create_oval(
                (x_debut, y_debut),
                (x_fin, y_fin),
                fill=COLORS[g[y][x]],
                activewidth=4,
                activeoutline=COLORS_OUTLINE[g[y][x]],
            )
    canvas.bind("<Button-1>", callback)
    canvas.pack()


root = Tk()
root.title("Candy Crush")
frame = ttk.Frame(root, padding=10)
g = charger_grille("exemple_grille.csv")
creer_canvas(frame, g)
ttk.Button(frame, text="Click me !", command=print).pack()
frame.pack()
root.mainloop()
