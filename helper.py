import pygame
pygame.init()
pygame.font.init()

GREEN = (0, 255, 0)

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font('jupiterc.ttf', size)
    text_surface = font.render(text, True, GREEN)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)