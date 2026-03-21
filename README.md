# Candy Crush

> Projet ISN S2
>
> Groupe :
>
> - Matthieu
> - Théo
> - Arthur

Pour le moment, nous allons partir sur le niveau 1, mais on va surement rajouter des petites améliorations dans le résultat final.

Convention pour la grille :

- Le premier caractère donne la couleur, "\_" si case vide ou "r" si bonbon arc-en-ciel

- Le deuxième caractère donne le bonnus, "\_" si aucun

- Les bonus sons : v - vertical / h - horizontal / p - explosif

Exemple :

- "0\_" le bonbon est normal de la première couleur

- "2v" le bonbon à un bonus vertical et est de la deuxème couleur

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

Sous-tâches dans le fichier `fonctions.py`
