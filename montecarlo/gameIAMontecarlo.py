import pygame
import random
import math
from montecarlo.montecarlo import montecarlo
from genetiques.model import generate_population, generate_random_individual
from genetiques.sauvegarde import load_pop, save_pop


pygame.init()

FPS = 2000

WIDTH, HEIGHT = 800, 800
ROWS = 4
COLS = 4

RECT_HEIGHT = HEIGHT // ROWS
RECT_WIDTH = WIDTH // COLS

score = 0

OUTLINE_COLOR = (187, 173, 160)
OUTLINE_THICKNESS = 10
BACKROUND_COLOR = (205, 192, 180)
FONT_COLOR = (199, 110, 101)

FONT = pygame.font.SysFont("comicsans", 60, bold=True)
SCORE_FONT = pygame.font.SysFont("comicsans", 40, bold=True)
MOVE_VEL = 20

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")

class Game_value : 
    def __init__(self):
        self.score = 0
        self.tabOfInfo = []
        # [(value,row,col),(value,row,col)]

class Tile:
    COLORS = [
        (237, 229, 218),
        (238, 225, 201),
        (243, 178, 122),
        (246, 150, 101),
        (247, 124, 95),
        (247, 95, 59),
        (237, 208, 115),
        (237, 204, 99),
        (236, 202, 80),
    ]


    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.x = col * RECT_WIDTH
        self.y = row * RECT_HEIGHT
        
    def get_info(self) :
        return self.value,self.row,self.col
    
    
    def get_color(self):
        """
        Returns:
        tuple: The RGB color of the tile based on its value.
        """
        color_index = int(math.log2(self.value)) - 1
        color = self.COLORS[color_index]
        return color

    def draw(self, window):
        """
        Draws the tile on the game window with its value and color.

        Args:
            window (pygame.Surface): The game window where the tile is drawn.
        """
        color = self.get_color()
        pygame.draw.rect(window, color, (self.x, self.y, RECT_WIDTH, RECT_HEIGHT))

        text = FONT.render(str(self.value), 1, FONT_COLOR)
        window.blit(
            text,
            (
                self.x + (RECT_WIDTH / 2 - text.get_width() / 2),
                self.y + (RECT_HEIGHT / 2 - text.get_height() / 2),
            ),
        )

    def set_pos(self, ceil=False):
        """
        Updates the tile's row and column position based on its current x and y coordinates.

        Args:
            ceil (bool): If True, uses the ceiling function; otherwise, uses the floor function.
        """
        if ceil:
            self.row = math.ceil(self.y / RECT_HEIGHT)
            self.col = math.ceil(self.x / RECT_WIDTH)
        else:
            self.row = math.floor(self.y / RECT_HEIGHT)
            self.col = math.floor(self.x / RECT_WIDTH)

    def move(self, delta):
        """
        Moves the tile by a given delta in x and y directions.

        Args:
            delta (tuple): A tuple of two integers representing the change in x and y positions.
        """
        self.x += delta[0]
        self.y += delta[1]


def draw_grid(window):
    """
    Draws the grid lines and border of the game window.

    Args:
        window (pygame.Surface): The game window where the grid is drawn.
    """
    for row in range(1, ROWS):
        y = row * RECT_HEIGHT
        pygame.draw.line(window, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)

    for col in range(1, COLS):
        x = col * RECT_WIDTH
        pygame.draw.line(window, OUTLINE_COLOR, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS)

    pygame.draw.rect(window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)


def draw(window, tiles, game_value):
    """
    Draws the entire game, including the background, grid, tiles, and score.

    Args:
        window (pygame.Surface): The game window.
        tiles (dict): A dictionary of all tiles on the board.
    """
    window.fill(BACKROUND_COLOR)

    # Affichage des tuiles
    for tile in tiles.values():
        tile.draw(window)

    draw_grid(window)

    # Affichage du score par-dessus les autres éléments
    score_text = SCORE_FONT.render(f"Score: {game_value.score}", 1, (0, 0, 0))
    window.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

    pygame.display.update()


