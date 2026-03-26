# Candy Crush

> Projet ISN S2
>
> Groupe :
>
> - Matthieu
> - Théo
> - Arthur

## Difficultée implémentée

La difficultée implémentée est le niveau 1, cependant, nous avons ajoutés des bonus pour les bonbons :

Les bonbons rayés (h/v):

![image](assets/candies/red-h.png)
![image](assets/candies/red-v.png)

Les bonbons explosifs (p) :

![image](assets/candies/red-p.png)

Et le bonbon arc-en-ciel (r) :

![image](assets/candies/rainbow.png)

Pour la grille, nous avons choisi de la représenter par une liste 2D de strings. Chacun des éléments de cette liste 2D est sur 2 caractères. La convention pour la grille est la suivante :

- Le premier caractère donne la couleur, "\_" si case vide ou "r" si bonbon arc-en-ciel

- Le deuxième caractère donne le bonnus, "\_" si aucun

- Les bonus sons : v - vertical / h - horizontal / p - explosif

Exemple :

- "0\_" le bonbon est normal de la première couleur

- "2v" le bonbon à un bonus vertical et est de la troisième couleur

- "r\_" c'est un bonbon arc-en-ciel, par convention on met sa couleur à "r" et on ne lui met pas de bonus

- "\_\_" est une case vide

## Algorithme en pseudo code

L'algorithme suivant sera ensuite placé dans la fonction `candy_crush`.

```txt
Charger la grille depuis le fichier csv
Afficher la grille
Tant que le jeu n'est pas bloqué et que l'utilisateur n'a pas atteint le nombre max d'iter :
    Demander à l'utilisateur un mouvement
    Jouer le coup
    Enlever 1 aux coups restants
    Tant que la grille n'est pas stable :
        Calculer la nouvelle grille
        Afficher la grille
```

Décomposition du calcul de la nouvelle grille :

```txt
Créer une nouvelle grille (duplication de la première)
Supprimer tous les bonbons qui forment une ligne de 3 par rapport à la première grille
Si bonbons supprimés :
    Appliquer la gravité et descendre tous les bonbons volants
    Remplir les emplacements vides par de nouveux bonbons aléatoires
```

## Découpage fonctionnel (liste des fonctions)

| Fonction                   | Chargé de la réalisation | Terminé |
| -------------------------- | ------------------------ | ------- |
| charger_fichier            | Tout le monde            | Oui     |
| jeu_est_bloque             | Matthieu                 | Oui     |
| afficher_grille            | Arthur                   | Oui     |
| demander_mouvement         | Théo                     | Oui     |
| echanger_deux_bonbons      | Matthieu                 | Oui     |
| grille_est_stable          | Théo                     | Oui     |
| calculer_nouvelle_grille   | Arthur                   | Oui     |
| dupliquer_grille           | Théo                     | Oui     |
| supprimer_bonbons_en_ligne | Matthieu                 | Oui     |
| appliquer_gravite          | Théo                     | Oui     |
| ajouter_bonbons_aleatoires | Arthur                   | Oui     |

Les sous-tâches sont dans le fichier `fonctions.py`.

## Les différents programmes

En executant `terminal.py` vous pourrez voir le jeu dans le terminal, sans interface graphique. Avec `app.py`, le jeu se lancera avec une interface graphique à condition que tous les fichiers soient bien présents dans le dossier racine. En lançant `tests.py`, vous pourrez observer les tests sur les fonctions du fichier `fonctions.py`.

## Calcule de complexité de la fonction supprimer_bonbons_en_ligne

Ligne 323-324 : On a dans une boucle conditionnelle une boucle for dans une autre. Complexité de la fonction : o(n) = n^2

Ligne 340-341 : On observe une première boucle for dans une autre boucle for.

Dans cette boucle for, Nous avons un ensemble de conditionel, qui renferme de nouvelles boucles for aux lignes : 369; 377; 385; 397; 405; 410. Comme chacune de ces boucles for sont situés dans des conditionnels dépendantes les unes des autres, On effectuera qu'une seule de ces boucles quand la fonction sera effectué. Complexité de la fonction : o(n) = n^3 + n^2

Ligne 416-418-423 : On a rexpectivement une boucle while-for-for. Complexité de la fonction : o(n) = 2n^3 + n^2

Ligne 433-438 : On a deux boucles for simples : Complexité de la fonction : o(n) = 2n^3 + n^2 + 2n

Ligne 460-461 : On a une boucle for dans une autre. Complexité de la fonction : o(n) = 2n^3 + 2n^2 + 2n

On a donc finalement une complexité de la fonction de 2n^3 car 2n^2 + 2n est négligeable devant 2n^3.
