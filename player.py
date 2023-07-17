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

        self.surface = surface

        # Animations and animation state
        self.frame_index = 0
        self.animation_speed = 0.1
        self.state = 'idle'
        self.animations = utils.import_sprites(
            sprites_path='game_core/sprites/player',
            animation_states={'idle': [], 'run': [], 'jump': [], 'prepare_lash_attack': [], 'lash_attack': [], 'stun': []}
        )

        # Collide box
        # self.collide_box = sprite.Sprite(pos, 11, 16, (255, 255, 255))
        # self.collide_box_sprite = pygame.sprite.GroupSingle(self.collide_box)

        # Vectors
        self.direction = pygame.math.Vector2(0, 0)  # vector used for movement handling
        self.facing_right = True

        # Speeds
        self.CONST_PLAYER_SPEED = 1
        self.player_speed = self.CONST_PLAYER_SPEED

        self.CONST_PLAYER_GRAVITY = 3
        self.player_gravity = self.CONST_PLAYER_GRAVITY

        self.CONST_JUMP_SPEED = 6
        self.jump_speed = self.CONST_JUMP_SPEED

        # Ticks and action states
        self.immovable_state = False

        self.jump_state = False
        self.CONST_JUMP_TICK = 40
        self.jump_tick = self.CONST_JUMP_TICK

        self.stun_state = False
        self.CONST_STUN_TICK = 100
        self.stun_tick = self.CONST_STUN_TICK

        self.lash_attack_state = False
        self.CONST_LASH_ATTACK_TICK = 30
        self.attack_lash_tick = self.CONST_LASH_ATTACK_TICK

        # Stats
        self.CONST_LASH_LENGTH = 16
        self.lash_length = 0

        # Items
        self.coins = 0

        # Inventory handling
        self.coins_text = text.Text(
            font='Minecraft',
            size=8,
            color=(240, 240, 240),
            pos=(0, 0),
        )

        # Other
        self.prev_bonfire = None

    def get_input(self):
        # Pressed keys handling
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
            self.state = 'prepare_lash_attack'

        # Unpressed keys handling
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_e:
                    self.lash_attack_state = True

    def player_movement(self):
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

    def anim_states_update(self):
        if self.direction.x != 0 and self.direction.y == 0:
            self.state = 'run'
        elif self.direction.y < 0:
            self.state = 'jump'
        elif self.lash_attack_state:
            self.state = 'lash_attack'
        else:
            self.state = 'idle'

    def states_update(self):
        if self.lash_attack_state:
            self.lash_attack_handle()

        if self.jump_state:
            self.jump_handle()

        if self.stun_state:
            self.stun_handle()

        if self.immovable_state:
            self.immovable_state_handle()

    def lash_attack_handle(self):
        self.immovable_state = True

        if self.lash_length < self.CONST_LASH_LENGTH:
            self.lash_length += 1
        else:
            self.immovable_state = False
            self.lash_attack_state = False
            self.lash_length = 0

        if self.facing_right:
            pygame.draw.line(self.surface, 'white', (self.rect.center[0] + 6, self.rect.center[1] - 3),
                             (self.rect.center[0] + 6 + self.lash_length, self.rect.center[1] - 3))
        else:
            pygame.draw.line(self.surface, 'white', (self.rect.center[0] - 6, self.rect.center[1] - 3),
                             (self.rect.center[0] + - 6 - self.lash_length, self.rect.center[1] - 3))

    def jump_handle(self):
        self.jump_tick -= 1
        if self.jump_tick == self.CONST_JUMP_TICK - 15:
            self.direction.y = 0
        elif self.jump_tick == 0:
            self.jump_state = False
            self.jump_tick = self.CONST_JUMP_TICK

    def stun_handle(self):
        self.state = 'stun'
        self.stun_tick -= 1
        self.immovable_state = True
        if self.stun_tick == 0:
            self.immovable_state = False
            self.stun_state = False
            self.stun_tick = self.CONST_STUN_TICK

    def immovable_state_handle(self):
        if self.immovable_state:
            self.direction.x = 0
            self.direction.y = 0

    def print_items(self, surface):
        self.coins_text.display_text(text=f'coins: {self.coins}', surface=surface)

    def update(self):
        if not self.immovable_state:
            self.get_input()
        self.animate()
        self.player_movement()
        self.anim_states_update()
        self.states_update()