def get_random_pos(tiles):
    """
    Generates a random position on the board that is not already occupied.

    Args:
        tiles (dict): A dictionary of all tiles on the board.

    Returns:
        tuple: A tuple (row, col) representing the random position.
    """
    row = None
    col = None
    while True:
        row = random.randrange(0, ROWS)
        col = random.randrange(0, COLS)

        if f"{row}{col}" not in tiles:
            break

    return row, col


def move_tiles(window, tiles, clock, direction, game_value):
    """
    Handles the movement and merging of tiles in the specified direction.

    Args:
        window (pygame.Surface): The game window.
        tiles (dict): A dictionary of all tiles on the board.
        clock (pygame.time.Clock): The game clock to control the frame rate.
        direction (str): The direction of movement ("left", "right", "up", "down").
        game_value (Game_value): The object containing game-related information.

    Returns:
        str: "continue" if the game continues, or "lost" if the game is over.
    """
    updated = True
    blocks = set()

    # Détermine les paramètres en fonction de la direction
    if direction == "left":
        sort_func = lambda x: x.col
        reverse = False
        delta = (-MOVE_VEL, 0)
        boundary_check = lambda tile: tile.col == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col-1}")
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + MOVE_VEL
        move_check = lambda tile, next_tile: tile.x > next_tile.x + RECT_WIDTH + MOVE_VEL
        ceil = True
    elif direction == "right":
        sort_func = lambda x: x.col
        reverse = True
        delta = (MOVE_VEL, 0)
        boundary_check = lambda tile: tile.col == COLS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col+1}")
        merge_check = lambda tile, next_tile: tile.x < next_tile.x - MOVE_VEL
        move_check = lambda tile, next_tile: tile.x + RECT_WIDTH + MOVE_VEL < next_tile.x
        ceil = False
    elif direction == "up":
        sort_func = lambda x: x.row
        reverse = False
        delta = (0, -MOVE_VEL)
        boundary_check = lambda tile: tile.row == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row-1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y > next_tile.y + MOVE_VEL
        move_check = lambda tile, next_tile: tile.y > next_tile.y + RECT_WIDTH + MOVE_VEL
        ceil = True
    elif direction == "down":
        sort_func = lambda x: x.row
        reverse = True
        delta = (0, MOVE_VEL)
        boundary_check = lambda tile: tile.row == ROWS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row+1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y < next_tile.y - MOVE_VEL
        move_check = lambda tile, next_tile: tile.y + RECT_WIDTH + MOVE_VEL < next_tile.y
        ceil = False

    while updated:
        clock.tick(FPS)
        updated = False
        sorted_tiles = sorted(tiles.values(), key=sort_func, reverse=reverse)

        for i, tile in enumerate(sorted_tiles):
            if boundary_check(tile):
                continue

            next_tile = get_next_tile(tile)
            if not next_tile:
                tile.move(delta)
            elif tile.value == next_tile.value and tile not in blocks and next_tile not in blocks:
                if merge_check(tile, next_tile):
                    tile.move(delta)
                else:
                    game_value.score += next_tile.value
                    next_tile.value *= 2
                    if next_tile.value==2048 : 
                        return "lost"
                    sorted_tiles.pop(i)
                    blocks.add(next_tile)
            elif move_check(tile, next_tile):
                tile.move(delta)
            else:
                continue
            tile.set_pos(ceil)
            updated = True

        update_tiles(window, tiles, sorted_tiles, game_value)

    # Passe game_value pour inclure les nouvelles tuiles dans tabOfInfo
    reponse = end_move(tiles, game_value)
    if reponse == "lost":
        return "lost"

    return "continue"

def end_move(tiles, game_value):
    """
    Checks if the game should continue or end after a move and generates a new tile if possible.

    Args:
        tiles (dict): A dictionary of all tiles on the board.
        game_value (Game_value): The object containing game-related information.

    Returns:
        str: "continue" if the game continues, or "lost" if no moves are possible.
    """
    if len(tiles) == 16:  # Vérifie si la grille est pleine
        for tile in tiles.values():
            for delta_row, delta_col in [(0, 1), (1, 0)]:
                neighbor = tiles.get(f"{tile.row + delta_row}{tile.col + delta_col}")
                if neighbor and neighbor.value == tile.value:
                    return "continue"

        return "lost"

    # Génère une nouvelle tuile
    row, col = get_random_pos(tiles)
    tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)

    # Met à jour tabOfInfo immédiatement après la génération de la nouvelle tuile
    game_value.tabOfInfo = [tile.get_info() for tile in tiles.values()]
    return "continue"


