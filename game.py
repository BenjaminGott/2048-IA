import pygame
import random
import math
import game_value

pygame.init()

FPS = 1000

WIDTH, HEIGHT = 800, 800
ROWS = 4
COLS = 4

RECT_HEIGHT = HEIGHT // ROWS
RECT_WIDTH = WIDTH // COLS

score =0

OUTLINE_COLOR = (187, 173, 160)
OUTLINE_THICKNESS = 10
BACKROUND_COLOR = (205, 192, 180)
FONT_COLOR = (199, 110, 101)

FONT = pygame.font.SysFont("comicsans", 60, bold=True)
SCORE_FONT = pygame.font.SysFont("comicsans", 40, bold=True)
MOVE_VEL = 20

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")


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

    def get_color(self):
        color_index = int(math.log2(self.value)) - 1
        color = self.COLORS[color_index]
        return color

    def draw(self, window):
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
        if ceil:
            self.row = math.ceil(self.y / RECT_HEIGHT)
            self.col = math.ceil(self.x / RECT_WIDTH)
        else:
            self.row = math.floor(self.y / RECT_HEIGHT)
            self.col = math.floor(self.x / RECT_WIDTH)

    def move(self, delta):
        self.x += delta[0]
        self.y += delta[1]


def draw_grid(window):
    for row in range(1, ROWS):
        y = row * RECT_HEIGHT
        pygame.draw.line(window, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)

    for col in range(1, COLS):
        x = col * RECT_WIDTH
        pygame.draw.line(window, OUTLINE_COLOR, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS)

    pygame.draw.rect(window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)


def draw(window, tiles):
    window.fill(BACKROUND_COLOR)

    # Affichage des tuiles
    for tile in tiles.values():
        tile.draw(window)

    draw_grid(window)

    # Affichage du score par-dessus les autres éléments
    score_text = SCORE_FONT.render(f"Score: {game_value.score}", 1, (0,0,0))
    window.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

    pygame.display.update()


def get_random_pos(tiles):
    row = None
    col = None
    while True:
        row = random.randrange(0, ROWS)
        col = random.randrange(0, COLS)

        if f"{row}{col}" not in tiles:
            break

    return row, col


def move_tiles(window, tiles, clock, direction):
    updated = True
    blocks = set()
    
    if direction == "left":
        sort_func = lambda x: x.col
        reverse = False
        delta = (-MOVE_VEL, 0)
        boundary_check = lambda tile: tile.col == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col-1}")
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.x > next_tile.x + RECT_WIDTH + MOVE_VEL
        )
        ceil = True
    elif direction == "right":
        sort_func = lambda x: x.col
        reverse = True
        delta = (MOVE_VEL, 0)
        boundary_check = lambda tile: tile.col == COLS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col+1}")
        merge_check = lambda tile, next_tile: tile.x < next_tile.x - MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.x + RECT_WIDTH + MOVE_VEL < next_tile.x
        )
        ceil = False
    elif direction == "up":
        sort_func = lambda x: x.row
        reverse = False
        delta = (0, -MOVE_VEL)
        boundary_check = lambda tile: tile.row == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row-1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y > next_tile.y + MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.y > next_tile.y + RECT_WIDTH + MOVE_VEL
        )
        ceil = True
    elif direction == "down":
        sort_func = lambda x: x.row
        reverse = True
        delta = (0, MOVE_VEL)
        boundary_check = lambda tile: tile.row == ROWS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row+1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y < next_tile.y - MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.y + RECT_WIDTH + MOVE_VEL < next_tile.y
        )
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
            elif (
                tile.value == next_tile.value
                and tile not in blocks
                and next_tile not in blocks
            ):
                if merge_check(tile, next_tile):
                    tile.move(delta)
                else:
                    game_value.score += next_tile.value
                    next_tile.value *= 2
                    sorted_tiles.pop(i)
                    blocks.add(next_tile)
            elif move_check(tile, next_tile):
                tile.move(delta)
            else:
                continue
            tile.set_pos(ceil)
            updated = True
        
        update_tiles(window, tiles, sorted_tiles)
        
    reponse = end_move(tiles)
    if reponse == "lost":
        return "lost"

    return "continue"


def end_move(tiles):
    
    if len(tiles) == 16:
        # Vérifie si des mouvements sont encore possibles
        for tile in tiles.values():
            for delta_row, delta_col in [(0, 1), (1, 0)]:
                neighbor = tiles.get(f"{tile.row + delta_row}{tile.col + delta_col}")
                if neighbor and neighbor.value == tile.value:
                    return "continue"
          
        return "lost"  # Aucun mouvement possible, le jeu est perdu

    # Ajout d'une nouvelle tuile si le plateau n'est pas plein
    row, col = get_random_pos(tiles)
    tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)
    return "continue"


def update_tiles(window, tiles, sorted_tiles):
    # Remplir les tiles mises à jour sans réinitialiser complètement
    
        
    updated_tiles = {}
    for tile in sorted_tiles:
        updated_tiles[f"{tile.row}{tile.col}"] = tile

    tiles.clear()
    tiles.update(updated_tiles)

    # Conserver le score et redessiner
    draw(window, tiles)



def generate_titles():
    tiles = {}
    for _ in range(2):
        row, col = get_random_pos(tiles)
        tiles[f"{row}{col}"] = Tile(2, row, col)

    return tiles


def game(window):
    reponse = ""
    
    clock = pygame.time.Clock()
    run = True

    tiles = generate_titles()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                return "lost", 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    reponse = move_tiles(window, tiles, clock, "left")
                if event.key == pygame.K_RIGHT:
                    reponse = move_tiles(window, tiles, clock, "right")
                if event.key == pygame.K_UP:
                    reponse = move_tiles(window, tiles, clock, "up")
                if event.key == pygame.K_DOWN:
                    reponse = move_tiles(window, tiles, clock, "down")
                if reponse == "lost":
                    
                    return "lost" 
        draw(window, tiles)
    pygame.quit()


def start_game():
    return game(WINDOW)


