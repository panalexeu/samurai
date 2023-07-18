import itertools

import pygame

import bonfire
import coin
import constants
import debug_console
import main
import player
import sprite
import basic_enemy


class Level:
    def __init__(self, surface, level_map):
        self.surface = surface

        # Level sprites init (rendering ones)
        self.collision_sprites = pygame.sprite.Group()
        self.animating_sprites = pygame.sprite.Group()
        self.destroyable_sprites = pygame.sprite.Group()

        # Interactive sprites
        self.interactive_sprites = pygame.sprite.Group()

        # Pickups init
        self.pickups = pygame.sprite.Group()

        # Enemies init
        self.enemies = pygame.sprite.Group()

        # Player init
        self.player = player.Player(self.surface)
        self.player_sprite = pygame.sprite.GroupSingle()
        self.player_sprite.add(self.player)

        # Map init
        self.level_map_init(level_map)

        # Console init
        self.level_console = debug_console.DebugConsole(self.surface, self.player, self.collision_sprites)

    def level_map_init(self, level_map):
        for row_index, row in enumerate(level_map):
            for column_index, column in enumerate(row):
                x = column_index * 8
                y = row_index * 8

                if column == '1':
                    self.collision_sprites.add(
                        sprite.Sprite(
                            pos=(x, y),
                            image_path='game_core/sprites/level_1/brick.png'
                        )
                    )  # had some problems with that line
                elif column == 'C':
                    self.pickups.add(coin.Coin(pos=(x, y)))
                elif column == 'Y':
                    self.enemies.add(basic_enemy.Yokai(pos=(x, y)))
                elif column == 'S':
                    self.enemies.add(basic_enemy.Spider(pos=(x, y)))
                elif column == 'B':
                    bonfire_ = bonfire.Bonfire(pos=(x, y))
                    self.animating_sprites.add(bonfire_)
                    self.interactive_sprites.add(bonfire_)
                # elif column == 'P':
                #     # self.player.reset_position((x, y))
                #     self.player_sprite.add(self.player)

    def level_scroll(self):
        for sprite_ in self.get_all_sprite_groups():  # joins pickups and destroyable with collision sprites
            # x coordinate scrolling
            indent_x = constants.SURFACE_SIZE[0] / 4
            if self.player.rect.x < indent_x and self.player.direction.x < 0:
                self.player.player_speed = 0
                scroll_x = self.player.CONST_PLAYER_SPEED
            elif self.player.rect.x > constants.SURFACE_SIZE[0] - indent_x and self.player.direction.x > 0:
                self.player.player_speed = 0
                scroll_x = -self.player.CONST_PLAYER_SPEED
            else:
                scroll_x = 0
                self.player.player_speed = self.player.CONST_PLAYER_SPEED

            # y coordinate scrolling
            indent_y = constants.SURFACE_SIZE[1] / 3
            if self.player.rect.y < indent_y and self.player.direction.y < 0:
                self.player.jump_speed = 0
                self.player.player_gravity = 0
                scroll_y = self.player.CONST_JUMP_SPEED - self.player.CONST_PLAYER_GRAVITY
            elif self.player.rect.y > constants.SURFACE_SIZE[1] - indent_y and self.player.direction.y >= 0:
                self.player.jump_speed = 0
                self.player.player_gravity = 0
                scroll_y = -self.player.CONST_PLAYER_GRAVITY
            else:
                scroll_y = 0
                self.player.player_gravity = self.player.CONST_PLAYER_GRAVITY
                self.player.jump_speed = self.player.CONST_JUMP_SPEED

            # applying scrolling
            sprite_.shift(scroll_x, scroll_y)

    def player_vertical_collisions(self):
        for sprite_ in self.collision_sprites:
            if sprite_.rect.colliderect(self.player.rect):
                if self.player.direction.y < 0 and self.player.rect.y > sprite_.rect.y:
                    self.player.rect.top = sprite_.rect.bottom
                    self.player.direction.y = 0
                elif self.player.direction.y == 0 and self.player.rect.y < sprite_.rect.y:
                    self.player.rect.bottom = sprite_.rect.top

    def player_horizontal_collisions(self):
        for sprite_ in self.collision_sprites:
            if sprite_.rect.colliderect(self.player.rect):
                if self.player.direction.x > 0 and sprite_.rect.y in range(
                        self.player.rect.y - self.player.CONST_PLAYER_GRAVITY,
                        self.player.rect.y + self.player.rect.size[1] // 2
                ):
                    self.player.rect.right = sprite_.rect.left
                elif self.player.direction.x < 0 and sprite_.rect.y in range(
                        self.player.rect.y - self.player.CONST_PLAYER_GRAVITY,
                        self.player.rect.y + self.player.rect.size[1] // 2
                ):
                    self.player.rect.left = sprite_.rect.right

    def enemies_collisions(self):
        for enemy in self.enemies:
            for sprite_ in self.collision_sprites:
                if sprite_.rect.colliderect(enemy.rect):
                    if isinstance(enemy, basic_enemy.Yokai):
                        if enemy.direction.x == 1:
                            enemy.direction.x = -1
                        else:
                            enemy.direction.x = 1
                    elif isinstance(enemy, basic_enemy.Spider):
                        if enemy.direction.y == -1:
                            enemy.direction.y = 1
                        else:
                            enemy.direction.y = -1

    def pickups_collisions(self):
        collision = pygame.sprite.spritecollide(self.player, self.pickups,
                                                dokill=True)  # here is possible to check with which object u collided (coin, item, posion)

        if len(collision) > 0:
            collision_obj = collision[0]
            if isinstance(collision_obj, coin.Coin):
                self.player.coins += 1

    # TODO Implement hints system
    def interactive_sprites_collisions(self):
        for sprite_ in self.interactive_sprites:
            if sprite_.rect.colliderect(self.player.rect):

                # Bonfires handling
                if isinstance(sprite_, bonfire.Bonfire):
                    if self.player.prev_bonfire:
                        self.player.prev_bonfire.set_inaction()
                    sprite_.set_action()
                    self.player.prev_bonfire = sprite_

                    # DEBUG
                    # TODO IMPLEMENT SAVING LEVEL SCROLL
                    sprite_.save_position()

    def get_all_sprite_groups(self):
        return itertools.chain(self.collision_sprites, self.animating_sprites, self.pickups,
                               self.destroyable_sprites)

    def animate_sprites(self):
        for spite_ in self.animating_sprites:
            spite_.animate()

    def animate_pickups(self):
        for sprite_ in self.pickups:
            if isinstance(sprite_, sprite.AnimatedSprite):
                sprite_.animate()

    def enemies_update(self):
        for sprite_ in self.enemies:
            sprite_.update()

    def enemies_hit_collision(self):
        for sprite_ in self.enemies:
            if sprite_.rect.colliderect(self.player.rect):
                self.player.death()

    def player_hit_collision(self):
        if self.player.bamboo_stick_attack_state:
            pygame.sprite.spritecollide(self.player.attack_box, self.enemies, dokill=True)

    def update(self):
        self.surface.fill((0, 0, 10))

        # Level scroll
        # self.level_scroll()

        # Level sprites render and animations
        self.collision_sprites.draw(self.surface)
        self.animating_sprites.draw(self.surface)
        self.pickups.draw(self.surface)
        self.animate_sprites()
        self.animate_pickups()

        # Level objects collisions handling
        self.pickups_collisions()
        self.interactive_sprites_collisions()

        # Enemies handling
        self.enemies.draw(self.surface)
        self.enemies_update()
        self.enemies_collisions()
        self.player_hit_collision()
        self.enemies_hit_collision()

        # Player handling and render
        self.player.update()
        self.player_horizontal_collisions()
        self.player_vertical_collisions()
        self.player_sprite.draw(self.surface)
        # TODO: Player items (IN PROGRESS INVENTORY)
        self.player.print_items(self.surface)

        # debug console
        self.level_console.update()
