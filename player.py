import pygame

import sprite


class Player(sprite.Sprite):
    def __init__(self, pos, size_x, size_y, color):
        super().__init__(pos, size_x, size_y, color)

        self.speed = 1
        self.jump_speed = 4

        self.direction = pygame.math.Vector2(0, 0)  # vector used for movement handling

    def reset_position(self, pos):
        self.rect = self.image.get_rect(topleft=pos)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE]:
            self.direction.y = -1
        else:
            self.direction.y = 0

        # handling input of the player movement
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.jump_speed

    def apply_player_gravity(self, gravity):
        self.rect.y += gravity

    def update(self):
        self.get_input()

