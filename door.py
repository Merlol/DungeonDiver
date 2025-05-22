import pygame

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size):
        super().__init__()
        self.image = pygame.Surface((tile_size, tile_size))
        #self.image.fill((0, 100, 100))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)