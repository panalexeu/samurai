import pygame

import text


class DebugConsole:
    def __init__(self, surface, player, level_sprites):
        self.player = player
        self.level_sprites = level_sprites.sprites()

        self.player_pos_text = text.Text(
            font='Minecraft',
            size=16,
            color=(240, 240, 240),
            pos=(0, 0),
            surface=surface
        )

        self.sprites_text = text.Text(
            font='Minecraft',
            size=16,
            color=(240, 240, 240),
            pos=(0, 16),
            surface=surface
        )

        self.player_states = text.Text(
            font='Minecraft',
            size=16,
            color=(240, 240, 240),
            pos=(0, 32),
            surface=surface
        )

        self.jump_cooldown = text.Text(
            font='Minecraft',
            size=16,
            color=(240, 240, 240),
            pos=(0, 48),
            surface=surface
        )

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_F1]:
            self.display()

    def display(self):
        self.player_pos_text.display_text(f'player position x:{self.player.rect.x} y:{self.player.rect.y}')
        self.sprites_text.display_text(f'sprites on the level:{len(self.level_sprites)}')
        self.player_states.display_text(f'jump state:{self.player.jump_state}')
        self.jump_cooldown.display_text(f'jump cooldown:{self.player.jump_cooldown}')
