import pygame


class Bar:
    def __init__(self, pos, surface, bar_img, shift):
        self.pos = pos
        self.surface = surface
        self.bar_img = bar_img
        self.shift = shift

    def update(self, points):
        for index in range(points):
            self.surface.blit(self.bar_img, (self.pos[0] + index * self.shift, self.pos[1]))


class HpBar(Bar):
    def __init__(self, pos, surface):
        super().__init__(
            pos,
            surface,
            bar_img=pygame.image.load('game_core/sprites/icons/hp_bar.png'),
            shift=7
        )


class StaminaBar(Bar):
    def __init__(self, pos, surface):
        super().__init__(
            pos,
            surface,
            bar_img=pygame.image.load('game_core/sprites/icons/stamina_bar.png'),
            shift=3
        )
