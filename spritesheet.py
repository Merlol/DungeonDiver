import pygame

class SpriteSheet():
    def __init__(self, image, offsetx, offsety):
        self.sheet = image
        self.offsetx = offsetx
        self.offsety = offsety

    def get_image(self, framex, framey, width, height, scale, colour):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0,0), ((framex * width) + (((framex + 1) * 2 - 1) * self.offsetx), (framey * height) + (self.offsety * 3), width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(colour)

        return image