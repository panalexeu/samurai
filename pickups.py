import pygame.image

import player
import sprite


class Coin(sprite.AnimatedSprite):

    def __init__(self, pos):
        super().__init__(
            pos,
            image_path='game_core/sprites/animated_sprites/coin/idle/coin1.png',
            anim_path='game_core/sprites/animated_sprites/coin',
            anim_states={'idle': []},
            anim_speed=0.1
        )


class AntiGravityPotion(sprite.Sprite):
    def __init__(self, pos, image_path, player: player.Player):
        super().__init__(
            pos,
            image_path=image_path
        )

        self.player = player
        self.duration = 150

    def apply_effect(self):
        self.player.player_gravity = -1
        self.player.jump_speed = -3
        self.player.image = pygame.transform.flip(self.player.image, flip_y=True, flip_x=False)

    def stop_effect(self):
        self.player.player_gravity = self.player.CONST_PLAYER_GRAVITY
        self.player.jump_speed = self.player.CONST_JUMP_SPEED
