import pygame

class Keys(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/key.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 20))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)