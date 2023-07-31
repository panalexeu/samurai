import random

import pygame

import projectile
import sprite


class Enemy(sprite.AnimatedSprite):
    def __init__(self, pos, direction, speed, image_path, anim_path, anim_states, anim_speed):
        super().__init__(pos, image_path, anim_path, anim_states, anim_speed)

        # Directions
        self.direction = direction

        # Stats
        self.speed = speed
        self.souls = 5

    def movement(self):
        self.state = 'run'
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

    def get_image(self):
        return self.animations[self.state][int(self.frame_index)]

    def animate(self):
        animation = self.animations[self.state]

        self.frame_index += self.anim_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

    def update(self):
        self.movement()
        self.animate()


class ShootingSkeleton(Enemy):
    def __init__(self, pos, level_projectiles: pygame.sprite.Group, rotation=True):
        super().__init__(
            pos=pos,
            direction=pygame.math.Vector2(0, 0),
            speed=1,
            image_path='game_core/sprites/enemies/shooting_skeleton/idle/shooting_skeleton.png',
            anim_path='game_core/sprites/enemies/shooting_skeleton',
            anim_states={'idle': [], 'run': []},
            anim_speed=0.1
        )

        self.souls = 15

        self.pos = pos
        self.level_projectiles = level_projectiles
        self.rotation = rotation

        if self.rotation:
            self.proj_pos = (pos[0] + 8, pos[1] - 1)
            self.proj_direction = pygame.math.Vector2(1, 0)
        else:
            self.proj_pos = (pos[0], pos[1] - 1)
            self.proj_direction = pygame.math.Vector2(-1, 0)

        self.shooting_state = False
        self.CONST_SHOOTING_TICK = 50
        self.shooting_tick = self.CONST_SHOOTING_TICK

    def animate(self):
        super().animate()
        image = self.get_image()
        if self.rotation:
            self.image = pygame.transform.flip(image, flip_x=True, flip_y=False)
        else:
            self.image = image

    # noinspection PyTypeChecker
    def shoot(self):
        if not self.shooting_state:
            # Playing a sound
            pygame.mixer.Sound('game_core/sounds/shoot.wav').play()

            # Spawning a projectile
            self.level_projectiles.add(
                projectile.Projectile(
                    pos=self.proj_pos,
                    image_path='game_core/sprites/projectiles/skeleton_projectile/skeleton_projectile.png',
                    speed=1,
                    direction=self.proj_direction
                )
            )

            self.shooting_state = True

        if self.shooting_state:
            self.shooting_tick -= 1
            if self.shooting_tick == 0:
                self.shooting_tick = self.CONST_SHOOTING_TICK
                self.shooting_state = False

    def update(self):
        super().update()
        self.shoot()


class Yokai(Enemy):
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

        self.souls = 10

    def animate(self):
        super().animate()
        image = self.get_image()

        if self.direction.x == 1:
            self.image = image
        else:
            self.image = pygame.transform.flip(image, flip_x=True, flip_y=False)


class Spider(Enemy):
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

    def animate(self):
        super().animate()
        image = self.get_image()

        if self.direction.y == -1:
            self.image = image
        elif self.direction.y == 1:
            self.image = pygame.transform.flip(image, flip_x=False, flip_y=True)
