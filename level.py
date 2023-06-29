import pygame

import sprite


class Level:
    def __init__(self, surface, level_map):
        self.surface = surface
        self.sprites = pygame.sprite.Group()

        for row_index, row in enumerate(level_map):
            for column_index, column in enumerate(row):
                x = column_index * 8
                y = row_index * 8 + 161
                if column == '1':
                    self.sprites.add(sprite.Sprite((x, y), 8))

    def render(self):
        self.sprites.draw(self.surface)
