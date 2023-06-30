import pygame

import constants
import player
import sprite


class Level:
    def __init__(self, surface, level_map):
        self.surface = surface

        # Level sprites init
        self.sprites = pygame.sprite.Group()

        # Player init
        self.player = player.Player(pos=(0, 0), size_x=8, size_y=16, color=(225, 225, 225))
        self.player_sprite = pygame.sprite.GroupSingle()

        # Map init
        self.level_map_init(level_map)

    def level_map_init(self, level_map):
        for row_index, row in enumerate(level_map):
            for column_index, column in enumerate(row):
                x = column_index * 8
                y = row_index * 8 + 161

                if column == '1':
                    self.sprites.add(sprite.Sprite((x, y), 8, 8, (0, 0, 0)))
                elif column == 'P':
                    self.player.reset_position((x, y))
                    self.player_sprite.add(self.player)

    def level_scroll(self):
        for sprite_ in self.sprites:
            gap = constants.SURFACE_SIZE[0] / 4
            if self.player.rect.x < gap and self.player.direction.x < 0:
                self.player.speed = 0
                scroll_x = 1
            elif self.player.rect.x > constants.SURFACE_SIZE[0] - gap and self.player.direction.x > 0:
                self.player.speed = 0
                scroll_x = -1
            else:
                scroll_x = 0
                self.player.speed = 1

            sprite_.shift(scroll_x, 0)

    def update(self):
        # Level sprites render
        self.sprites.draw(self.surface)
        self.level_scroll()

        # Player handling and render
        self.player.update()
        self.player_sprite.draw(self.surface)
