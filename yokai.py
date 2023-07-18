import random

import pygame

import sprite


class Yokai(sprite.AnimatedSprite):
    def __init__(self, pos):
        super().__init__(
            pos=pos,
            image_path='game_core/sprites/enemies/yokai/idle/yokai_idle.png',
            anim_path='game_core/sprites/enemies/yokai',
            anim_states={'idle': [], 'run': []},
            anim_speed=0.1
        )

        # Yokai directions
        self.direction = pygame.math.Vector2(random.choice((-1, 1)), 0)

        # Yokai stats
        self.speed = 0.1
        self.jump_speed = 1
        self.gravity = 0

    def movement(self):
        self.state = 'run'
        print(self.direction.x)
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.jump_speed + self.gravity

    def animate(self):
        animation = self.animations[self.state]

        self.frame_index += self.anim_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.direction.x == 1:
            self.image = image
        else:
            self.image = pygame.transform.flip(image, flip_x=True, flip_y=False)

    def update(self):
        self.animate()
        self.movement()
