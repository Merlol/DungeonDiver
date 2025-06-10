import pygame

#This class is used to make obtaining frames from a spritesheet easier
class SpriteSheet():
    def __init__(self, image, offsetx, offsety):
        self.sheet = image
        #These values account for empty space between frames created by the author
        self.offsetx = offsetx
        self.offsety = offsety

    #The function requires the x and y values of the frame on the spritesheet to return the right frame
    def get_image(self, framex, framey, width, height, scale, colour):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0,0), ((framex * width) + (((framex + 1) * 2 - 1) * self.offsetx), (framey * height) + (self.offsety * 3), width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(colour)

        return image