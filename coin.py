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
