import tkinter as tk
from tkinter import Tk, ttk, PhotoImage, messagebox
from font_manager import FontManager
from fonctions import *
from utils import *
from storage import storage
from button import CanvasButton, SmallCanvasButton, CanvasCircleHitBox
from assets import assets
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

    def __init__(self):
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

        self.bg_img = PhotoImage(file="v2/assets/background.png")
        self.canvas.create_image(0, 0, image=self.bg_img, anchor="nw")
        self.grille_view = None

        if storage.is_first_time:
            self.root.update()
            self.ouvrir_parametres()
        else:
            self.lancer_jeu()

    def ouvrir_parametres(self):
        """Ouvre la fenêtre de réglages en mode popup."""
        ParametresWindow(self.root, self.appliquer_parametres)

    def appliquer_parametres(self, h, l, n, coups):
        """Sauvegarde les réglages et (re)lance la partie."""

        _h = int(storage.get("lignes"))
        _l = int(storage.get("colonnes"))
        _n = int(storage.get("nb_bonbons"))
        _coups = int(storage.get("coups"))

        rep = False
        if (
            _h != h or _l != l or _n != n or _coups != coups
        ) and not storage.is_first_time:
            rep = messagebox.askyesno(
                "Enregistrer les paramètres",
                "Attention, l'enregistrement des paramètres redemarrera une nouvelle partie.\nVoulez-vous vraiment enregistrer les paramètres ?\nLa partie actuelle sera perdue.",
            )

        if rep or storage.is_first_time:
            if storage.is_first_time:
                storage.create_file()

            storage.set("lignes", h)
            storage.set("colonnes", l)
            storage.set("nb_bonbons", n)
            storage.set("coups", coups)

            self.lancer_jeu()

    def lancer_jeu(self):
        """Lance la grille avec les paramètres stockés en mémoire."""
        if self.grille_view:
            self.canvas.delete("dynamic")

        h = int(storage.get("lignes"))
        l = int(storage.get("colonnes"))
        n = int(storage.get("nb_bonbons"))
        coups = int(storage.get("coups"))

        grille_donnees = generer_grille(h, l, n)
        self.grille_view = Grille(
            self.canvas,
            grille_donnees,
            n,
            coups,
            self.width,
            self.height,
            self.ouvrir_parametres,
            self.lancer_jeu,
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

    def main(self):
        self.root.mainloop()


class ParametresWindow(tk.Toplevel):
    """
    Fenêtre secondaire pour configurer les paramètres du jeu.
    """

    def __init__(self, root: Tk, callback_valider):
        super().__init__(root)
        self.title("Réglages Candy Crush")
        self.geometry("400x500")
        self.resizable(False, False)

        self.root = root
        self.grab_set()  # Rend la fenêtre modale (bloque l'accès au jeu derrière)

        self.callback_valider = callback_valider

        # Variables de contrôle initialisées avec le storage
        self.val_h = tk.IntVar(value=int(storage.get("lignes")))
        self.val_l = tk.IntVar(value=int(storage.get("colonnes")))
        self.val_n = tk.IntVar(value=int(storage.get("nb_bonbons")))
        self.val_coups = tk.StringVar(value=storage.get("coups"))

        self.creer_widgets()
        self.bind("<Destroy>", self.on_destroy)

    def on_destroy(self, e):
        if isinstance(e.widget, tk.Toplevel):
            if storage.is_first_time:
                self.root.destroy()

    def snap_value(self, val, var, label_obj):
        """Arrondit la valeur du slider et met à jour son label."""
        n = int(round(float(val)))
        var.set(n)
        label_obj.config(text=str(n))

    def creer_widgets(self):
        """Crée l'interface de saisie dans la petite fenêtre."""

        tk.Label(self, text="PARAMÈTRES", font=("Helvetica", 18, "bold")).pack(pady=20)

        configs = [
            ("Lignes", self.val_h, 4, 10),
            ("Colonnes", self.val_l, 4, 12),
            ("Couleurs", self.val_n, 3, 6),
        ]

        for nom, var, v_min, v_max in configs:
            frame = tk.Frame(self)
            frame.pack(fill="x", padx=20, pady=10)

            tk.Label(frame, text=nom, font=("Helvetica", 10, "bold")).pack(side="left")

            val_label = tk.Label(
                frame, text=str(var.get()), fg="red", font=("Helvetica", 10, "bold")
            )
            val_label.pack(side="right")

            s = ttk.Scale(
                self, from_=v_min, to=v_max, variable=var, orient="horizontal"
            )
            s.config(command=lambda v, var=var, l=val_label: self.snap_value(v, var, l))
            s.pack(fill="x", padx=20)

        tk.Label(
            self, text="Nombre de coups max :", font=("Helvetica", 10, "bold")
        ).pack(pady=(20, 0))
        ttk.Entry(self, textvariable=self.val_coups, width=10, justify="center").pack(
            pady=5
        )

        frame = tk.Frame(self)
        frame.pack(pady=30)
        ttk.Button(frame, text="Valider et jouer", width=15, command=self.valider).grid(
            row=0, column=0, padx=5
        )
        ttk.Button(frame, text="Annuler", width=9, command=self.destroy).grid(
            row=0, column=1, padx=5
        )

    def valider(self):
        try:
            h, l, n = self.val_h.get(), self.val_l.get(), self.val_n.get()
            c = int(self.val_coups.get())
            if c <= 0:
                raise ValueError()
            if c > 999999:
                c = 999999
            self.callback_valider(h, l, n, c)
            self.destroy()
        except ValueError:
            messagebox.showerror(
                "Erreur", "Le nombre de coups doit être un entier strictement positif."
            )


class Grille:
    """
    Gère l'affichage graphique de la grille, les animations et les interactions utilisateur.
    """

    def __init__(
        self, canvas: tk.Canvas, grille, nb_bonbons, coups, sw, sh, callback, lancer_jeu
    ):
        """
        Initialise le moteur graphique du plateau de jeu.

        Args:
            canvas (Canvas): Le parent Tkinter.
            grille (list): Liste 2D représentant les bonbons.
            nb_bonbons (int): Nombre de types de bonbons.
            coups (int): Nombre de coups restant
            sw (int): Largeur de la fenêtre
            sh (int): Hauteur de la fenêtre
            callback (func): Fonction pour ouvrir le menu
        """
        self.canvas = canvas
        self.root = canvas.winfo_toplevel()
        self.grille = grille
        self.nb_bonbons = nb_bonbons
        self.callback_menu = callback
        self.callback_lancer_jeu = lancer_jeu
        self.coups_restant = coups

        self.bonbon_choisi = None  # Stocke (x, y) du premier bonbon cliqué
        self.assets_cache = {}  # Cache pour éviter de recharger les images
        self.items = {}  # Dictionnaire {(x, y): canvas_id}
        self.is_animating = False
        self.score = 0
        self.partie_finie = False
        self.dernier_score = 0

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
        self.py = (self.height - grid_height) // 2 + 43

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
        topbar = assets.get("topbar")
        pos_x = self.width - 1024
        self.canvas.create_image(pos_x, 0, image=topbar, anchor="nw", tags="dynamic")

        topbar_part = assets.get("topbar-part")
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
            fill="#92143e",
            outline="#febfc7",
            tags="dynamic",
        )

        self.draw_score()

        # Frame des coups restants
        small_frame = assets.get("small-frame")
        self.canvas.create_image(
            self.px - 218, self.py - 2, image=small_frame, anchor="nw", tags="dynamic"
        )
        self.draw_coups_restant()

        button_y_start = self.py + 134

        if self.partie_finie or self.coups_restant <= 0:
            # Bouton Rejouer
            SmallCanvasButton(
                self.canvas,
                self.px - 205,
                button_y_start,
                "Rejouer",
                self.callback_lancer_jeu,
            )
            button_y_start += 46

        # Bouton Menu avec confirmation
        SmallCanvasButton(
            self.canvas,
            self.px - 205,
            button_y_start,
            "Réglages",
            self.callback_menu,
        )

        button_y_start += 46

        # Bouton Quitter
        SmallCanvasButton(
            self.canvas,
            self.px - 205,
            button_y_start,
            "Quitter",
            self.confirmer_quitter,
        )

        if self.partie_finie:
            pos_x = self.width
            pos_y = 0
            shadow = assets.get("shadow")
            frame = assets.get("frame")
            center_x = self.width // 2
            center_y = self.height // 2

            while pos_x > 0:
                pos_x -= 960
                while pos_y < self.height:
                    self.canvas.create_image(
                        pos_x, pos_y, image=shadow, anchor="nw", tags="dynamic"
                    )
                    pos_y += 540
                pos_y = 0

            x = center_x - 339
            y = center_y - 251
            self.canvas.create_image(x, y, image=frame, anchor="nw", tags="dynamic")

            self.canvas.create_text(
                center_x - 34,
                center_y - 180,
                text="Fin",
                font=("candice", 34, "bold"),
                fill="#fefefe",
                anchor="w",
                tags="dynamic",
            )

            self.canvas.create_text(
                center_x - 38,
                center_y - 184,
                text="Fin",
                font=("candice", 34, "bold"),
                fill="#143a7c",
                anchor="w",
                tags="dynamic",
            )

            self.canvas.create_text(
                center_x - 240,
                center_y - 80,
                text=f"Score de la partie : {self.score}",
                font=("candice", 26),
                fill="#76203c",
                anchor="w",
                tags="dynamic",
            )

            self.canvas.create_text(
                center_x - 240,
                center_y - 20,
                text=f"Meilleur score : {storage.get("meilleur_score")}",
                font=("candice", 26),
                fill="#76203c",
                anchor="w",
                tags="dynamic",
            )

            self.canvas.create_text(
                center_x - 240,
                center_y + 40,
                text=f"Dernier score : {self.dernier_score}",
                font=("candice", 26),
                fill="#76203c",
                anchor="w",
                tags="dynamic",
            )

            CanvasButton(
                self.canvas,
                center_x - 260,
                center_y + 105,
                "Rejouer",
                self.callback_lancer_jeu,
            )

            CanvasButton(
                self.canvas,
                center_x + 12,
                center_y + 105,
                "Quitter",
                lambda: self.root.after(10, self.root.destroy),
            )

            def close():
                self.partie_finie = False
                self.recharger_composant()

            CanvasCircleHitBox(self.canvas, center_x + 287, center_y - 162, 37, close)

    def confirmer_quitter(self):
        """Demande confirmation avant de quitter la partie en cours."""
        rep = True
        if not self.partie_finie and self.coups_restant > 0:
            rep = messagebox.askyesno(
                "Quitter",
                "Voulez-vous vraiment quitter la partie en cours ?\nLa partie actuelle sera perdue.",
            )
        if rep:
            self.root.after(10, self.root.destroy)

    def create_outlined_text(self, x, y, *args, fill, outline, **kwargs):
        self.canvas.create_text(x + 2, y + 2, fill=outline, *args, **kwargs)
        self.canvas.create_text(x, y, fill=fill, *args, **kwargs)

    def charger_assets(self):
        """Charge toutes les images nécessaires (bonbons, bonus, tuiles) dans le cache."""
        for _, color in COLOR_PATH.items():
            for bonus in ["", "-h", "-v", "-p"]:
                path = f"candies/{color + bonus}.png"
                assets.load(color + bonus, path)

        assets.load("rainbow", "candies/rainbow.png")

        for tuile in TUILES_PATH:
            assets.load(tuile, f"grid/{tuile}.png", SIZE + GAP)

        assets.load("selected", "selected.png", SIZE + 2 * GAP)
        assets.load("topbar", "elements/topbar.png")
        assets.load("topbar-part", "elements/topbar-part.png")
        assets.load("frame", "elements/frame.png")
        assets.load("small-frame", "elements/small-frame.png")
        assets.load("shadow", "elements/shadow.png")

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

                img_tuile = assets.get(tuile_type if tuile_type else "C")
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
            return assets.get("rainbow")

        color_name = COLOR_PATH.get(val[0], "red")
        suffix = f"-{val[1]}" if len(val) > 1 and val[1] in "vhp" else ""
        return assets.get(color_name + suffix)

    def draw_score(self):
        """Actualise le texte du score"""

        self.canvas.delete("score")
        self.canvas.create_text(
            self.width - 325,
            48,
            text=f"Score : {int(self.score)}",
            font=("candice", 26, "bold"),
            fill="#76203c",
            anchor="w",
            tags="dynamic score",
        )

    def draw_coups_restant(self):
        """Actualise le texte des coups restant"""

        self.canvas.delete("coups")
        self.canvas.create_text(
            self.px - 192,
            self.py + 62,
            text=f"Coups :\n{int(self.coups_restant)}",
            font=("candice", 22, "bold"),
            justify="center",
            fill="#76203c",
            anchor="w",
            tags="dynamic coups",
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
                self.coups_restant -= 1
                self.draw_coups_restant()
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
                        new_score += 5
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

            if self.coups_restant <= 0:
                meilleur_score = storage.get("meilleur_score")
                self.score = int(self.score)
                if not meilleur_score.isdigit() or self.score > int(meilleur_score):
                    meilleur_score = str(self.score)
                    storage.set("meilleur_score", meilleur_score)
                self.dernier_score = storage.get("dernier_score")
                storage.set("dernier_score", self.score)
                self.partie_finie = True
                self.supprimer_bindings()
                self.root.after(500, self.recharger_composant)
            else:
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
            self.score = int(final)
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
                image=assets.get("selected"),
                anchor="nw",
                tags="selector dynamic",
            )

    def actualiser_bindings(self):
        """Réattache les clics sur les objets du canvas après remaniement de la grille."""
        for (x, y), item_id in self.items.items():
            self.canvas.tag_bind(item_id, "<Button-1>", self.create_callback(x, y))

    def supprimer_bindings(self):
        """Supprimer les clics sur les bonbons de la grille."""
        for _, item_id in self.items.items():
            self.canvas.tag_unbind(item_id, "<Button-1>")

    def create_callback(self, x, y):
        """Crée une fonction de rappel pour le clic sur un bonbon spécifique."""
        return lambda e: self.on_click(x, y)

    def on_click(self, x, y):
        """Gère la logique de sélection et de déplacement au clic."""
        if self.is_animating or self.coups_restant <= 0:
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
