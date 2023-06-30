import pygame


class Sprite(pygame.sprite.Sprite):
    def __init__(
            self,
            pos,
            size_x,
            size_y,
            color
    ):
        super().__init__()
        self.image = pygame.Surface((size_x, size_y))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)

    def reset_position(self, pos):
        self.rect = self.image.get_rect(topleft=pos)

    def shift(self, shift_x, shift_y):
        self.rect.x += shift_x
        self.rect.y += shift_y
