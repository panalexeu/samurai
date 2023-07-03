import pygame

import constants
import player
import sprite


class Level:
    def __init__(self, surface, level_map, level_gravity):
        self.surface = surface

        # Level sprites init
        self.level_sprites = pygame.sprite.Group()

        # Player init
        self.player = player.Player(pos=(0, 0), size_x=8, size_y=16, color=(225, 225, 225))
        self.player_sprite = pygame.sprite.GroupSingle()

        # Map init
        self.level_map_init(level_map)
        self.level_gravity = level_gravity

    def level_map_init(self, level_map):
        for row_index, row in enumerate(level_map):
            for column_index, column in enumerate(row):
                x = column_index * 8
                y = row_index * 8 + 161

                if column == '1':
                    self.level_sprites.add(sprite.Sprite((x, y), 8, 8, (0, 0, 0)))  # had some problems with that line
                elif column == 'P':
                    self.player.reset_position((x, y))
                    self.player_sprite.add(self.player)  # had some problems with that line

    def level_scroll(self):
        for sprite_ in self.level_sprites:
            indent = constants.SURFACE_SIZE[0] / 4
            if self.player.rect.x < indent and self.player.direction.x < 0:
                self.player.speed = 0
                scroll_x = 1
            elif self.player.rect.x > constants.SURFACE_SIZE[0] - indent and self.player.direction.x > 0:
                self.player.speed = 0
                scroll_x = -1
            else:
                scroll_x = 0
                self.player.speed = 1

            sprite_.shift(scroll_x, 0)

    def player_collisions(self):
        for sprite_ in self.level_sprites:
            if sprite_.rect.colliderect(self.player.rect):
                # Handling vertical collisions
                if self.player.direction.y < 0 and self.player.rect.y > sprite_.rect.y:
                    self.player.rect.top = sprite_.rect.bottom
                elif self.player.direction.y == 0 and self.player.rect.y < sprite_.rect.y:
                    self.player.rect.bottom = sprite_.rect.top

    def horizontal_collisions(self):
        for sprite_ in self.level_sprites:
            if sprite_.rect.colliderect(self.player.rect):
                # Handling horizontal collisions
                if self.player.direction.x > 0 and self.player.rect.y + 8 >= sprite_.rect.y:
                    self.player.rect.right = sprite_.rect.left
                elif self.player.direction.x < 0 and self.player.rect.y + 8 >= sprite_.rect.y:
                    self.player.rect.left = sprite_.rect.right

    def update(self):
        # Level sprites render
        self.level_sprites.draw(self.surface)
        self.level_scroll()

        # Player handling and render
        self.player.update()
        self.player.apply_player_gravity(self.level_gravity)
        self.horizontal_collisions()
        self.player_collisions()
        self.player_sprite.draw(self.surface)
