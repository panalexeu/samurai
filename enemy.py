import random

import pygame

import player
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


class DeadSamuraiBoss(Enemy):
    def __init__(self, pos, player_obj: player.Player, level_projectiles: pygame.sprite.Group):
        super().__init__(
            pos=pos,
            direction=pygame.math.Vector2(0, 0),
            speed=1,
            image_path='game_core/sprites/enemies/dead_samurai_boss/idle/dead_samurai_boss_idle.png',
            anim_path='game_core/sprites/enemies/dead_samurai_boss',
            anim_states={'idle': [], 'run': [], 'stun': [], 'charge': []},
            anim_speed=0.1
        )

        self.player = player_obj
        self.level_projectiles = level_projectiles

        self.souls = 200

        self.HP_CONST = 6
        self.hp = self.HP_CONST

        self.CONST_SPEED = 1
        self.speed = self.CONST_SPEED

        self.second_stage = False

        self.hit_state = False
        self.CONST_HIT_TICK = 30
        self.hit_tick = self.CONST_HIT_TICK

        self.stun_state = False
        self.CONST_STUN_TICK = 100
        self.stun_tick = self.CONST_STUN_TICK

        self.charge_state = False
        self.CONST_CHARGE_TICK = 50
        self.charge_tick = self.CONST_CHARGE_TICK

        self.check_state = False

        self.shooting_state = False
        self.CONST_SHOOTING_TICK = 50
        self.shooting_tick = self.CONST_SHOOTING_TICK

    def attacks_check(self):
        if self.player.rect.y >= self.rect.y:
            if not self.charge_state and not self.stun_state:
                self.charge_state = True
                self.check_state = False

        if self.player.potion_state:
            self.check_state = True

    def stage_check(self):
        if self.hp <= 3:
            self.second_stage = True

    def check_player_pos(self):
        if self.player.rect.x < self.rect.x:
            self.direction.x = -1
        else:
            self.direction.x = 1

    def anim_states_update(self):
        if self.speed > 0:
            if self.second_stage:
                self.state = 'run'
            else:
                self.state = 'charge'
        else:
            self.state = 'stun'

    def states_update(self):
        if self.hit_state:
            self.hit_tick -= 1
            if self.hit_tick == 0:
                self.hit_state = False
                self.hit_tick = self.CONST_HIT_TICK

        if self.charge_state:
            self.charge_tick -= 1
            if self.charge_tick == 0:
                self.charge_state = False
                self.charge_tick = self.CONST_CHARGE_TICK
                self.check_player_pos()
                if self.second_stage:
                    self.speed = 6
                else:
                    self.speed = 4

        if self.check_state:
            self.speed = 1
            self.shoot()

        if self.stun_state:
            self.state = 'stun'
            self.stun_tick -= 1
            self.speed = 0
            if self.stun_tick == 0:
                pygame.mixer.Sound('game_core/sounds/boss_laugh.wav').play()
                self.stun_state = False
                self.stun_tick = self.CONST_STUN_TICK

    # noinspection PyTypeChecker
    def shoot(self):
        if not self.shooting_state:
            # Playing a sound
            pygame.mixer.Sound('game_core/sounds/shoot.wav').play()

            # Spawning a projectile
            self.level_projectiles.add(
                projectile.Projectile(
                    pos=self.rect.center,
                    image_path='game_core/sprites/projectiles/shuriken/shuriken.png',
                    speed=2,
                    direction=pygame.math.Vector2(0, -1)
                )
            )

            self.shooting_state = True

        if self.shooting_state:
            self.shooting_tick -= 1
            if self.shooting_tick == 0:
                self.shooting_tick = self.CONST_SHOOTING_TICK
                self.shooting_state = False

    def hit(self):
        if not self.hit_state:
            self.hp -= 1
            self.hit_state = True

    def animate(self):
        super().animate()
        self.image = self.get_image()

    def update(self):
        super().update()
        self.attacks_check()
        self.states_update()
        self.stage_check()
        self.anim_states_update()


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
        self.state = 'run'


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

    def update(self):
        super().update()
        self.state = 'run'


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

    def update(self):
        super().update()
        self.state = 'run'
