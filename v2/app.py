import tkinter as tk
from tkinter import Tk, ttk, PhotoImage
from font_manager import FontManager
from fonctions import *
from utils import *
import math

# --- Configuration Visuelle ---
GAP = 4
SIZE = 72

# --- Paramètres Techniques ---
COLOR_PATH = {
    "0": "red",
    "1": "blue",
    "2": "green",
    "3": "yellow",
    "4": "purple",
    "5": "orange",
}
TUILES_PATH = ["TL", "T", "TR", "L", "C", "R", "BL", "B", "BR"]


FontManager.load_font("v2/assets/font.ttf")


class CandyCrush:
    """
    Classe principale gérant la fenêtre du jeu et l'initialisation globale.
    """

    def __init__(self, background="background"):
        self.width = 1520
        self.height = 780

        self.root = Tk()
        self.root.title("Candy Crush")
        self.root.geometry(f"{self.width}x{self.height}+0+0")
        self.root.minsize(1200, 675)
        self.root.maxsize(1920, 1080)

        self.root.bind("<Configure>", self.on_configure)

        self.canvas = tk.Canvas(
            self.root, width=self.width, height=self.height, highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        self.bg_img = PhotoImage(file=f"v2/assets/backgrounds/{background}.png")
        self.canvas.create_image(0, 0, image=self.bg_img, anchor="nw")

        self.grille_view = None
        self.menu = None
        self.creer_menu()

    def creer_menu(self):
        """Initialise le menu de configuration."""
        self.menu = Menu(self.canvas, self.width, self.height, self.lancer_partie)

    def lancer_partie(self, h, l, n, coups):
        """Détruit le menu et lance la grille."""
        self.canvas.delete("dynamic")
        self.menu = None
        self.creer_grille(largeur=l, hauteur=h, nb_bonbons=n)

    def creer_grille(self, largeur=7, hauteur=6, nb_bonbons=6):
        grille_donnees = generer_grille(hauteur, largeur, nb_bonbons)
        self.grille_view = Grille(
            self.canvas, grille_donnees, nb_bonbons, sw=self.width, sh=self.height
        )

    def on_configure(self, event):
        if not isinstance(event.widget, tk.Tk):
            return
        self.width = event.width
        self.height = event.height
        self.canvas.config(width=self.width, height=self.height)
        if self.grille_view:
            self.grille_view.set_size(self.width, self.height)
            self.grille_view.recharger_composant()
        if self.menu:
            self.menu.set_size(self.width, self.height)
            self.menu.recharger_composant()

    def main(self):
        self.root.mainloop()


class Menu:
    """
    Gère l'affichage du popup avec des textes natifs au Canvas pour éviter les glitchs.
    """

    def __init__(self, canvas: tk.Canvas, sw, sh, callback_valider):
        self.canvas = canvas
        self.root = canvas.winfo_toplevel()
        self.callback_valider = callback_valider

        # Variables de contrôle
        self.val_h = tk.IntVar(value=6)
        self.val_l = tk.IntVar(value=7)
        self.val_n = tk.IntVar(value=5)
        self.val_coups = tk.StringVar(value="30")

        self.set_size(sw, sh)
        self.draw_interface()

    def set_size(self, w, h):
        self.width = w
        self.height = h
        self.px = self.width // 2
        self.py = self.height // 2

    def recharger_composant(self):
        self.canvas.delete("dynamic")
        self.draw_interface()

    def snap_value(self, val, var, tag):
        """Arrondit la valeur et met à jour le texte du Canvas manuellement."""
        n = int(round(float(val)))
        var.set(n)
        self.canvas.itemconfig(tag, text=str(n))

    def draw_interface(self):
        """Dessine l'interface en utilisant create_text pour les valeurs."""

        # --- Fond du popup ---
        menu_w, menu_h = 450, 550
        self.canvas.create_rectangle(
            self.px - menu_w // 2,
            self.py - menu_h // 2,
            self.px + menu_w // 2,
            self.py + menu_h // 2,
            fill="#FFFFFF",
            outline="#472E09",
            width=4,
            tags="dynamic",
        )

        self.canvas.create_text(
            self.px,
            self.py - 230,
            text="Paramètres",
            font=("candice", 32),
            fill="#472E09",
            tags="dynamic",
        )

        # --- Configuration des Sliders ---
        configs = [
            ("Lignes (Vertical) : ", self.val_h, 4, 10, -140, "val_h_txt"),
            ("Colonnes (Horizontal) : ", self.val_l, 4, 12, -60, "val_l_txt"),
            ("Types de bonbons : ", self.val_n, 3, 6, 20, "val_n_txt"),
        ]

        slider_len = 300

        for text, var, v_min, v_max, y_off, tag in configs:
            # Libellé fixe
            self.canvas.create_text(
                self.px - 180,
                self.py + y_off,
                text=text,
                font=("Helvetica", 12, "bold"),
                anchor="w",
                fill="#472E09",
                tags="dynamic",
            )

            # Valeur dynamique
            self.canvas.create_text(
                self.px + 150,
                self.py + y_off,
                text=str(var.get()),
                font=("Helvetica", 12, "bold"),
                fill="#E74C3C",
                tags=f"dynamic {tag}",
                anchor="center",
            )

            # Slider
            slider = ttk.Scale(
                self.root,
                from_=v_min,
                to=v_max,
                variable=var,
                orient="horizontal",
                length=slider_len,
                command=lambda v, var=var, tag=tag: self.snap_value(v, var, tag),
            )
            self.canvas.create_window(
                self.px, self.py + y_off + 30, window=slider, tags="dynamic"
            )

            # Min / Max
            self.canvas.create_text(
                self.px - (slider_len // 2),
                self.py + y_off + 50,
                text=str(v_min),
                font=("Helvetica", 10),
                fill="#7F8C8D",
                tags="dynamic",
            )
            self.canvas.create_text(
                self.px + (slider_len // 2),
                self.py + y_off + 50,
                text=str(v_max),
                font=("Helvetica", 10),
                fill="#7F8C8D",
                tags="dynamic",
            )

        # --- Entry pour les coups ---
        self.canvas.create_text(
            self.px - 180,
            self.py + 110,
            text="Nombre de coups max :",
            font=("Helvetica", 12, "bold"),
            anchor="w",
            fill="#472E09",
            tags="dynamic",
        )

        entry_coups = ttk.Entry(
            self.root, textvariable=self.val_coups, width=10, justify="center"
        )
        self.canvas.create_window(
            self.px + 100, self.py + 110, window=entry_coups, tags="dynamic"
        )

        # --- Bouton Valider ---
        btn_valider = ttk.Button(
            self.root, text="LANCER LA PARTIE", command=self.valider_settings
        )
        self.canvas.create_window(
            self.px,
            self.py + 200,
            window=btn_valider,
            tags="dynamic",
            height=40,
            width=200,
        )

    def valider_settings(self):
        try:
            h, l, n = self.val_h.get(), self.val_l.get(), self.val_n.get()
            coups = int(self.val_coups.get())
            self.callback_valider(h, l, n, coups)
        except ValueError:
            pass


class Grille:
    """
    Gère l'affichage graphique de la grille, les animations et les interactions utilisateur.
    """

    def __init__(self, canvas: tk.Canvas, grille, nb_bonbons, sw, sh):
        """
        Initialise le moteur graphique du plateau de jeu.

        Args:
            canvas (Canvas): Le parent Tkinter.
            grille (list): Liste 2D représentant les bonbons.
            nb_bonbons (int): Nombre de types de bonbons.
            sw (int): Largeur de la fenêtre
            sh (int): Hauteur de la fenêtre
        """
        self.canvas = canvas
        self.root = canvas.winfo_toplevel()
        self.grille = grille
        self.nb_bonbons = nb_bonbons

        self.bonbon_choisi = None  # Stocke (x, y) du premier bonbon cliqué
        self.assets_cache = {}  # Cache pour éviter de recharger les images
        self.items = {}  # Dictionnaire {(x, y): canvas_id}
        self.is_animating = False
        self.score = 0

        # Calcul dynamique du padding pour centrer la grille
        self.set_size(sw, sh)

        # Chargement de toutes les images et de l'interface
        self.charger_assets()
        self.dessiner_plateau()
        self.initialiser_bonbons()
        self.ajouter_interface()

    def set_size(self, w, h):
        self.width = w
        self.height = h
        grid_width = len(self.grille[0]) * (SIZE + GAP)
        grid_height = len(self.grille) * (SIZE + GAP)
        self.px = (self.width - grid_width) // 2
        self.py = (self.height - grid_height) // 2

    def recharger_composant(self):
        """Recharge tous les elements du canvas sauf le bg"""
        self.canvas.delete("dynamic")
        self.dessiner_plateau()
        self.initialiser_bonbons()
        self.ajouter_interface()

    def ajouter_interface(self):
        """
        Ajoute des éléments UI (boutons, texte) par-dessus le fond.
        """
        # Ajout de la topbar
        topbar = self.get_asset("topbar")
        pos_x = self.width - 1024
        self.canvas.create_image(pos_x, 0, image=topbar, anchor="nw", tags="dynamic")

        topbar_part = self.get_asset("topbar-part")
        while pos_x > 0:
            pos_x -= 255
            self.canvas.create_image(
                pos_x, 0, image=topbar_part, anchor="nw", tags="dynamic"
            )

        # Ajout du text Candy Crush
        self.create_outlined_text(
            172,
            42,
            text="Candy Crush",
            font=("candice", 36, "bold"),
            fill="#F3DE76",
            outline="#472E09",
            tags="dynamic",
        )

        self.draw_score()

        # Ajout du bonton quitter via create_window
        btn_quitter = ttk.Button(self.root, text="Quitter", command=self.root.destroy)
        self.canvas.create_window(
            self.px - 100, self.py, window=btn_quitter, tags="dynamic"
        )

    def create_outlined_text(
        self, x, y, *args, fill="white", outline="black", outline_width=3, **kwargs
    ):
        for teta in [n * math.pi / 4 for n in range(8)]:
            dx = outline_width * math.cos(teta)
            dy = outline_width * math.sin(teta)
            self.canvas.create_text(x + dx, y + dy, fill=outline, *args, **kwargs)
        self.canvas.create_text(x, y, fill=fill, *args, **kwargs)

    def charger_assets(self):
        """Charge toutes les images nécessaires (bonbons, bonus, tuiles) dans le cache."""
        for _, color in COLOR_PATH.items():
            for bonus in ["", "-h", "-v", "-p"]:
                path = f"v2/assets/candies/{color + bonus}.png"
                self.get_asset(color + bonus, path)

        self.get_asset("rainbow", "v2/assets/candies/rainbow.png")

        for tuile in TUILES_PATH:
            self.get_asset(tuile, f"v2/assets/grid/{tuile}.png", size=SIZE + GAP)

        self.get_asset("selected", "v2/assets/selected.png", SIZE + 2 * GAP)
        self.get_asset("topbar", "v2/assets/elements/topbar.png", 1024)
        self.get_asset("topbar-part", "v2/assets/elements/topbar-part.png", 256)

    def dessiner_plateau(self):
        """Dessine les tuiles de la grille en utilisant les offsets px et py."""
        for y in range(len(self.grille)):
            for x in range(len(self.grille[y])):
                px_item, py_item = self.get_pixel_pos(x, y)

                tuile_type = ""
                if y == 0:
                    tuile_type += "T"
                elif y == len(self.grille) - 1:
                    tuile_type += "B"
                if x == 0:
                    tuile_type += "L"
                elif x == len(self.grille[0]) - 1:
                    tuile_type += "R"

                img_tuile = self.get_asset(tuile_type if tuile_type else "C")
                self.canvas.create_image(
                    px_item - GAP / 2,
                    py_item - GAP / 2,
                    image=img_tuile,
                    anchor="nw",
                    tags="dynamic",
                )

    def initialiser_bonbons(self):
        """Remplit le plateau avec les bonbons initiaux."""
        for y in range(len(self.grille)):
            for x in range(len(self.grille[y])):
                self.creer_bonbon_item(x, y)

    def get_asset(self, index: str, file: str | None = None, size=SIZE) -> PhotoImage:
        """
        Récupère une image redimensionnée ou la crée si elle n'existe pas.

        Args:
            index (str): Identifiant unique de l'image.
            file (str): Chemin du fichier (si création).
            size (int): Taille cible en pixels.
        """
        if index not in self.assets_cache and file:
            raw = PhotoImage(file=file)
            # Calcul du ratio pour un redimensionnement propre via zoom/subsample
            diviseur_commun = math.gcd(raw.width(), size)
            self.assets_cache[index] = raw.zoom(size // diviseur_commun).subsample(
                raw.width() // diviseur_commun
            )
        return self.assets_cache[index]

    def get_pixel_pos(self, x, y):
        """Convertit les coordonnées de la grille (x, y) en position pixels (px, py)."""
        return self.px + (SIZE + GAP) * x, self.py + (SIZE + GAP) * y

    def creer_bonbon_item(self, x, y):
        """Crée l'objet graphique du bonbon sur le canvas."""
        val = self.grille[y][x]
        if val == "__":
            return

        px, py = self.get_pixel_pos(x, y)
        img = self.get_candy_image(val)

        item_id = self.canvas.create_image(
            px, py, image=img, anchor="nw", tags="dynamic"
        )
        self.items[(x, y)] = item_id
        # Liaison de l'événement clic
        self.canvas.tag_bind(item_id, "<Button-1>", self.create_callback(x, y))

    def get_candy_image(self, val):
        """Détermine l'image correcte à partir de la chaîne de caractères du bonbon."""
        if val == "__":
            return None
        if val == "r_":
            return self.get_asset("rainbow")

        color_name = COLOR_PATH.get(val[0], "red")
        suffix = f"-{val[1]}" if len(val) > 1 and val[1] in "vhp" else ""
        return self.get_asset(color_name + suffix)

    def draw_score(self):
        """Actualise le texte du score"""

        self.canvas.delete("score")
        self.canvas.create_text(
            self.width - 325,
            48,
            text=f"Score : {int(self.score)}",
            font=("candice", 26, "bold"),
            fill="#2F6D0F",
            anchor="w",
            tags="dynamic score",
        )

    def animate_move(self, movements, step=0, callback=None):
        """
        Déplace fluidement un ou plusieurs objets sur le canvas.

        Args:
            movements (list): Liste de listes [item_id, dx, dy].
            step (int): Étape actuelle de l'animation.
            callback (function): Action à exécuter après la fin du mouvement.
        """
        if step >= STEPS:
            if callback:
                callback()
            return

        for move in movements:
            self.canvas.move(move[0], move[1][step], move[2][step])

        self.root.after(
            ANIM_SPEED, lambda: self.animate_move(movements, step + 1, callback)
        )

    def play_move(self, x, y):
        """Gère la séquence d'échange de deux bonbons."""
        if self.is_animating or not self.bonbon_choisi:
            return

        x_prev, y_prev = self.bonbon_choisi
        # Vérification de la proximité (voisins directs uniquement)
        if abs(x_prev - x) + abs(y_prev - y) != 1:
            self.bonbon_choisi = None
            self.actualiser_selecteur()
            return

        self.is_animating = True
        self.bonbon_choisi = None
        self.actualiser_selecteur()

        id1, id2 = self.items[(x, y)], self.items[(x_prev, y_prev)]
        px1, py1 = self.get_pixel_pos(x, y)
        px2, py2 = self.get_pixel_pos(x_prev, y_prev)

        def after_swap():
            # Échange des données logiques
            echanger_deux_bonbons(self.grille, (x, y), (x_prev, y_prev))
            nouvelle = supprimer_bonbons_en_ligne(self.grille, (x_prev, y_prev), (x, y))

            if self.grille == nouvelle:
                # Mouvement invalide : on annule visuellement l'échange
                self.animate_move(
                    [
                        create_animation(id1, ANIM_SWAP, px1 - px2, py1 - py2),
                        create_animation(id2, ANIM_SWAP, px2 - px1, py2 - py1),
                    ],
                    callback=self.end_animation_revert,
                )
                echanger_deux_bonbons(self.grille, (x, y), (x_prev, y_prev))
            else:
                # Mouvement validé : mise à jour du dictionnaire d'items
                self.items[(x, y)], self.items[(x_prev, y_prev)] = id2, id1
                self.resolve_board(nouvelle, (x, y), (x_prev, y_prev))

        # Animation d'échange
        self.animate_move(
            [
                create_animation(id1, ANIM_SWAP, px2 - px1, py2 - py1),
                create_animation(id2, ANIM_SWAP, px1 - px2, py1 - py2),
            ],
            callback=after_swap,
        )

    def end_animation_revert(self):
        """Réactive les clics après une annulation d'échange."""
        self.is_animating = False

    def resolve_board(self, grille_post_suppression=None, pos_i=None, pos_f=None):
        """
        Orchestre la cascade : destruction, gravité, remplissage.
        """
        if grille_post_suppression is not None:
            nouvelle = grille_post_suppression
        else:
            nouvelle = supprimer_bonbons_en_ligne(self.grille, pos_i, pos_f)

        to_destroy, to_transform = [], []

        new_score = self.score
        # Comparaison pour identifier les changements
        for y in range(len(self.grille)):
            for x in range(len(self.grille[0])):
                old, new = self.grille[y][x], nouvelle[y][x]
                if old != "__":
                    if new == "__":
                        new_score += 5
                        if old[1] != "_" or old[0] == "r":
                            match old[1]:
                                case "h" | "v":
                                    new_score += 10
                                case "p":
                                    new_score += 20
                                case _:
                                    new_score += 95

                        to_destroy.append((x, y))
                    elif new != old:
                        to_transform.append((x, y, new))

        scores = create_animation(
            None, ANIM_SCORE, new_score - self.score, steps=2 * STEPS
        )[1]

        self.animate_score(
            scores,
            final=new_score,
        )

        if not to_destroy and not to_transform:
            self.is_animating = False
            self.actualiser_bindings()
            return

        self.animate_destruction(
            to_destroy, to_transform, lambda: self.after_destruction(nouvelle)
        )

    def animate_score(self, scores, final, step=0):
        """
        Rafraichit fluidement le score.

        Args:
            movements (list): Liste de scores .
            step (int): Étape actuelle de l'animation.
        """
        if step >= len(scores):
            self.score = final
            self.draw_score()
            return

        self.score += scores[step]
        self.draw_score()
        self.root.after(ANIM_SPEED, lambda: self.animate_score(scores, final, step + 1))

    def animate_destruction(self, destroy_coords, transform_data, callback, step=0):
        """Fait clignoter les bonbons détruits et transforme les bonus."""
        if step >= 4:
            for x, y in destroy_coords:
                if (x, y) in self.items:
                    self.canvas.delete(self.items[x, y])
                    del self.items[x, y]

            for x, y, val in transform_data:
                if (x, y) in self.items:
                    self.canvas.itemconfig(
                        self.items[x, y], image=self.get_candy_image(val)
                    )

            callback()
            return

        # Effet visuel de clignotement
        visibilite = "hidden" if step % 2 == 0 else "normal"
        for x, y in destroy_coords:
            if (x, y) in self.items:
                self.canvas.itemconfig(self.items[x, y], state=visibilite)

        self.root.after(
            80,
            lambda: self.animate_destruction(
                destroy_coords, transform_data, callback, step + 1
            ),
        )

    def after_destruction(self, nouvelle_grille):
        """Lance l'animation de gravité après la phase de destruction."""
        self.grille = nouvelle_grille
        self.animate_gravity(lambda: self.after_gravity())

    def animate_gravity(self, callback):
        """Calcule et anime la chute des bonbons existants vers le bas."""
        movements, new_items = [], {}

        for x in range(len(self.grille[0])):
            vides = 0
            for y in range(len(self.grille) - 1, -1, -1):
                if self.grille[y][x] == "__":
                    vides += 1
                elif vides > 0:
                    item_id = self.items.pop((x, y))
                    target_y = y + vides
                    dist_px = vides * (SIZE + GAP)
                    movements.append(
                        create_animation(item_id, ANIM_GRAVITY, 0, dist_px)
                    )
                    new_items[(x, target_y)] = item_id
                else:
                    if (x, y) in self.items:
                        new_items[(x, y)] = self.items.pop((x, y))

        self.items = new_items

        if not movements:
            callback()
        else:
            appliquer_gravite(self.grille)
            self.animate_move(movements, callback=callback)

    def after_gravity(self):
        """Remplit les trous et vérifie si de nouveaux alignements sont créés."""
        ajouter_bonbons_aleatoires(self.grille, self.nb_bonbons)
        self.animate_refill(lambda: self.resolve_board())

    def animate_refill(self, callback):
        """Anime l'entrée de nouveaux bonbons depuis le haut de l'écran."""
        movements = []
        for y in range(len(self.grille)):
            for x in range(len(self.grille[0])):
                if (x, y) not in self.items:
                    px, py_final = self.get_pixel_pos(x, y)
                    py_start = py_final - (SIZE * 2)  # Départ hors champ

                    item_id = self.canvas.create_image(
                        px,
                        py_start,
                        image=self.get_candy_image(self.grille[y][x]),
                        anchor="nw",
                        tags="dynamic",
                    )
                    self.items[(x, y)] = item_id
                    movements.append(
                        create_animation(item_id, ANIM_GRAVITY, 0, py_final - py_start)
                    )

        if not movements:
            callback()
        else:
            self.animate_move(movements, callback=callback)

    def actualiser_selecteur(self):
        """Affiche ou cache le cadre de sélection autour du bonbon actif."""
        self.canvas.delete("selector")
        if self.bonbon_choisi:
            px, py = self.get_pixel_pos(*self.bonbon_choisi)
            self.canvas.create_image(
                px - GAP,
                py - GAP,
                image=self.get_asset("selected"),
                anchor="nw",
                tags="selector dynamic",
            )

    def actualiser_bindings(self):
        """Réattache les clics sur les objets du canvas après remaniement de la grille."""
        for (x, y), item_id in self.items.items():
            self.canvas.tag_bind(item_id, "<Button-1>", self.create_callback(x, y))

    def create_callback(self, x, y):
        """Crée une fonction de rappel pour le clic sur un bonbon spécifique."""
        return lambda e: self.on_click(x, y)

    def on_click(self, x, y):
        """Gère la logique de sélection et de déplacement au clic."""
        if self.is_animating:
            return

        if self.bonbon_choisi == (x, y):
            self.bonbon_choisi = None
        elif self.bonbon_choisi:
            self.play_move(x, y)
        else:
            self.bonbon_choisi = (x, y)
        self.actualiser_selecteur()


if __name__ == "__main__":
    jeu = CandyCrush()
    jeu.main()
