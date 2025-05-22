import pygame

class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size):
        super().__init__()
        self.image = pygame.Surface((tile_size, tile_size))
        self.image.fill((255, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)