import pygame

import level
import constants


class MainScreen:
    # Main screen and game settings
    SCREEN_SIZE = (600, 450)  # 600 : 450 = 4 : 3
    SURFACE_SIZE = (300, 225)
    FRAME_RATE = 60

    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode(self.SCREEN_SIZE)
        self.surface = pygame.Surface(self.SURFACE_SIZE)
        self.clock = pygame.time.Clock()

    def run(self):
        # debug level init
        debug_level = level.Level(self.surface, constants.DEBUG_LEVEL)

        while True:
            self.surface.fill((124, 101, 101))

            # debug level rendering
            debug_level.render()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            # Scaling surface to screen
            self.display.blit(pygame.transform.scale(self.surface, self.SCREEN_SIZE), (0, 0))

            pygame.display.update()
            self.clock.tick(self.FRAME_RATE)
