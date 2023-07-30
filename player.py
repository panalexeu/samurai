import pygame

import main
import sprite
import text
import utils


class Player(sprite.Sprite):
    # noinspection PyTypeChecker
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

        # Jump
        self.jump_state = False
        self.CONST_JUMP_TICK = 40
        self.jump_tick = self.CONST_JUMP_TICK

        # Bamboo stick attack
        self.bamboo_stick_attack_state = False
        self.CONST_BAMBOO_STICK_ATTACK_TICK = 30
        self.bamboo_stick_attack_tick = 0
        self.CONST_BAMBOO_STICK_LENGTH = 8
        self.bamboo_stick_length = 0

        # Stun
        self.stun_state = False
        self.CONST_STUN_TICK = 100
        self.stun_tick = self.CONST_STUN_TICK

        self.hit_state = False
        self.CONST_HIT_TICK = 30
        self.hit_tick = self.CONST_HIT_TICK

        self.regen_state = False
        self.CONST_REGEN_TICK = 150
        self.regen_tick = self.CONST_REGEN_TICK

        # Potions
        self.potion_state = False
        self.potion_tick = 0

        # Stats
        self.CONST_HP = 3
        self.hp = self.CONST_HP

        self.CONST_STAMINA = 6
        self.stamina = self.CONST_STAMINA

        # Items
        self.coins = 0
        self.potion = None

        # TODO CURRENTLY JUST FOR DEBUGGING
        # Inventory handling
        self.coins_text = text.Text(
            font='Minecraft',
            size=8,
            color=(240, 240, 240),
            pos=(0, 0),
        )

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
                pygame.mixer.Sound('game_core/sounds/jump.wav').play()
                self.direction.y = -1
                self.jump_state = True
        else:
            self.direction.y = 0

        # Bamboo stick attack
        if keys[pygame.K_e]:
            pygame.mixer.Sound('game_core/sounds/hit.wav').play()
            self.bamboo_stick_attack_state = True

        # Potion usage
        if keys[pygame.K_c]:
            if self.potion and not self.potion_state:
                pygame.mixer.Sound('game_core/sounds/potion.wav').play()
                self.potion_state = True

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
            self.state = 'bamboo_stick_attack'
            self.immovable_state = True

            if self.bamboo_stick_length < self.CONST_BAMBOO_STICK_LENGTH:
                self.bamboo_stick_length += 1  # bamboo stick deploying speed

            self.bamboo_stick_attack_tick += 1
            if self.bamboo_stick_attack_tick >= self.CONST_BAMBOO_STICK_ATTACK_TICK:
                self.immovable_state = False
                self.bamboo_stick_attack_state = False
                self.bamboo_stick_attack_tick = 0
                self.bamboo_stick_length = 0

            # Handling bamboo stick render
            bamboo_stick_color = (153, 229, 80)

            if self.facing_right:
                stick_x_factor = 1
            else:
                stick_x_factor = -1

            if self.player_gravity < 0:
                stick_y_factor = 1
                stick_hb_y_factor = 2
            else:
                stick_y_factor = -3
                stick_hb_y_factor = -2

            # Drawing stick
            pygame.draw.line(
                self.surface,
                bamboo_stick_color,
                (self.rect.center[0] + 6 * stick_x_factor, self.rect.center[1] + stick_y_factor),
                (self.rect.center[0] + 6 * stick_x_factor + self.bamboo_stick_length * stick_x_factor,
                 self.rect.center[1] + stick_y_factor)
            )

            # Handling attack box
            self.attack_box.reset_position(
                (self.rect.center[0] + 6 * stick_x_factor + self.bamboo_stick_length * stick_x_factor,
                 self.rect.center[1] + stick_hb_y_factor)
            )

            # self.attack_box_sprite.draw(self.surface)

        if self.jump_state:
            self.jump_tick -= 1
            if self.jump_tick == self.CONST_JUMP_TICK - 15:
                self.hit_stamina()
                self.direction.y = 0
            elif self.jump_tick == 0:
                self.jump_state = False
                self.jump_tick = self.CONST_JUMP_TICK

        if self.stun_state:
            self.state = 'stun'
            self.stun_tick -= 1
            self.immovable_state = True
            if self.stun_tick == 0:
                self.immovable_state = False
                self.stun_state = False
                self.stun_tick = self.CONST_STUN_TICK

        if self.immovable_state:
            self.direction.x = 0
            self.direction.y = 0

        if self.hit_state:
            self.hit_tick -= 1
            if self.hit_tick == 0:
                self.hit_state = False
                self.hit_tick = self.CONST_HIT_TICK

        if self.regen_state:
            self.regen_tick -= 1
            if self.regen_tick == 0:
                self.stamina += 1
                self.regen_tick = self.CONST_REGEN_TICK
                if self.stamina >= self.CONST_STAMINA:
                    self.stamina = self.CONST_STAMINA
                    self.regen_state = False

        if self.potion_state:
            self.potion_tick += 1
            self.potion.apply_effect()
            if self.potion_tick == self.potion.duration:
                self.potion.stop_effect()
                self.potion_tick = 0
                self.potion_state = False

    def reset_stats(self):
        self.hp = self.CONST_HP
        self.stamina = self.CONST_STAMINA

    def hit(self):
        if not self.hit_state:
            pygame.mixer.Sound('game_core/sounds/explosion.wav').play()
            self.hit_state = True
            self.hp -= 1

    def hit_stamina(self):
        self.regen_state = True
        self.stamina -= 1

    def check_low_stamina(self):
        if self.stamina <= 0:
            self.stun_state = True

    def print_items(self, surface):
        self.coins_text.display_text(text=f'coins: {self.coins}', surface=surface)

    def update(self):
        if not self.immovable_state:
            self.get_input()
        self.animate()
        self.player_movement()
        self.anim_states_update()
        self.check_low_stamina()
        self.states_update()
