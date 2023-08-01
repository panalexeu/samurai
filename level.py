import pygame

import bonfire
import bar
import constants
import enemy
import level_system
import main
import pickups
import player
import sprite


class Level:
    # noinspection PyTypeChecker
    def __init__(self, surface, level_map_key):
        self.surface = surface
        self.level_map_key = level_map_key

        # Level backgrounds
        self.background = (102, 57, 49)
        self.level_background = level_system.LEVEL_COLOR[level_map_key]

        # # Level music handling
        # pygame.mixer.music.load('game_core/sounds/castle_theme.mp3')
        # pygame.mixer.music.play(-1)

        # Entrance system init
        self.level_entrances = {'east': [], 'west': [], 'north': [], 'south': []}

        # Level sprites init (rendering ones)
        self.collision_sprites = pygame.sprite.Group()
        self.level_background_sprites = pygame.sprite.Group()
        self.background_sprites = pygame.sprite.Group()
        self.animating_sprites = pygame.sprite.Group()
        self.destroyable_sprites = pygame.sprite.Group()

        # Interactive sprites
        self.interactive_sprites = pygame.sprite.Group()

        # Traps init
        self.traps_sprites = pygame.sprite.Group()

        # Pickups init
        self.pickups = pygame.sprite.Group()

        # Enemies init
        self.enemies = pygame.sprite.Group()

        # Projectiles
        self.projectiles = pygame.sprite.Group()

        # Player init
        self.player = player.Player(self.surface)
        self.init_player_items()
        self.player_sprite = pygame.sprite.GroupSingle()
        self.player_sprite.add(self.player)

        # Boss init
        self.boss = None
        self.boss_bar = None

        # Inventory and bars init
        self.hp_bar = bar.HpBar((14, 2), self.surface)
        self.stamina_bar = bar.StaminaBar((14, 8), self.surface)
        self.potion_bar = bar.PotionBar((2, 2), self.surface)
        self.souls_bar = bar.SoulsBar((0, 22), self.surface)

        # Level map init
        self.level_map_init()

        # Console init
        # self.level_console = debug_console.DebugConsole(self.surface, self.player, self.collision_sprites)

    # noinspection PyTypeChecker
    def level_map_init(self, prev_direction=None):
        level_map = level_system.LEVEL_MAPS[self.level_map_key]

        self.boss = None
        self.boss_bar = None

        max_x_len = max([len(row) for row in level_map])  # calculates the longest x row in the level map

        shift_x = ((constants.SURFACE_SIZE[0] - max_x_len * 8) / 2)
        shift_y = ((constants.SURFACE_SIZE[1] - len(level_map) * 8) / 2)

        for row_index, row in enumerate(level_map):
            for column_index, cell in enumerate(row):
                # Centering the level map on the surface algorithm
                x = column_index * 8 + shift_x
                y = row_index * 8 + shift_y
                pos = (x, y)

                # Adding level background sprites
                if cell != ' ':
                    self.level_background_sprites.add(
                        sprite.Sprite(pos=pos, size_x=8, size_y=8, color=self.level_background))

                # Collision sprites
                if cell == '1':
                    self.collision_sprites.add(
                        sprite.Sprite(
                            pos=pos,
                            image_path='game_core/sprites/castle/brick.png'
                        )
                    )
                elif cell == '2':
                    self.collision_sprites.add(
                        sprite.Sprite(
                            pos=pos,
                            image_path='game_core/sprites/castle/brick_window.png'
                        )
                    )
                elif cell == '3':
                    self.collision_sprites.add(
                        sprite.Sprite(
                            pos=pos,
                            image_path='game_core/sprites/castle/brick_var.png'
                        )
                    )
                elif cell == '4':
                    self.collision_sprites.add(
                        sprite.Sprite(
                            pos=pos,
                            image_path='game_core/sprites/castle/old_brick.png'
                        )
                    )
                elif cell == '9':
                    self.collision_sprites.add(
                        sprite.Sprite(
                            pos=pos,
                            image_path='game_core/sprites/castle/brick_roof.png'
                        )
                    )
                elif cell == '_':
                    self.collision_sprites.add(
                        sprite.Sprite(
                            pos=pos,
                            image_path='game_core/sprites/castle/grass.png'
                        )
                    )
                elif cell == '+':
                    self.collision_sprites.add(
                        sprite.Sprite(
                            pos=pos,
                            image_path='game_core/sprites/castle/dirt.png'
                        )
                    )

                # Background sprites
                elif cell == 'l':
                    self.animating_sprites.add(
                        sprite.AnimatedSprite(
                            pos=pos,
                            image_path='game_core/sprites/animated_sprites/back_light/idle/back_light1.png',
                            anim_path='game_core/sprites/animated_sprites/back_light',
                            anim_states={'idle': []},
                            anim_speed=0.1
                        )
                    )
                elif cell == 't':
                    self.animating_sprites.add(
                        sprite.AnimatedSprite(
                            pos=pos,
                            image_path='game_core/sprites/animated_sprites/sewer_tube/idle/sewer_tube1.png',
                            anim_path='game_core/sprites/animated_sprites/sewer_tube',
                            anim_states={'idle': []},
                            anim_speed=0.1
                        )
                    )
                elif cell == 'c':
                    self.background_sprites.add(
                        sprite.Sprite(
                            pos=pos,
                            image_path='game_core/sprites/castle/chain_back.png'
                        )
                    )
                elif cell == 'k':
                    self.level_background_sprites.add(
                        sprite.Sprite(
                            pos=pos,
                            image_path='game_core/sprites/castle/cage.png'
                        )
                    )

                # Destroyable
                elif cell == 'D':
                    self.destroyable_sprites.add(
                        sprite.Sprite(
                            pos=pos,
                            image_path='game_core/sprites/castle/old_brick.png'
                        )
                    )

                # Traps
                elif cell == 'T':
                    self.traps_sprites.add(
                        sprite.Sprite(
                            pos=pos,
                            image_path='game_core/sprites/castle/spikes.png'
                        )
                    )
                elif cell == 'w':
                    self.traps_sprites.add(
                        sprite.Sprite(
                            pos=pos,
                            image_path='game_core/sprites/castle/sewer_water.png'
                        )
                    )

                # Entrances
                elif cell == 'E':
                    if prev_direction == 'west':
                        self.player.reset_position(pos=(x + 11, y))

                    self.background_sprites.add(
                        sprite.Sprite(
                            pos=(x, y),
                            image_path='game_core/sprites/castle/brick_door.png'
                        )
                    )

                    self.level_entrances['east'].append(
                        sprite.Sprite(
                            pos=(x, y),
                            image_path='game_core/sprites/castle/transparent.png'
                        )
                    )
                elif cell == 'W':
                    if prev_direction == 'east':
                        self.player.reset_position(pos=(x - 11, y))

                    self.background_sprites.add(
                        sprite.Sprite(
                            pos=(x, y),
                            image_path='game_core/sprites/castle/brick_door.png'
                        )
                    )

                    self.level_entrances['west'].append(
                        sprite.Sprite(pos=(x, y), image_path='game_core/sprites/castle/transparent.png')
                    )
                elif cell == 'N':
                    if prev_direction == 'south':
                        self.player.reset_position(pos=(x, y + 11))

                    tube_north_sprite = sprite.Sprite(pos=(x, y), image_path='game_core/sprites/castle/tube.png')
                    tube_north_sprite.flip(y=True)

                    self.background_sprites.add(
                        tube_north_sprite
                    )

                    self.level_entrances['north'].append(
                        sprite.Sprite(pos=(x, y), image_path='game_core/sprites/castle/transparent.png')
                    )
                elif cell == 'S':
                    if prev_direction == 'north':
                        self.player.reset_position(pos=(x - 11, y - 11))

                    self.background_sprites.add(
                        sprite.Sprite(
                            pos=(x, y),
                            image_path='game_core/sprites/castle/tube.png'
                        )
                    )

                    self.level_entrances['south'].append(
                        sprite.Sprite(pos=(x, y), image_path='game_core/sprites/castle/transparent.png')
                    )
                elif cell == 's':
                    if prev_direction == 'north':
                        self.player.reset_position(pos=(x + 11, y - 11))

                    self.background_sprites.add(
                        sprite.Sprite(
                            pos=(x, y),
                            image_path='game_core/sprites/castle/tube.png'
                        )
                    )

                    self.level_entrances['south'].append(
                        sprite.Sprite(pos=(x, y), image_path='game_core/sprites/castle/transparent.png')
                    )

                # Pickups
                elif cell == 'C':
                    self.pickups.add(pickups.Coin(pos=pos))
                elif cell == 'g':
                    self.pickups.add(
                        pickups.AntiGravityPotion(pos=pos, player_obj=self.player))
                elif cell == 'h':
                    self.pickups.add(
                        pickups.HpMushroom(pos=pos)
                    )
                elif cell == 'e':
                    self.pickups.add(
                        pickups.StaminaMushroom(pos=pos)
                    )

                # Enemies
                elif cell == 'Y':
                    self.enemies.add(enemy.Yokai(pos=pos))
                elif cell == 'P':
                    self.enemies.add(enemy.Spider(pos=pos))
                elif cell == '>':
                    self.enemies.add(enemy.ShootingSkeleton(pos=pos, level_projectiles=self.projectiles))
                elif cell == '<':
                    self.enemies.add(
                        enemy.ShootingSkeleton(pos=pos, level_projectiles=self.projectiles, rotation=False))
                elif cell == '*':
                    self.boss = enemy.DeadSamuraiBoss(pos=pos, player_obj=self.player,
                                                      level_projectiles=self.projectiles)
                    self.boss_bar = bar.BossHpBar(self.surface, 'Dead Samurai')
                    self.enemies.add(self.boss)

                # Interactive sprites
                elif cell == 'B':
                    bonfire_ = bonfire.Bonfire(pos=pos, level_key=self.level_map_key)
                    self.animating_sprites.add(bonfire_)
                    self.interactive_sprites.add(bonfire_)

    def clear_entrance_sprites(self):
        for value in self.level_entrances.values():
            value.clear()

    def clear_level_sprites(self):
        self.level_background_sprites.empty()
        self.collision_sprites.empty()
        self.background_sprites.empty()
        self.animating_sprites.empty()
        self.destroyable_sprites.empty()
        self.interactive_sprites.empty()
        self.traps_sprites.empty()
        self.pickups.empty()
        self.enemies.empty()
        self.projectiles.empty()
        self.clear_entrance_sprites()

    def player_vertical_collisions(self):
        for sprite_ in self.collision_sprites:
            if sprite_.rect.colliderect(self.player.rect):
                if self.player.player_gravity > 0:
                    if self.player.direction.y < 0 and self.player.rect.y > sprite_.rect.y:
                        self.player.rect.top = sprite_.rect.bottom
                        self.player.direction.y = 0
                    elif self.player.direction.y == 0 and self.player.rect.y < sprite_.rect.y:
                        self.player.rect.bottom = sprite_.rect.top
                # Vertical collisions for negative gravity
                elif self.player.player_gravity < 0:
                    if self.player.direction.y == 0 and self.player.rect.y > sprite_.rect.y:
                        self.player.rect.top = sprite_.rect.bottom
                    elif self.player.direction.y < 0 and self.player.rect.y < sprite_.rect.y:
                        self.player.rect.bottom = sprite_.rect.top
                        self.player.direction.y = 0

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
        for enemy_ in self.enemies:
            for sprite_ in self.collision_sprites:
                if sprite_.rect.colliderect(enemy_.rect):
                    if isinstance(enemy_, enemy.Yokai):
                        if enemy_.direction.x == 1:
                            enemy_.direction.x = -1
                        else:
                            enemy_.direction.x = 1
                    elif isinstance(enemy_, enemy.Spider):
                        if enemy_.direction.y == -1:
                            enemy_.direction.y = 1
                        else:
                            enemy_.direction.y = -1
                    elif isinstance(enemy_, enemy.DeadSamuraiBoss):
                        if enemy_.direction.x == 1:
                            if enemy_.charge_state:
                                enemy_.stun_state = True
                            enemy_.direction.x = -1
                            enemy_.rect.x = enemy_.rect.x - 1  # Without this collisions break I guess this is connected with the sprite size
                        else:
                            if enemy_.charge_state:
                                enemy_.stun_state = True
                            enemy_.direction.x = 1
                            enemy_.rect.x = enemy_.rect.x + 1  # Without this collisions break I guess this is connected with the sprite size

    def pickups_collisions(self):
        collision = pygame.sprite.spritecollide(self.player, self.pickups, dokill=True)

        if len(collision) > 0:
            collision_obj = collision[0]
            if isinstance(collision_obj, pickups.Coin):
                pygame.mixer.Sound('game_core/sounds/coin_pickup.wav').play()
                self.player.souls += 1
            elif isinstance(collision_obj, pickups.HpMushroom):
                pygame.mixer.Sound('game_core/sounds/powerup.wav').play()
                self.player.hp = self.player.CONST_HP
            elif isinstance(collision_obj, pickups.StaminaMushroom):
                pygame.mixer.Sound('game_core/sounds/powerup.wav').play()
                self.player.stamina = self.player.CONST_STAMINA
            elif isinstance(collision_obj, pickups.AntiGravityPotion):
                pygame.mixer.Sound('game_core/sounds/powerup.wav').play()
                self.player.potion = collision_obj

    def destroyable_sprites_collision(self):
        pygame.sprite.spritecollide(self.player, self.destroyable_sprites, dokill=True)

    def traps_collision(self):
        for sprite_ in self.traps_sprites:
            if sprite_.rect.colliderect(self.player.rect):
                pygame.mixer.Sound('game_core/sounds/explosion.wav').play()
                self.player_death()

    def interactive_sprites_collisions(self):
        for sprite_ in self.interactive_sprites:
            if sprite_.rect.colliderect(self.player.rect):
                # Bonfires handling
                if isinstance(sprite_, bonfire.Bonfire):
                    if sprite_.state == 'inaction':
                        sprite_.set_action()
                        self.player.reset_stats()
                        sprite_.save(self.player)

    def entrance_collision(self):
        for direction_key in self.level_entrances:
            for sprite_ in self.level_entrances[direction_key]:
                if sprite_.rect.colliderect(self.player.rect):
                    pygame.mixer.Sound('game_core/sounds/entrance.wav').play()
                    self.level_map_key = level_system.LEVEL_ADJACENCY_MAP[self.level_map_key][direction_key]
                    self.level_background = level_system.LEVEL_COLOR[self.level_map_key]
                    self.clear_level_sprites()
                    self.level_map_init(direction_key)

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
                self.player.hit()

    def projectiles_update(self):
        for sprite_ in self.projectiles:
            sprite_.update()

    def projectiles_hit_collision(self):
        for sprite_ in self.projectiles:
            if sprite_.rect.colliderect(self.player.rect):
                self.player.hit()

    def projectiles_destroy_collision(self):
        for sprite_ in self.collision_sprites:
            pygame.sprite.spritecollide(sprite_, self.projectiles, dokill=True)

    # noinspection PyTypeChecker
    def player_hit_collision(self):
        if self.player.bamboo_stick_attack_state:
            for enemy_ in self.enemies:
                if self.player.attack_box.rect.colliderect(enemy_.rect):
                    if isinstance(enemy_, enemy.DeadSamuraiBoss):
                        enemy_.hit()
                        if enemy_.hp < 1:
                            pygame.mixer.Sound('game_core/sounds/enemy_died.wav').play()
                            pygame.mixer.Sound('game_core/sounds/game_over.mp3').play()
                            self.player.souls += enemy_.souls
                            self.enemies.remove(enemy_)
                            self.boss = None
                            self.boss_bar = None
                    else:
                        pygame.mixer.Sound('game_core/sounds/enemy_died.wav').play()
                        self.player.souls += enemy_.souls
                        self.enemies.remove(enemy_)

    def player_death(self):
        self.clear_level_sprites()
        self.player.reset_stats()
        self.player.souls = 0
        self.player.reset_position(main.saves_database.get_player_position())
        self.level_map_key = main.saves_database.get_player_level_position()
        self.level_background = level_system.LEVEL_COLOR[self.level_map_key]
        self.level_map_init()

    def check_player_death(self):
        if self.player.hp <= 0:
            self.player_death()

    def init_player_items(self):
        if main.saves_database.get_potion():
            self.player.potion = pickups.AntiGravityPotion(pos=self.player.rect.bottomleft, player_obj=self.player)

    def update(self):
        # Background drawing
        self.surface.fill(self.background)

        # Level background drawing
        self.level_background_sprites.draw(self.surface)

        # Level sprites render and animations
        self.collision_sprites.draw(self.surface)
        self.background_sprites.draw(self.surface)
        self.animating_sprites.draw(self.surface)
        self.destroyable_sprites.draw(self.surface)
        self.traps_sprites.draw(self.surface)
        self.pickups.draw(self.surface)
        self.animate_sprites()
        self.animate_pickups()

        # Level objects collisions handling
        self.pickups_collisions()
        self.traps_collision()
        self.destroyable_sprites_collision()
        self.interactive_sprites_collisions()

        # Enemies handling
        self.enemies.draw(self.surface)
        self.enemies_update()
        self.enemies_collisions()
        self.player_hit_collision()
        self.enemies_hit_collision()

        # Projectiles handling
        self.projectiles.draw(self.surface)
        self.projectiles.update()
        self.projectiles_hit_collision()
        self.projectiles_destroy_collision()

        # Entrance collision checking
        self.entrance_collision()

        # Player handling and render
        self.player.update()
        self.player_horizontal_collisions()
        self.player_vertical_collisions()
        self.player_sprite.draw(self.surface)
        self.check_player_death()

        # Inventory and bars
        self.hp_bar.update(points=self.player.hp, points_const=self.player.CONST_HP)
        self.stamina_bar.update(points=self.player.stamina, points_const=self.player.CONST_STAMINA)
        self.potion_bar.update(self.player.potion)
        self.souls_bar.update(self.player.souls)
        if self.boss_bar:
            self.boss_bar.update(self.boss.hp, self.boss.HP_CONST)

        # # debug console
        # self.level_console.update()
