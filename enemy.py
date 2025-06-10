import pygame.sprite
from spritesheet import SpriteSheet

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, WIDTH, HEIGHT, wall_group, tile_size, enemy_group):
        super().__init__()

        #Sounds
        pygame.mixer.init()
        self.hitSound = pygame.mixer.Sound("assets/sounds/slimedies.mp3")
        self.moveSound = pygame.mixer.Sound("assets/sounds/slimejump.mp3")
        self.moveSound.set_volume(0.5)
        self.sound_cooldown = 0

        #Animation
        enemy_image = pygame.image.load('assets/Slime_Green.png').convert_alpha()
        sprite_sheet = SpriteSheet(enemy_image, 18, 15)
        BLACK = (0, 0, 0)

        self.frames = []
        for i in range(8):
            frame = sprite_sheet.get_image(i, 1, 28, 32, tile_size // 75, BLACK)
            self.frames.append(frame)

        self.image = frame
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 75
        self.frame = 0

        #Game Logic
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.speed = speed
        self.width = WIDTH
        self.height = HEIGHT
        self.player = None
        self.dx = 4
        self.dy = 0
         #These values are used for collisions later
        self.walls = wall_group
        self.enemies = enemy_group

        self.knows = False

    def setPlayer(self, player):
        self.player = player

    def update(self):
        self.check_move()
        self.animation()

    def check_move(self):
        if self.player:
            if self.player.rect.x > self.rect.x:
                self.dx = self.speed
            if self.player.rect.x < self.rect.x:
                self.dx = -(self.speed)
            if self.player.rect.y < self.rect.y:
                self.dy = -(self.speed)
            if self.player.rect.y > self.rect.y:
                self.dy = self.speed

        self.move()

    def animation(self):
        current_time = pygame.time.get_ticks()
        #Update the frame of the sprite each time the animation cooldown ends
        if current_time - self.last_update >= self.animation_cooldown:
            self.frame += 1
            self.last_update = current_time
            if self.frame >= len(self.frames):
                self.frame = 0
            if self.frame == 0:
                if self.sound_cooldown == 2:
                    self.moveSound.play()
                    self.sound_cooldown = 0
                else:
                    self.sound_cooldown += 1
        self.image = self.frames[self.frame]

    def move(self):
        if self.player == None:
            self.rect.x += self.dx
            #Check wall collisions
            for wall in self.walls:
                if self.rect.colliderect(wall.rect):
                    if self.dx > 0:
                        self.rect.right = wall.rect.left
                        self.dx = -self.dx
                    elif self.dx < 0:
                        self.rect.left = wall.rect.right
                        self.dx = -self.dx

            for other in self.enemies:
                if other != self and self.rect.colliderect(other.rect):
                    if self.dx > 0:
                        self.rect.right = other.rect.left
                        self.dx = -self.dx
                    elif self.dx < 0:
                        self.rect.left = other.rect.right
                        self.dx = -self.dx

            self.rect.y += self.dy
            # Check wall collisions
            for wall in self.walls:
                if self.rect.colliderect(wall.rect):
                    if self.dy > 0:
                        self.rect.bottom = wall.rect.top
                        self.dy = -self.dy
                    elif self.dy < 0:
                        self.rect.top = wall.rect.bottom
                        self.dy = -self.dy

            for other in self.enemies:
                if other != self and self.rect.colliderect(other.rect):
                    if self.dy > 0:
                        self.rect.right = other.rect.left
                        self.dy = -self.dy
                    elif self.dy < 0:
                        self.rect.left = other.rect.right
                        self.dy = -self.dy

        else:
            self.rect.x += self.dx
            for wall in self.walls:
                if self.rect.colliderect(wall.rect):
                    if self.dx > 0:
                        self.rect.right = wall.rect.left
                    elif self.dx < 0:
                        self.rect.left = wall.rect.right

            for other in self.enemies:
                if other != self and self.rect.colliderect(other.rect):
                    if self.dx > 0:
                        self.rect.right = other.rect.left
                    elif self.dx < 0:
                        self.rect.left = other.rect.right


            self.rect.y += self.dy
            for wall in self.walls:
                if self.rect.colliderect(wall.rect):
                    if self.dy > 0:
                        self.rect.bottom = wall.rect.top
                    elif self.dy < 0:
                        self.rect.top = wall.rect.bottom

            for other in self.enemies:
                if other != self and self.rect.colliderect(other.rect):
                    if self.dy > 0:
                        self.rect.right = other.rect.left
                    elif self.dy < 0:
                        self.rect.left = other.rect.right

    def rectOutline(self, screen, camera_offset):
        # Draw image with camera offset
        screen_pos = (self.rect.x - camera_offset[0], self.rect.y - camera_offset[1])

        # Draw rect outline in red
        pygame.draw.rect(screen, (255, 0, 0), (*screen_pos, self.rect.width, self.rect.height), 1)