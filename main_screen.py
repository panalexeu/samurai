import pygame


class MainScreen:
    # Main screen and game settings
    SCREEN_SIZE = (320, 320)
    FRAME_RATE = 60

    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode(self.SCREEN_SIZE)
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            self.display.fill((124, 101, 101))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            pygame.display.update()
            self.clock.tick(self.FRAME_RATE)
