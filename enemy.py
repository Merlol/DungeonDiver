import pygame.sprite

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, WIDTH, HEIGHT):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.speedx = speed
        self.speedy = speed
        self.width = WIDTH
        self.height = HEIGHT
        self.player = None

    def setPlayer(self, player):
        self.player = player

    def update(self):
        if self.player.rect.x > self.rect.x:
            self.rect.x += self.speedx
        if self.player.rect.x < self.rect.x:
            self.rect.x -= self.speedx
        if self.player.rect.y > self.rect.y:
            self.rect.y += self.speedy
        if self.player.rect.y < self.rect.y:
            self.rect.y -= self.speedx