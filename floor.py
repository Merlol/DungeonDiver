import pygame

#This is just graphical. There isn't even any collision
class Floor(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size):
        super().__init__()
        self.image = pygame.image.load('assets/floor.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)