import pygame.sprite

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, WIDTH, HEIGHT, wall_group):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.speed = speed
        self.width = WIDTH
        self.height = HEIGHT
        self.player = None
        self.dx = 4
        self.dy = 0
        self.walls = wall_group

    def setPlayer(self, player):
        self.player = player

    def update(self):
        keys = pygame.key.get_pressed()
        self.check_move(keys)

    def check_move(self, keys):

        if not (self.player == None):
            if self.player.rect.x > self.rect.x:
                self.dx = self.speed
            if self.player.rect.x < self.rect.x:
                self.dx = -(self.speed)
            if self.player.rect.y < self.rect.y:
                self.dy = -(self.speed)
            if self.player.rect.y > self.rect.y:
                self.dy = self.speed

        self.move()

    def move(self):
        if self.player == None:
            self.rect.x += self.dx
            print(self.dx)
            for wall in self.walls:
                if self.rect.colliderect(wall.rect):
                    if self.dx > 0:
                        self.rect.right = wall.rect.left
                        self.dx = -self.dx
                    elif self.dx < 0:
                        self.rect.left = wall.rect.right
                        self.dx = -self.dx

            self.rect.y += self.dy
            for wall in self.walls:
                if self.rect.colliderect(wall.rect):
                    if self.dy > 0:
                        self.rect.bottom = wall.rect.top
                        self.dy = -self.dy
                    elif self.dy < 0:
                        self.rect.top = wall.rect.bottom
                        self.dy = -self.dy