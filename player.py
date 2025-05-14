import pygame
from sword import *

class Player(pygame.sprite.Sprite):
    def __init__(self, width, height, speed, screen_width, screen_height, all_sprites, swords, wall_group):
        super().__init__()
        self.image = pygame.Surface((width,height))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = 250
        self.rect.centery = 250
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

    def update(self):
        keys = pygame.key.get_pressed()
        #If the player is slashing, they will not move
        if not self.sword_group:
            self.check_move(keys)
        self.slash(keys, self.all_sprites_group, self.sword_group)

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
        self.rect.x += self.dx
        for wall in self.walls:
            if self.rect.colliderect(wall.rect):
                if self.dx > 0:
                    self.rect.right = wall.rect.left
                elif self.dx < 0:
                    self.rect.left = wall.rect.right

        self.rect.y += self.dy
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
                sword = Rightsword(self.rect.centerx, self.rect.centery)
            if self.direction == "W":
                sword = Leftsword(self.rect.centerx, self.rect.centery)
            if self.direction == "N":
                sword = Upsword(self.rect.centerx, self.rect.centery)
            if self.direction == "S":
                sword = Downsword(self.rect.centerx, self.rect.centery)
            all_sprites_group.add(sword)
            sword_group.add(sword)
            self.last_slash = now

