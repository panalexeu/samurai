import pygame


class Text:

    def __init__(self, font, size, color, pos, surface):
        self.font = font
        self.size = size
        self.color = color
        self.pos = pos
        self.surface = surface

    def display_text(self, text):
        text_surface = pygame.font.Font(f'game_core/fonts/{self.font}.ttf', self.size).render(text, True, self.color)
        text_rect = text_surface.get_rect(topleft=self.pos)
        self.surface.blit(text_surface, text_rect)