def update_tiles(window, tiles, sorted_tiles,game_value):
    """
    Updates the tiles dictionary with the current positions and redraws the game.

    Args:
        window (pygame.Surface): The game window.
        tiles (dict): A dictionary of all tiles on the board.
        sorted_tiles (list): A list of tiles sorted for the current move.
    """

    updated_tiles = {}

    game_value.tabOfInfo = []  
    for tile in sorted_tiles:
        updated_tiles[f"{tile.row}{tile.col}"] = tile
        game_value.tabOfInfo.append(tile.get_info())

    tiles.clear()
    tiles.update(updated_tiles)

    draw(window, tiles,game_value)


def generate_titles():
    """
    Generates the initial tiles on the board at the start of the game.

    Returns:
        dict: A dictionary of the initial tiles.
    """
    tiles = {}
    for _ in range(2):
        row, col = get_random_pos(tiles)
        tiles[f"{row}{col}"] = Tile(2, row, col)

    return tiles


def game(window,game_value):
    """
    Runs the main game loop, handling user input and game logic.

    Args:
        The game window.

    Returns:
        tuple: A tuple containing the game state ("lost").
    """
    reponse = ""
    game_value.score = 0

    clock = pygame.time.Clock()
    run = True

    tiles = generate_titles()

    while run:
        clock.tick(FPS)
        direction = testmontecarlo(window, tiles, clock, game_value)
        reponse = move_tiles(window, tiles, clock, direction, game_value)
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         run = False
        #         return "lost", 0
        #     if event.type == pygame.KEYDOWN:
        #         # if event.key == pygame.K_LEFT:
        #         #     reponse = move_tiles(window, tiles, clock, "left",game_value)
        #         # if event.key == pygame.K_RIGHT:
        #         #     reponse = move_tiles(window, tiles, clock, "right",game_value)
        #         # if event.key == pygame.K_UP:
        #         #     reponse = move_tiles(window, tiles, clock, "up",game_value)
        #         # if event.key == pygame.K_DOWN:
        #         #     reponse = move_tiles(window, tiles, clock, "down",game_value)
        #         # if reponse == "lost":

        #         #     return "lost"
        draw(window, tiles, game_value)
        print(f"Score actuelle : {game_value.score}, direction choisie : {direction}")
    pygame.quit()
    
    
def play_individu(individu, game_value, window):
    '''L'IA fait bouger les blocs de façon aléatoire au début'''
    game_value.score = 0
    clock = pygame.time.Clock()
    tiles = generate_titles()
    i = 0  
    while i < len(individu):  # Continue jusqu'à ce que tous les mouvements soient joués
        move = individu[i]
        print(f"Move: {move}, Score: {game_value.score}")

        if move == "left":
            reponse = move_tiles(window, tiles, clock, "left", game_value)
        elif move == "right":
            reponse = move_tiles(window, tiles, clock, "right", game_value)
        elif move == "up":
            reponse = move_tiles(window, tiles, clock, "up", game_value)
        elif move == "down":
            reponse = move_tiles(window, tiles, clock, "down", game_value)

        draw(window, tiles, game_value)

        if reponse == "lost":
            print(f"Lost at move: {move}, Final Score: {game_value.score}")
            return game_value.score  # Retourner le score final si le jeu est perdu

        i += 1  

    return game_value.score  # Retourner le score final sauf si perdu


def eval_pop(population, game_value, window):
    scores = []
    for individu in population:
        score = play_individu(individu, game_value,window)
        scores.append(score)
    return scores


def selection(population, scores, num_parents):
    """meilleurs individus selon leurs scores."""
    sorted_population = [individu for _, individu in sorted(zip(scores, population), reverse=True)]
    return sorted_population[:num_parents]

