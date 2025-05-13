import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((100, 100))
        self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)