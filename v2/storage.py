import os


default_settings = {
    "lignes": 6,
    "colonnes": 7,
    "nb_bonbons": 5,
    "coups": "30",
    "dernier_score": 0,
    "meilleur_score": 0,
}


class Storage:
    def __init__(self) -> None:
        self.file_name = "data.csv"
        self.is_first_time = False

        content = ""
        if os.path.exists(self.file_name):
            with open(self.file_name, "r") as file:
                content = file.read()

        if content == "":
            self.is_first_time = True
            self._storage = {}
        else:
            self.load_file_storage()

    def create_file(self):
        print(f"Le fichier de stockage n'existe pas... Création de {self.file_name}")
        with open(self.file_name, "w") as file:
            file.write(
                "\n".join(f"{key}:{item}" for key, item in default_settings.items())
            )
        self.is_first_time = False

    def load_file_storage(self):
        with open(self.file_name, "r") as file:
            self._storage = {
                line.split(":")[0]: line.split(":")[-1]
                for line in file.read().split("\n")
            }

    def get(self, name: str):
        if name not in self._storage and name in default_settings:
            if self.is_first_time:
                return default_settings[name]
            self.set(name, default_settings[name])
        return self._storage[name]

    def set(self, name: str, value):
        self._storage[name] = str(value)
        with open(self.file_name, "w") as file:
            file.write(
                "\n".join(f"{key}:{item}" for key, item in self._storage.items())
            )


storage = Storage()
