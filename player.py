import pygame

import sprite
import utils


class Player(sprite.Sprite):
    def __init__(self, pos, size_x, size_y, color):
        super().__init__(pos, size_x, size_y, color)

        # animations
        self.frame_index = 0
        self.animation_speed = 0.1
        self.animations = self.import_sprites()
        print(self.animations)  # for debugging

        # size
        self.size_x = size_x
        self.size_y = size_y

        # vectors and player state
        self.state = 'idle'
        self.direction = pygame.math.Vector2(0, 0)  # vector used for movement handling
        self.facing_right = True

        # speeds
        self.CONST_PLAYER_SPEED = 1
        self.player_speed = self.CONST_PLAYER_SPEED

        self.CONST_PLAYER_GRAVITY = 3
        self.player_gravity = self.CONST_PLAYER_GRAVITY

        self.CONST_JUMP_SPEED = 6
        self.jump_speed = self.CONST_JUMP_SPEED

        # ticks and action states
        self.jump_state = False
        self.CONST_JUMP_TICK = 40
        self.jump_tick = self.CONST_JUMP_TICK

    @staticmethod
    def import_sprites():
        sprites_path = 'game_core/sprites/player/'
        animations = {'idle': [], 'run': []}

        for animation in animations.keys():
            full_path = sprites_path + animation + '/'
            animations[animation] = utils.load_animation(full_path)

        return animations

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE]:
            if not self.jump_state:
                self.direction.y = -1
                self.jump_state = True
        else:
            self.direction.y = 0

        # handling input of the player movement and gravity
        self.rect.x += self.direction.x * self.player_speed
        self.rect.y += self.direction.y * self.jump_speed + self.player_gravity

    def animate(self):
        animation = self.animations[self.state]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            self.image = pygame.transform.flip(image, flip_x=True, flip_y=False)

    def states_update(self):
        if self.direction.x != 0:
            self.state = 'run'
        else:
            self.state = 'idle'

    def ticks_update(self):
        # Jumping handling
        if self.jump_state:
            self.jump_tick -= 1
            if self.jump_tick == self.CONST_JUMP_TICK - 15:
                self.direction.y = 0
            elif self.jump_tick == 0:
                self.jump_state = False
                self.jump_tick = self.CONST_JUMP_TICK

    def update(self):
        self.get_input()
        self.animate()
        self.states_update()
        self.ticks_update()
