import pygame

class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size, keys):
        super().__init__()
        self.image = pygame.image.load('assets/closed.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.keys = keys
        self.tilesize = tile_size

    def open(self):
        self.image = pygame.image.load('assets/open.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.tilesize, self.tilesize))