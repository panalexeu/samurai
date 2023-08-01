import pygame

import text


class DebugConsole:
    def __init__(self, surface, player, level_sprites):
        self.surface = surface

        self.player = player
        self.level_sprites = level_sprites.sprites()

        self.sprites_text = text.Text(
            font='Minecraft',
            size=8,
            color=(240, 240, 240),
            pos=(0, 0),
        )

        self.player_pos_text = text.Text(
            font='Minecraft',
            size=8,
            color=(240, 240, 240),
            pos=(0, 8),
        )

        self.player_directions = text.Text(
            font='Minecraft',
            size=8,
            color=(240, 240, 240),
            pos=(0, 16),
        )

        self.player_states = text.Text(
            font='Minecraft',
            size=8,
            color=(240, 240, 240),
            pos=(0, 24),
        )

        self.jump_cooldown = text.Text(
            font='Minecraft',
            size=8,
            color=(240, 240, 240),
            pos=(0, 32),
        )

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_q]:
            self.display()

    def display(self):
        self.sprites_text.display_text(f'sprites on the level:{len(self.level_sprites)}', self.surface)
        self.player_pos_text.display_text(f'player position x:{self.player.rect.x} y:{self.player.rect.y}',
                                          self.surface)
        self.player_directions.display_text(
            f'player directions x:{self.player.direction.x} y:{self.player.direction.y}', self.surface)
        self.player_states.display_text(f'STATES jump state:{self.player.jump_state}', self.surface)
        self.jump_cooldown.display_text(f'jump tick:{self.player.jump_tick} gravity:{self.player.player_gravity}',
                                        self.surface)