def crossover(parents, population_size):
    """nouvelle génération en combinant deux parents."""
    new_population = []
    while len(new_population) < population_size:
        parent1 = random.choice(parents)
        parent2 = random.choice(parents)
        crossover_point = random.randint(0, len(parent1) - 1)
        child = parent1[:crossover_point] + parent2[crossover_point:]
        new_population.append(child)
    return new_population


def mutate(population, mutation_rate):
    """ Un truc en plus aléatoire"""
    for i in range(len(population)):
        if random.random() < mutation_rate:
            mutation_point = random.randint(0, len(population[i]) - 1)
            population[i][mutation_point] = random.choice(["up", "down", "left", "right"])
    return population


def algorithme_genetique(game_value, window, generations=50, population_size=100, mutation_rate=0.1, num_parents=10, resume_from_saved=True):
    """Algorithme génétique pour entraîner l'IA."""
    
    if resume_from_saved:
        population, starting_generation = load_pop("pop.json")
        if not population:
            population = generate_population(population_size)  
        generation = starting_generation
    else:
        population = generate_population(population_size)
        generation = 0

    for generation in range(generation, generations):
        print(f"=== Génération {generation + 1} ===")
        
        scores = eval_pop(population, game_value, window)
        print(f"Meilleur score de cette génération : {max(scores)}")
        
        # Sélection des meilleurs individus 
        parents = selection(population, scores, num_parents)
        
        # Croisement 
        population = crossover(parents, population_size)
        
        # mutation
        population = mutate(population, mutation_rate)

        # Sauvegarde de la population 
        save_pop(population, generation + 1)

    






def start_training():
    game_value = Game_value()
    algorithme_genetique(game_value, WINDOW)



def start_game(game_value):
    """
    Starts the game by initializing the game window and running the main loop.

    Returns:
        tuple: The result of the gadme function (e.g., game state and score).
    """

    return game(WINDOW,game_value)

def testmontecarlo(window, tiles, clock, game_value):
    """
    Utilise l'algorithme Monte Carlo pour déterminer la meilleure direction de mouvement.

    Args:
        window (pygame.Surface): Fenêtre du jeu (nécessaire pour certains appels de simulation).
        tiles (dict): Dictionnaire contenant les tuiles actuelles du plateau.
        clock (pygame.time.Clock): Horloge pour gérer le framerate.
        game_value (Game_value): État actuel du jeu.

    Returns:
        str: La meilleure direction ("left", "right", "up", "down").
    """
    directions = ["left", "right", "up", "down"]  # Actions possibles
    nb_simulations = 1  # Nombre de simulations par direction
    best_direction = None
    max_average_score = float('-inf')  # Initialise à une valeur très basse

    for direction in directions:
        total_score = 0
        simulations_valides = 0

        for _ in range(nb_simulations):
            # Copie indépendante des tuiles et de l'état du jeu
            simulated_tiles = {key: Tile(tile.value, tile.row, tile.col) for key, tile in tiles.items()}
            simulated_game = Game_value()
            simulated_game.tabOfInfo = [tile.get_info() for tile in simulated_tiles.values()]
            simulated_game.score = game_value.score
            
            # Applique le mouvement initial dans la direction donnée
            reponse = move_tiles(window, simulated_tiles, clock, direction, simulated_game)
            if reponse == "lost":
                continue  # Ignore les simulations où le premier mouvement est invalide

            # Continue avec des mouvements aléatoires jusqu'à la fin du jeu
            while reponse != "lost":
                random_direction = random.choice(directions)
                reponse = move_tiles(window, simulated_tiles, clock, random_direction, simulated_game)

            # Ajoute le score final de cette simulation
            total_score += simulated_game.score
            simulations_valides += 1

        # Calcule le score moyen pour cette direction
        if simulations_valides > 0:
            average_score = total_score / simulations_valides
        else:
            average_score = float('-inf')  # Mouvement initial impossible

        # Met à jour la meilleure direction si nécessaire
        if average_score > max_average_score:
            max_average_score = average_score
            best_direction = direction

    return best_direction

    choice = input("Jouer manuellement (1) ou Entraîner l'IA (2) ? ")

    if choice == "1":
        return game(WINDOW, game_value)  
    elif choice == "2":
        print("Lancement de l'entrainement")
        start_training()
        return None  
    else:
        print("Choix invalide.")
        return None

