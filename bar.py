import pygame

import pickups
import sprite
import text


class PotionBar:
    def __init__(self, pos, surface):
        self.pos = pos
        self.image = pygame.image.load('game_core/sprites/icons/potion_bar.png')
        self.surface = surface

    def update(self, potion: pickups.AntiGravityPotion):
        self.surface.blit(self.image, self.pos)
        if potion:
            self.surface.blit(potion.image, (self.pos[0] + 1, self.pos[1] + 1))


class SoulsBar:
    # noinspection PyTypeChecker
    def __init__(self, pos, surface):
        self.pos = pos
        self.surface = surface

        self.souls_sprite = sprite.AnimatedSprite(
                pos=pos,
                image_path='game_core/sprites/animated_sprites/souls/idle/souls1.png',
                anim_path='game_core/sprites/animated_sprites/souls',
                anim_states={'idle': []},
                anim_speed=0.1
            )

        self.souls_group = pygame.sprite.GroupSingle(self.souls_sprite)

        self.text = text.Text(
            'Minecraft',
            size=8,
            color='white',
            pos=(self.pos[0] + 8, self.pos[1] - 8)
        )

    def update(self, souls):
        self.souls_sprite.animate()
        self.souls_group.draw(self.surface)
        self.text.display_text(str(souls), self.surface)


class Bar:
    def __init__(self, pos, surface, bar_img, empty_bar_img, shift):
        self.pos = pos
        self.surface = surface
        self.bar_img = bar_img
        self.empty_bar_img = empty_bar_img
        self.shift = shift

    def update(self, points, points_const):
        for index in range(points_const):
            if index in range(points):
                self.surface.blit(self.bar_img, (self.pos[0] + index * self.shift, self.pos[1]))
            else:
                self.surface.blit(self.empty_bar_img, (self.pos[0] + index * self.shift, self.pos[1]))


class HpBar(Bar):
    def __init__(self, pos, surface):
        super().__init__(
            pos,
            surface,
            bar_img=pygame.image.load('game_core/sprites/icons/hp_bar.png'),
            empty_bar_img=pygame.image.load('game_core/sprites/icons/empty_hp_bar.png'),
            shift=7
        )


class StaminaBar(Bar):
    def __init__(self, pos, surface):
        super().__init__(
            pos,
            surface,
            bar_img=pygame.image.load('game_core/sprites/icons/stamina_bar.png'),
            empty_bar_img=pygame.image.load('game_core/sprites/icons/empty_stamina_bar.png'),
            shift=3
        )


class BossHpBar(HpBar):
    def __init__(self, surface, boss_name):
        self.pos = (65, 20)

        super().__init__(self.pos, surface)

        self.boss_name = boss_name
        self.text = text.Text(
            'Minecraft',
            8,
            'white',
            pos=(self.pos[0], self.pos[1] - 8)
        )

    def update(self, points, points_const):
        super().update(points, points_const)
        self.text.display_text(self.boss_name, self.surface)
