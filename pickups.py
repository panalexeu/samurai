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


class HpMushroom(sprite.Sprite):
    def __init__(self, pos):
        super().__init__(
            pos=pos,
            image_path='game_core/sprites/castle/hp_mushroom.png'
        )


class StaminaMushroom(sprite.Sprite):
    def __init__(self, pos):
        super().__init__(
            pos=pos,
            image_path='game_core/sprites/castle/stamina_mushroom.png'
        )


class AntiGravityPotion(sprite.Sprite):
    def __init__(self, pos, player_obj: player.Player):
        super().__init__(
            pos,
            image_path='game_core/sprites/castle/antigravity_potion.png'
        )

        self.player = player_obj
        self.duration = 150

    def apply_effect(self):
        self.player.player_gravity = -1
        self.player.jump_speed = -3
        self.player.image = pygame.transform.flip(self.player.image, flip_y=True, flip_x=False)

    def stop_effect(self):
        self.player.player_gravity = self.player.CONST_PLAYER_GRAVITY
        self.player.jump_speed = self.player.CONST_JUMP_SPEED
