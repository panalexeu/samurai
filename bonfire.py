import pygame.mixer_music

import main
import sprite


class Bonfire(sprite.AnimatedSprite):
    def __init__(self, pos, level_key):
        super().__init__(
            pos,
            image_path='game_core/sprites/animated_sprites/bonfire/inaction/bonfire_inaction.png',
            anim_path='game_core/sprites/animated_sprites/bonfire',
            anim_states={'inaction': [], 'action': []},
            anim_speed=0.1
        )

        self.level_key = level_key

        self.state = 'inaction'

    def set_action(self):
        pygame.mixer.Sound('game_core/sounds/bonfire.wav').play()
        self.state = 'action'

    def save(self, player):
        main.saves_database.set_player_position(self.rect.x, self.rect.y, self.level_key)

        if player.potion:
            potion_state = 1
        else:
            potion_state = 0

        main.saves_database.set_stats(potion_state, player.souls, player.hp, player.stamina)
        player.upgrade_calculation()
        player.reset_stats()
