import pygame

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

    def get_image(self, framex, framey, width, height, scale, colour):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0,0), ((framex * width), (framey * height), width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(colour)

        return image