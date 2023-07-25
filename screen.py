import pygame

import level
import constants
import level_system
import main


class MainScreen:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode(constants.SCREEN_SIZE)
        self.surface = pygame.Surface(constants.SURFACE_SIZE)
        self.clock = pygame.time.Clock()

    def run(self):
        screen_level = level.Level(self.surface, main.saves_database.get_player_level_position())

        while True:
            # Screen level rendering
            screen_level.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    quit()

            # Scaling surface to screen
            self.display.blit(pygame.transform.scale(self.surface, constants.SCREEN_SIZE), (0, 0))

            pygame.display.update()
            self.clock.tick(constants.FRAME_RATE)
