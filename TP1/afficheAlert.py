import pygame
from ajoutTexte import draw_text
from config import *

# Fonction d'affiche d'une alerte
def draw_alert_box():
    box_rect = pygame.Rect(100, 150, 300, 200)
    pygame.draw.rect(screen, GRAY, box_rect)
    pygame.draw.rect(screen, BLACK, box_rect, 2)
    draw_text("Vous pouvez faire un swap!", BLACK, SCREEN_WIDTH // 2, 200)

    #OK
    ok_button_rect = pygame.Rect(130, 270, 100, 40)
    pygame.draw.rect(screen, BLUE, ok_button_rect)
    draw_text("OK", WHITE, ok_button_rect.centerx, ok_button_rect.centery)

    #Fermer
    close_button_rect = pygame.Rect(270, 270, 100, 40)
    pygame.draw.rect(screen, RED, close_button_rect)
    draw_text("FERMER", WHITE, close_button_rect.centerx, close_button_rect.centery)

    return ok_button_rect, close_button_rect
