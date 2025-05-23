import pygame
from sword import *
from spritesheet import SpriteSheet

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed, screen_width, screen_height, all_sprites, swords, wall_group, enemies, exits, tile_size):
        super().__init__()

        #Animation Frames
        player_image = pygame.image.load('../PygameTester/assets/Player.png').convert_alpha()
        sprite_sheet = SpriteSheet(player_image)
        BLACK = (0, 0, 0)
        self.rightframes = []
        for i in range(6):
            frame = sprite_sheet.get_image(i, 1, 32, 32, tile_size//75, BLACK)
            self.rightframes.append(frame)

        self.leftframes = []
        for i in range(6):
            frame = sprite_sheet.get_image(i, 1, 32, 32, tile_size // 75, BLACK)
            frame = pygame.transform.flip(frame, True, False)
            self.leftframes.append(frame)

        self.downframes = []
        for i in range(6):
            frame = sprite_sheet.get_image(i, 0, 32, 32, tile_size // 75, BLACK)
            self.downframes.append(frame)

        self.upframes = []
        for i in range(6):
            frame = sprite_sheet.get_image(i, 2, 32, 32, tile_size // 75, BLACK)
            self.upframes.append(frame)

        self.rightattackframes = []
        for i in range(4):
            frame = sprite_sheet.get_image(i, 7, 32, 32, tile_size // 75, BLACK)
            self.rightattackframes.append(frame)

        self.leftattackframes = []
        for i in range(4):
            frame = sprite_sheet.get_image(i, 7, 32, 32, tile_size // 75, BLACK)
            frame = pygame.transform.flip(frame, True, False)
            self.leftattackframes.append(frame)

        self.downattackframes = []
        for i in range(4):
            frame = sprite_sheet.get_image(i, 6, 32, 32, tile_size // 75, BLACK)
            self.downattackframes.append(frame)

        self.upattackframes = []
        for i in range(4):
            frame = sprite_sheet.get_image(i, 8, 32, 32, tile_size // 75, BLACK)
            self.upattackframes.append(frame)

        self.image = frame
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed
        self.width = screen_width
        self.height = screen_height
        self.all_sprites_group = all_sprites
        self.sword_group = swords
        self.last_slash = pygame.time.get_ticks()
        self.slash_cooldown = 1000
        self.direction = "N"
        self.dx = 0
        self.dy = 0
        self.walls = wall_group
        self.health = 3
        self.enemies = enemies
        self.immunity = 0
        self.exits = exits
        self.escape = False
        self.tile_size = tile_size

        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 75
        self.frame = 0
        self.swordframe = 0

    def update(self):
        keys = pygame.key.get_pressed()
        #If the player is slashing, they will not move
        if not self.sword_group:
            self.check_move(keys)
            print("moving")
            self.animation()
        else:
            print("sword")
            self.sword_animation()
        self.slash(keys, self.all_sprites_group, self.sword_group)
        self.hurt()


    def sword_animation(self):
        current_time = pygame.time.get_ticks()
        if self.direction == 'E' or self.direction == 'N':
            if current_time - self.last_update >= self.animation_cooldown:
                self.swordframe += 1
                self.last_update = current_time
                if self.swordframe >= len(self.rightattackframes):
                    self.swordframe = 0
            self.image = self.rightattackframes[self.swordframe]

        if self.direction == 'W':
            if current_time - self.last_update >= self.animation_cooldown:
                self.swordframe += 1
                self.last_update = current_time
                if self.swordframe >= len(self.leftattackframes):
                    self.swordframe = 0
            self.image = self.leftattackframes[self.swordframe]

        if self.direction == 'S':
            if current_time - self.last_update >= self.animation_cooldown:
                self.swordframe += 1
                self.last_update = current_time
                if self.swordframe >= len(self.downattackframes):
                    self.swordframe = 0
            self.image = self.downattackframes[self.swordframe]

        if self.direction == 'N':
            if current_time - self.last_update >= self.animation_cooldown:
                self.swordframe += 1
                self.last_update = current_time
                if self.swordframe >= len(self.upattackframes):
                    self.swordframe = 0
            self.image = self.upattackframes[self.swordframe]
    def animation(self):
        current_time = pygame.time.get_ticks()
        if self.direction == 'E' or self.direction == 'N':
            if current_time - self.last_update >= self.animation_cooldown:
                self.frame += 1
                self.last_update = current_time
                if self.frame >= len(self.rightframes):
                    self.frame = 0
            self.image = self.rightframes[self.frame]

        if self.direction == 'W':
            if current_time - self.last_update >= self.animation_cooldown:
                self.frame += 1
                self.last_update = current_time
                if self.frame >= len(self.leftframes):
                    self.frame = 0
            self.image = self.leftframes[self.frame]

        if self.direction == 'S':
            if current_time - self.last_update >= self.animation_cooldown:
                self.frame += 1
                self.last_update = current_time
                if self.frame >= len(self.downframes):
                    self.frame = 0
            self.image = self.downframes[self.frame]

        if self.direction == 'N':
            if current_time - self.last_update >= self.animation_cooldown:
                self.frame += 1
                self.last_update = current_time
                if self.frame >= len(self.upframes):
                    self.frame = 0
            self.image = self.upframes[self.frame]

    def check_move(self, keys):
        self.dx = 0
        self.dy = 0
        accel = 1
        if keys[pygame.K_LSHIFT]:
            accel = 2

        if keys[pygame.K_a]:
            self.dx = -(self.speed*accel)
            self.direction = "W"
        if keys[pygame.K_d]:
            self.dx = self.speed * accel
            self.direction = "E"
        if keys[pygame.K_w]:
            self.dy = -(self.speed * accel)
            self.direction = "N"
        if keys[pygame.K_s]:
            self.dy = self.speed * accel
            self.direction = "S"

        self.move()

    def move(self):
        self.escape = False

        self.rect.x += self.dx

        for exit in self.exits:
            if self.rect.colliderect(exit.rect):
                self.escape = True

        for wall in self.walls:
            if self.rect.colliderect(wall.rect):
                if self.dx > 0:
                    self.rect.right = wall.rect.left
                elif self.dx < 0:
                    self.rect.left = wall.rect.right

        self.rect.y += self.dy

        for exit in self.exits:
            if self.rect.colliderect(exit.rect):
                self.escape = True

        for wall in self.walls:
            if self.rect.colliderect(wall.rect):
                if self.dy > 0:
                    self.rect.bottom = wall.rect.top
                elif self.dy < 0:
                    self.rect.top = wall.rect.bottom

    def boundary_check(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.width:
            self.rect.right = self.width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.height:
            self.rect.bottom = self.height

    def slash(self, keys, all_sprites_group, sword_group):
        now = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and now-self.last_slash > self.slash_cooldown:
            if self.direction == "E":
                sword = Rightsword(self.rect.centerx, self.rect.centery, self.tile_size)
            if self.direction == "W":
                sword = Leftsword(self.rect.centerx, self.rect.centery, self.tile_size)
            if self.direction == "N":
                sword = Upsword(self.rect.centerx, self.rect.centery, self.tile_size)
            if self.direction == "S":
                sword = Downsword(self.rect.centerx, self.rect.centery, self.tile_size)
            all_sprites_group.add(sword)
            sword_group.add(sword)
            self.last_slash = now

    def hurt(self):
        if self.immunity != 0:
            self.immunity -= 1
        for enemy in self.enemies:
            if self.rect.colliderect(enemy.rect) and self.immunity == 0:
                self.health -= 1
                self.immunity = 45