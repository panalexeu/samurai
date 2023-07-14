import sprite


class Bonfire(sprite.AnimatedSprite):
    def __init__(self, pos):
        super().__init__(
            pos,
            image_path='game_core/sprites/animated_sprites/bonfire/inaction/bonfire_inaction.png',
            anim_path='game_core/sprites/animated_sprites/bonfire',
            anim_states={'inaction': [], 'action': []},
            anim_speed=0.1
        )

        self.state = 'inaction'

    def set_action(self):
        self.state = 'action'

    def set_inaction(self):
        self.state = 'inaction'

    def save_coordinates(self, coordinates):
        pass
