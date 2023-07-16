import pygame

import main
import sprite
import text
import utils


class Player(sprite.Sprite):
    def __init__(self, surface):
        super().__init__(
            pos=main.saves_database.get_player_position()[0],
            image_path='game_core/sprites/player/idle/samurai_idle1.png'
        )

        # Surface init
        self.surface = surface

        # Animations and animation state
        self.frame_index = 0
        self.animation_speed = 0.1
        self.state = 'idle'
        self.animations = utils.import_sprites(
            sprites_path='game_core/sprites/player',
            animation_states={'idle': [], 'run': [], 'jump': [], 'attack': [], 'stun': []}
        )

        # Collide box
        # self.collide_box = sprite.Sprite(pos, 11, 16, (255, 255, 255))
        # self.collide_box_sprite = pygame.sprite.GroupSingle(self.collide_box)

        # Vectors
        self.direction = pygame.math.Vector2(0, 0)  # vector used for movement handling
        self.facing_right = True

        # Attack range
        self.CONST_ATTACK_RANGE = 5
        self.attack_range = 0

        # Speeds
        self.CONST_PLAYER_SPEED = 1
        self.player_speed = self.CONST_PLAYER_SPEED

        self.CONST_PLAYER_GRAVITY = 3
        self.player_gravity = self.CONST_PLAYER_GRAVITY

        self.CONST_JUMP_SPEED = 6
        self.jump_speed = self.CONST_JUMP_SPEED

        # Ticks and action states
        self.jump_state = False
        self.CONST_JUMP_TICK = 40
        self.jump_tick = self.CONST_JUMP_TICK

        self.stun_state = False
        self.CONST_STUN_TICK = 100
        self.stun_tick = self.CONST_STUN_TICK

        # Items
        self.prev_bonfire = None

        self.coins = 0
        self.coins_text = text.Text(
            font='Minecraft',
            size=8,
            color=(240, 240, 240),
            pos=(0, 0),
        )

    def get_input(self):
        # Pressed keys
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

        if keys[pygame.K_e]:
            self.draw_attack_range_line()

        # Unpressed keys
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_e:
                    self.state = 'attack'
                    self.attack_range = 0

    def player_movement(self):
        self.rect.x += self.direction.x * self.player_speed
        self.rect.y += self.direction.y * self.jump_speed + self.player_gravity

    def draw_attack_range_line(self):
        if self.attack_range <= self.CONST_ATTACK_RANGE:
            self.attack_range += 1

        if self.facing_right:
            pygame.draw.line(self.surface, 'white', self.rect.bottomright,
                             (self.rect.bottomright[0] + self.attack_range, self.rect.bottomright[1]), 1)
        else:
            pygame.draw.line(self.surface, 'white', self.rect.bottomleft,
                             (self.rect.bottomleft[0] - self.attack_range, self.rect.bottomright[1]), 1)

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
        if self.direction.x != 0 and self.direction.y == 0:
            self.state = 'run'
        elif self.direction.y < 0:
            self.state = 'jump'
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

        if self.stun_state:
            self.state = 'stun'
            self.stun_tick -= 1
            if self.stun_tick == 0:
                self.stun_state = False
                self.stun_tick = self.CONST_STUN_TICK

    def print_items(self, surface):
        self.coins_text.display_text(text=f'coins: {self.coins}', surface=surface)

    def update(self):
        if not self.stun_state:
            self.get_input()
        self.animate()
        self.player_movement()
        self.states_update()
        self.ticks_update()
