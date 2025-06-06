import pygame
from sword import *
from spritesheet import SpriteSheet

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed, screen_width, screen_height, all_sprites, swords, wall_group, enemies, exits, tile_size):
        super().__init__()

        #Animation Frames
        player_image = pygame.image.load('assets/Player.png').convert_alpha()
        sprite_sheet = SpriteSheet(player_image, 0, 0)
        BLACK = (0, 0, 0)
        self.upbaseframe = sprite_sheet.get_image(0, 2, 32, 32, tile_size//75, BLACK)
        self.upbaseframe = sprite_sheet.get_image(0, 2, 32, 32, tile_size // 75, BLACK)
        self.rightframes = []
        for i in range(6):
            frame = sprite_sheet.get_image(i, 1, 32,32, tile_size//75, BLACK)
            self.rightframes.append(frame)

        self.leftframes = []
        for i in range(6):
            frame = sprite_sheet.get_image(i, 1, 32, 32, tile_size // 75, BLACK)
            frame = pygame.transform.flip(frame, True, False)
            frame.set_colorkey((BLACK))
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
            frame.set_colorkey((BLACK))
            self.leftattackframes.append(frame)

        self.downattackframes = []
        for i in range(4):
            frame = sprite_sheet.get_image(i, 6, 32, 32, tile_size // 75, BLACK)
            self.downattackframes.append(frame)

        self.upattackframes = []
        for i in range(4):
            frame = sprite_sheet.get_image(i, 8, 32, 32, tile_size // 75, BLACK)
            self.upattackframes.append(frame)

        self.rightsprintframes = []
        for i in range(6):
            frame = sprite_sheet.get_image(i, 4, 32, 32, tile_size // 75, BLACK)
            self.rightsprintframes.append(frame)

        self.rightsprintframes = []
        for i in range(6):
            frame = sprite_sheet.get_image(i, 4, 32, 32, tile_size // 75, BLACK)
            self.rightsprintframes.append(frame)

        self.leftsprintframes = []
        for i in range(6):
            frame = sprite_sheet.get_image(i, 4, 32, 32, tile_size // 75, BLACK)
            frame = pygame.transform.flip(frame, True, False)
            frame.set_colorkey((BLACK))
            self.leftsprintframes.append(frame)

        self.downsprintframes = []
        for i in range(6):
            frame = sprite_sheet.get_image(i, 3, 32, 32, tile_size // 75, BLACK)
            self.downsprintframes.append(frame)

        self.upsprintframes = []
        for i in range(6):
            frame = sprite_sheet.get_image(i, 5, 32, 32, tile_size // 75, BLACK)
            self.upsprintframes.append(frame)

        self.image = frame
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        #self.rect.inflate_ip(-16, -16)

        #Sounds
        pygame.mixer.init()

        self.slash_sound = pygame.mixer.Sound("assets/sounds/slash.mp3")
        self.step = pygame.mixer.Sound("assets/sounds/footstep.mp3")


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
        self.sound(keys)
        #If the player is slashing, they will not move
        if not self.sword_group:
            if self.swordframe != 0:
                self.sword_animation()
            else:
                self.check_move(keys)
                self.animation(keys)
        else:
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
    def animation(self, keys):
        current_time = pygame.time.get_ticks()
        self.swordframe = 0
        if keys[pygame.K_LSHIFT]:
            if self.direction == 'E':
                if current_time - self.last_update >= self.animation_cooldown:
                    self.frame += 1
                    self.last_update = current_time
                    if self.frame >= len(self.rightsprintframes):
                        self.frame = 0
                self.image = self.rightsprintframes[self.frame]

            if self.direction == 'W':
                if current_time - self.last_update >= self.animation_cooldown:
                    self.frame += 1
                    self.last_update = current_time
                    if self.frame >= len(self.leftsprintframes):
                        self.frame = 0
                self.image = self.leftsprintframes[self.frame]

            if self.direction == 'S':
                if current_time - self.last_update >= self.animation_cooldown:
                    self.frame += 1
                    self.last_update = current_time
                    if self.frame >= len(self.downsprintframes):
                        self.frame = 0
                self.image = self.downsprintframes[self.frame]

            if self.direction == 'N':
                if current_time - self.last_update >= self.animation_cooldown:
                    self.frame += 1
                    self.last_update = current_time
                    if self.frame >= len(self.upsprintframes):
                        self.frame = 0
                self.image = self.upsprintframes[self.frame]
        else:
            if self.direction == 'E':
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

    def slash(self, keys, all_sprites_group, sword_group):
        now = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and now-self.last_slash > self.slash_cooldown:
            self.slash_sound.play()
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

    def sound(self, keys):
        if keys[pygame.K_LSHIFT]:
            if self.frame == 0 or self.frame == 3:
                self.step.stop()
                self.step.play()
        else:
            if keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]:
                if self.frame == 0:
                    self.step.stop()
                    self.step.play()

    def draw(self, screen, camera_offset):
        # Draw image with camera offset
        screen_pos = (self.rect.x - camera_offset[0], self.rect.y - camera_offset[1])

        # Draw rect outline in red
        pygame.draw.rect(screen, (255, 0, 0), (*screen_pos, self.rect.width, self.rect.height), 1)