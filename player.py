import pygame

import sprite


class Player(sprite.Sprite):
    def __init__(self, pos, size_x, size_y, color):
        super().__init__(pos, size_x, size_y, color)

        self.speed = 1

        self.direction = pygame.math.Vector2(0, 0)  # vector used for movement handling

    def reset_position(self, pos):
        self.rect = self.image.get_rect(center=pos)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x, self.direction.y = 0, 0

    def update(self):
        self.get_input()

        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
