import pygame


class Sprite(pygame.sprite.Sprite):
    def __init__(
            self,
            pos,
            size_x=None,
            size_y=None,
            color=None,
            image_path=None
    ):
        super().__init__()

        if color and size_x and size_y:
            self.image = pygame.Surface((size_x, size_y))
            self.image.fill(color)
        else:
            self.image = pygame.image.load(image_path)

        self.rect = self.image.get_rect(bottomleft=pos)

    def reset_position(self, pos):
        self.rect.bottomleft = pos

    def shift(self, shift_x, shift_y):
        self.rect.x += shift_x
        self.rect.y += shift_y

