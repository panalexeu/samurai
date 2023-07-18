import pygame

import utils


class Sprite(pygame.sprite.Sprite):
    def __init__(
            self,
            pos,
            size_x=None,
            size_y=None,
            color=None,
            image_path=None
    ):
        super().__init__()

        if color and size_x and size_y:
            self.resize(size_x, size_y)
            self.image.fill(color)
        else:
            self.image = pygame.image.load(image_path)

        self.rect = self.image.get_rect(bottomleft=pos)

    def reset_position(self, pos):
        self.rect = self.image.get_rect(bottomleft=pos)

    def resize(self, size_x, size_y):
        self.image = pygame.Surface((size_x, size_y))

    def shift(self, shift_x, shift_y):
        self.rect.x += shift_x
        self.rect.y += shift_y


class AnimatedSprite(Sprite):
    def __init__(
            self,
            pos,
            image_path,
            anim_path,
            anim_states,
            anim_speed
    ):
        super().__init__(pos, image_path=image_path)

        self.frame_index = 0
        self.anim_speed = anim_speed
        self.anim_path = anim_path
        self.anim_states = anim_states
        self.state = 'idle'

        self.animations = utils.import_sprites(anim_path, anim_states)

    def animate(self):
        animation = self.animations[self.state]
        self.frame_index += self.anim_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]

