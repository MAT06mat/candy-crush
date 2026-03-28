# Tests

Pour les tests, nous avons utilisé la librairie built-in [unittest](https://docs.python.org/fr/3/library/unittest.html) qui permet de lancer les tests à notre place sans devoir appeler une à une les fonctions. Celle-ci se trouvent dans `tests/tests.py`. Voici un exemple d'utilisation de `unittest`:

```py
from unittest import TestCase, main
from exemple import ajouter


# Définition de la classe pour faire des tests sur une fonction
class Ajouter(TestCase):
    # Définition du cas numéro 1 : ajouter 1
    def test_premier_cas_sur_cette_fonction(self):
        a = 1
        b = ajouter(a, 1)
        self.assertEqual(a + 1, b) # S'assure que (a + 1) == b sinon, fait une erreur
    
    def test_cas_2(self):
        ...

    def test_cas_2(self):
        ...


# Lance tous les tests se trouvant dans les fonctions des classes au dessus de cette ligne
# Créé également automatiquement des erreurs si les tests ne sont pas bon
main()
```

Les fonctions se trouvents dans `fonctions.py` et les tests dans `test/test.py`

> Info : Nous avons fait des listes 2D de string plutôt que d'entiers, car il y a aussi une gestion des bonus. Nous avons donc choisi d'identifier un bonbon par sa couleur et son bonus avec un caractère chacun, ce qui fait qu'il faut une string de 2 de long. L'utilisation de ces chaînes de caractères est plus détaillé dans le [README.md](https://github.com/MAT06mat/candy-crush/blob/main/README.md) du projet github.
