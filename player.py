import pygame

import sprite


class Player(sprite.Sprite):
    def __init__(self, pos, size_x, size_y, color):
        super().__init__(pos, size_x, size_y, color)

        # vectors
        self.direction = pygame.math.Vector2(0, 0)  # vector used for movement handling

        # speeds
        self.speed = 1
        self.player_gravity = 1
        self.jump_speed = 4

        # cooldowns
        self.jump_state = False
        self.jump_cooldown = 30

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE]:
            if not self.jump_state:
                self.direction.y = -1
                self.jump_state = True
        else:
            self.direction.y = 0

        # handling input of the player movement
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.jump_speed + self.player_gravity

    def cooldowns_handling(self):
        # Jumping handling
        if self.jump_state:
            self.jump_cooldown -= 1
            if self.jump_cooldown == 0:
                self.jump_state = False
                self.jump_cooldown = 30
            elif self.jump_cooldown == 15:
                self.direction.y = 0
    def apply_player_gravity(self, gravity):
        self.rect.y += gravity

    def update(self):
        self.get_input()
        self.cooldowns_handling()

