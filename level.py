import pygame

import constants
import debug_console
import player
import sprite


class Level:
    def __init__(self, surface, level_map):
        self.surface = surface

        # Level sprites init
        self.level_sprites = pygame.sprite.Group()

        # Player init
        self.player = player.Player(pos=(0, 0), image_path='game_core/sprites/player/idle/samurai_idle1.png')
        self.player_sprite = pygame.sprite.GroupSingle()

        # Map init
        self.level_map_init(level_map)

        # Console init
        self.level_console = debug_console.DebugConsole(self.surface, self.player, self.level_sprites)

    def level_map_init(self, level_map):
        for row_index, row in enumerate(level_map):
            for column_index, column in enumerate(row):
                x = column_index * 8
                y = row_index * 8

                if column == '1':
                    # noinspection PyTypeChecker
                    self.level_sprites.add(sprite.Sprite(pos=(x, y), size_x=8, size_y=8, image_path='game_core/sprites/level_1/brick.png'))  # had some problems with that line
                elif column == 'P':
                    self.player.reset_position((x, y))
                    # noinspection PyTypeChecker
                    self.player_sprite.add(self.player)  # had some problems with that line

    def level_scroll(self):
        for sprite_ in self.level_sprites:
            # x coordinate scrolling
            indent_x = constants.SURFACE_SIZE[0] / 4
            if self.player.rect.x < indent_x and self.player.direction.x < 0:
                self.player.player_speed = 0
                scroll_x = self.player.CONST_PLAYER_SPEED
            elif self.player.rect.x > constants.SURFACE_SIZE[0] - indent_x and self.player.direction.x > 0:
                self.player.player_speed = 0
                scroll_x = -self.player.CONST_PLAYER_SPEED
            else:
                scroll_x = 0
                self.player.player_speed = self.player.CONST_PLAYER_SPEED

            # y coordinate scrolling
            indent_y = constants.SURFACE_SIZE[1] / 3
            if self.player.rect.y < indent_y and self.player.direction.y < 0:
                self.player.jump_speed = 0
                self.player.player_gravity = 0
                scroll_y = self.player.CONST_JUMP_SPEED - self.player.CONST_PLAYER_GRAVITY
            elif self.player.rect.y > constants.SURFACE_SIZE[1] - indent_y and self.player.direction.y >= 0:
                self.player.jump_speed = 0
                self.player.player_gravity = 0
                scroll_y = -self.player.CONST_PLAYER_GRAVITY
            else:
                scroll_y = 0
                self.player.player_gravity = self.player.CONST_PLAYER_GRAVITY
                self.player.jump_speed = self.player.CONST_JUMP_SPEED

            # applying scrolling
            sprite_.shift(scroll_x, scroll_y)

    def player_vertical_collisions(self):
        for sprite_ in self.level_sprites:
            if sprite_.rect.colliderect(self.player.rect):
                if self.player.direction.y < 0 and self.player.rect.y > sprite_.rect.y:
                    self.player.rect.top = sprite_.rect.bottom

                    # Handling stun
                    self.player.stun_state = True
                    self.player.direction.y = 0
                    self.player.direction.x = 0

                elif self.player.direction.y == 0 and self.player.rect.y < sprite_.rect.y:
                    self.player.rect.bottom = sprite_.rect.top

    def player_horizontal_collisions(self):
        for sprite_ in self.level_sprites:
            if sprite_.rect.colliderect(self.player.rect):
                sprite_.image.fill('red')  # for debugging
                if self.player.direction.x > 0 and sprite_.rect.y in range(
                        self.player.rect.y - self.player.CONST_PLAYER_GRAVITY,
                        self.player.rect.y + self.player.rect.size[1] // 2
                ):
                    self.player.rect.right = sprite_.rect.left
                elif self.player.direction.x < 0 and sprite_.rect.y in range(
                        self.player.rect.y - self.player.CONST_PLAYER_GRAVITY,
                        self.player.rect.y + self.player.rect.size[1] // 2
                ):
                    self.player.rect.left = sprite_.rect.right

    def update(self):
        # Level sprites render
        self.level_sprites.draw(self.surface)
        self.level_scroll()

        # Player handling and render
        self.player.update()
        self.player_horizontal_collisions()
        self.player_vertical_collisions()
        self.player_sprite.draw(self.surface)

        # debug console
        self.level_console.update()
