import pygame
import gameForHumain
import genetiques.geneticgameIA 
import montecarlo.gameIAMontecarlo

# Initialisation de Pygame

pygame.init()

# Paramètres de la fenêtre
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048-IA")

# Couleurs
WHITE = (255, 255, 255)
BLUE = (0, 122, 204)
RED = (204, 0, 0)
GREEN = (0, 204, 0)
BLACK = (0, 0, 0)

# Police pour les boutons
font = pygame.font.Font(None, 36)

title_font = pygame.font.Font(None, 72)  # Grande police pour le titre
button_font = pygame.font.Font(None, 36)  # Police des boutons

# Création des boutons (position et dimensions)
button_width, button_height = 200, 50
button1_rect = pygame.Rect((WIDTH - button_width) // 2, 300, button_width, button_height)
button2_rect = pygame.Rect((WIDTH - button_width) // 2, 400, button_width, button_height)
button3_rect = pygame.Rect((WIDTH - button_width) // 2, 500, button_width, button_height)

# Fonction pour dessiner un bouton
def draw_button(screen, rect, color, text):
    pygame.draw.rect(screen, color, rect)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

# Boucle principale
running = True
while running:
    screen.fill(WHITE)

    # Dessiner les boutons
    draw_button(screen, button1_rect, BLUE, "Jouer au jeu")
    draw_button(screen, button2_rect, RED, "IA Montecarlo")
    draw_button(screen, button3_rect, GREEN, "IA Générique")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                if button1_rect.collidepoint(event.pos):
                    currentGame = gameForHumain.Game_value()
                    state = gameForHumain.start_game(currentGame)
                    print(f"Score : {currentGame.score}")
                elif button2_rect.collidepoint(event.pos):
                    n = montecarlo.gameIAMontecarlo.Game_value()
                    state = montecarlo.gameIAMontecarlo.start_game(n)
                elif button3_rect.collidepoint(event.pos):
                    n = genetiques.geneticgameIA.Game_value()
                    state = genetiques.geneticgameIA.start_game(n)

    
    pygame.display.flip()

# Quitter Pygame
pygame.quit()