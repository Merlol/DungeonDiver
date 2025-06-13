import pygame

BLACK = (0,0,0)

#Different sword types to change where the sword is in relation to the player
class Rightsword(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size):
        super().__init__()
        self.image = pygame.Surface((tile_size//4,tile_size//4))
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.rect.left = x
        self.rect.centery = y
        self.var = 0

    def update(self):
        self.var += 1
        if self.var == 10:
            self.kill()

class Leftsword(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size):
        super().__init__()
        self.image = pygame.Surface((tile_size//4,tile_size//4))
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.rect.right = x
        self.rect.centery = y
        self.var = 0

    def update(self):
        self.var += 1
        if self.var == 10:
            self.kill()

class Upsword(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size):
        super().__init__()
        self.image = pygame.Surface((tile_size//4,tile_size//4))
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.rect.bottom = y
        self.rect.centerx = x
        self.var = 0

    def update(self):
        self.var += 1
        if self.var == 10:
            self.kill()

class Downsword(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size):
        super().__init__()
        self.image = pygame.Surface((tile_size//4,tile_size//4))
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.rect.top = y
        self.rect.centerx = x
        self.var = 0

    def update(self):
        self.var += 1
        if self.var == 10:
            self.kill()