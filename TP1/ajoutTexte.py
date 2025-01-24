from config import font, screen


# Fonction pour dessiner du texte
def draw_text(text, color, x, y, center=True):
    rendered_text = font.render(text, True, color)
    text_rect = rendered_text.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    screen.blit(rendered_text, text_rect)
