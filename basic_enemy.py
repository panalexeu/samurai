import random

import pygame

import sprite


class BasicEnemy(sprite.AnimatedSprite):
    def __init__(self, pos, direction, speed, image_path, anim_path, anim_states, anim_speed):
        super().__init__(pos, image_path, anim_path, anim_states, anim_speed)

        # Souls amount
        self.souls = 10

        # Directions
        self.direction = direction

        # Stats
        self.speed = speed

    def movement(self):
        self.state = 'run'
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

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

        if self.direction.y == -1:
            self.image = image
        elif self.direction.y == 1:
            self.image = pygame.transform.flip(image, flip_x=False, flip_y=True)

    def update(self):
        self.movement()
        self.animate()


class Yokai(BasicEnemy):
    def __init__(self, pos):
        super().__init__(
            pos=pos,
            direction=pygame.math.Vector2(random.choice((-1, 1)), 0),
            speed=1,
            image_path='game_core/sprites/enemies/yokai/idle/yokai_idle.png',
            anim_path='game_core/sprites/enemies/yokai',
            anim_states={'idle': [], 'run': []},
            anim_speed=0.1
        )


class Spider(BasicEnemy):
    def __init__(self, pos):
        super().__init__(
            pos=pos,
            direction=pygame.math.Vector2(0, random.choice((-1, 1))),
            speed=1,
            image_path='game_core/sprites/enemies/spider/idle/spider_idle.png',
            anim_path='game_core/sprites/enemies/spider',
            anim_states={'idle': [], 'run': []},
            anim_speed=0.1
        )
