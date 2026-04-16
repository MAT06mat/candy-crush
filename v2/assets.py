from tkinter import PhotoImage
import math, os


class Assets:
    def __init__(self, base="") -> None:
        self.base = base
        self.cache: dict[str, PhotoImage] = {}

    def load(self, index: str, file: str, size=None) -> PhotoImage:
        if index not in self.cache:
            raw = PhotoImage(file=os.path.join(self.base, file))
            if size:
                # Calcul du ratio pour un redimensionnement propre via zoom/subsample
                diviseur_commun = math.gcd(raw.width(), size)
                self.cache[index] = raw.zoom(size // diviseur_commun).subsample(
                    raw.width() // diviseur_commun
                )
            else:
                self.cache[index] = raw
        return self.cache[index]

    def get(self, index: str) -> PhotoImage:
        return self.cache[index]


assets = Assets("v2/assets/")
