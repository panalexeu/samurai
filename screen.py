import pygame

import level
import constants


class MainScreen:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode(constants.SCREEN_SIZE)
        self.surface = pygame.Surface(constants.SURFACE_SIZE)
        self.clock = pygame.time.Clock()

    def run(self):
        # debug level init
        debug_level = level.Level(self.surface, constants.DEBUG_LEVEL, level_gravity=1)

        while True:
            self.surface.fill((124, 101, 101))

            # debug level rendering
            debug_level.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        quit()

            # Scaling surface to screen
            self.display.blit(pygame.transform.scale(self.surface, constants.SCREEN_SIZE), (0, 0))

            pygame.display.update()
            self.clock.tick(constants.FRAME_RATE)