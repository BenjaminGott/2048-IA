from copy import deepcopy
import random
import game
import pygame

directions = ["left", "right", "up", "down"]
nbGame = 50  # Nombre de simulations par direction

def montecarlo(current_game):
    max_score = 0
    best_direction = None
    original_tiles = deepcopy(current_game.tabOfInfo)

    for direction in directions:
        total_score = 0

        for _ in range(nbGame):
            # Préparer la simulation
            simulated_game = game.Game_value()
            simulated_game.tabOfInfo = deepcopy(original_tiles)
            simulated_game.score = current_game.score

            # Convertir tabOfInfo en dictionnaire de tuiles
            simulated_tiles = {
                f"{tile[1]}{tile[2]}": game.Tile(tile[0], tile[1], tile[2])
                for tile in simulated_game.tabOfInfo
            }

            # Simuler le premier mouvement
            response, score = game.move_tiles(None, simulated_tiles, pygame.time.Clock(), direction, simulated_game)

            # Simuler les mouvements aléatoires jusqu'à la fin de la partie
            while response != "lost":
                random_direction = random.choice(directions)
                response, score = game.move_tiles(None, simulated_tiles, pygame.time.Clock(), random_direction, simulated_game)

            total_score += simulated_game.score

        # Calculer le score moyen pour cette direction
        average_score = total_score / nbGame

        # Mettre à jour la meilleure direction si nécessaire
        if average_score > max_score:
            max_score = average_score
            best_direction = direction

    return best_direction
