# 2048-IA

2048-IA est une interface graphique créée avec Pygame et tenserflow permettant d'interagir avec une intelligence artificielle jouant au jeu 2048. 

## Installation

1. **Cloner le dépôt :**

   ```bash
   https://github.com/BenjaminGott/2048-IA.git
   cd 2048-IA
   ```

2. **Installer les dépendances :**

   ```bash
   pip install -r requirements.txt
   ou 
   pip install pygame 
   pip install tenserflow
   ```
   Assurez-vous que le fichier `requirements.txt` contient les modules nécessaires.

3. **Exécuter le programme :**

   ```bash
   python main.py
   ```

## Fonctionnalités des boutons

1. **Jouer au jeu :**
   - Permet de jouer au jeu normalement avec les quatre flèches du clavier.

2. **IA Montecarlo :**
    - Permet de voir L'IA jouer
   - Fonctionement de l'IA : L'algorithme de Monte Carlo simule de nombreux scénarios aléatoires pour estimer une solution à un problème complexe. En prenant la moyenne des résultats des simulations, il détermine la meilleure action ou une approximation de la solution.

3. **IA Générique :**
    - Permet de voir L'IA jouer
   - Fonctionement de l'IA : L'algorithmes génétiques  crée des individu qui  au début ont une séquence aléatoire pour faire une population,ceux qui ont le meilleur scores sont  gardées ,le reste sont supprimé. Suite a cela on regroupe  deux individu pour crée des parents puis j on fait une mutation qui  modifie aléaoirement certaines parties des séquences   ..



## Contribution

    @BenjaminGott
    @Yukojuni
    @lamynoah

