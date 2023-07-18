import pygame

import main
import sprite
import text
import utils


class Player(sprite.Sprite):
    def __init__(self, surface):
        super().__init__(
            pos=main.saves_database.get_player_position(),
            image_path='game_core/sprites/player/idle/samurai_idle.png'
        )

        self.surface = surface

        # Animations and animation state
        self.frame_index = 0
        self.animation_speed = 0.1
        self.state = 'idle'
        self.animations = utils.import_sprites(
            sprites_path='game_core/sprites/player',
            animation_states={'idle': [], 'run': [], 'jump': [], 'bamboo_stick_attack': [], 'stun': []}
        )

        # Vectors
        self.direction = pygame.math.Vector2(0, 0)  # vector used for movement handling
        self.facing_right = True

        # Attack box
        self.attack_box = sprite.Sprite(self.rect.center, 1, 1, (255, 255, 255))
        self.attack_box_sprite = pygame.sprite.GroupSingle(self.attack_box)

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

        self.bamboo_stick_attack_state = False
        self.CONST_BAMBOO_STICK_ATTACK_TICK = 30
        self.bamboo_stick_attack_tick = 0

        self.stun_state = False
        self.CONST_STUN_TICK = 100
        self.stun_tick = self.CONST_STUN_TICK

        # Stats
        self.CONST_BAMBOO_STICK_LENGTH = 8
        self.bamboo_stick_length = 0

        # Items
        self.coins = 0

        # TODO CURRENTLY JUST FOR DEBUGGING
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
            self.bamboo_stick_attack_state = True

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
        else:
            self.state = 'idle'

    def states_update(self):
        if self.bamboo_stick_attack_state:
            self.lash_attack_handle()

        if self.jump_state:
            self.jump_handle()

        if self.stun_state:
            self.stun_handle()

        if self.immovable_state:
            self.immovable_state_handle()

    def lash_attack_handle(self):
        self.state = 'bamboo_stick_attack'
        self.immovable_state = True

        if self.bamboo_stick_length < self.CONST_BAMBOO_STICK_LENGTH:
            self.bamboo_stick_length += 1

        self.bamboo_stick_attack_tick += 1
        if self.bamboo_stick_attack_tick >= self.CONST_BAMBOO_STICK_ATTACK_TICK:
            self.immovable_state = False
            self.bamboo_stick_attack_state = False
            self.bamboo_stick_attack_tick = 0
            self.bamboo_stick_length = 0

        # Handling bamboo stick render
        bamboo_stick_color = (153, 229, 80)
        if self.facing_right:
            pygame.draw.line(self.surface, bamboo_stick_color, (self.rect.center[0] + 6, self.rect.center[1] - 3),
                             (self.rect.center[0] + 6 + self.bamboo_stick_length, self.rect.center[1] - 3))
            # Handling attack box
            self.attack_box.reset_position(
                (self.rect.center[0] + 6 + self.bamboo_stick_length, self.rect.center[1] - 2))
        else:
            pygame.draw.line(self.surface, bamboo_stick_color, (self.rect.center[0] - 6, self.rect.center[1] - 3),
                             (self.rect.center[0] - 6 - self.bamboo_stick_length, self.rect.center[1] - 3))
            # Handling attack box
            self.attack_box.reset_position(
                (self.rect.center[0] - 6 - self.bamboo_stick_length, self.rect.center[1] - 2))

        # Debug
        # self.attack_box_sprite.draw(self.surface)

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

    def death(self):
        self.reset_position(main.saves_database.get_player_position())

    def print_items(self, surface):
        self.coins_text.display_text(text=f'coins: {self.coins}', surface=surface)

    def update(self):
        if not self.immovable_state:
            self.get_input()
        self.animate()
        self.player_movement()
        self.anim_states_update()
        self.states_update()
