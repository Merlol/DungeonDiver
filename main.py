import pygame
from player import Player
from enemy import Enemy

pygame.init()

#Set up display
WIDTH, HEIGHT = 1500, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dungeon Diver")
clock = pygame.time.Clock()

#Constants
GREY = (169, 169, 169)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)

#Sprites
 #Sprite Groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
swords = pygame.sprite.Group()

 #Sprite Generation
player = Player(40, 40, 7, WIDTH, HEIGHT, all_sprites, swords)
all_sprites.add(player)

enemy = Enemy(200, 200, 3, WIDTH, HEIGHT)
enemies.add(enemy)
all_sprites.add(enemy)

#Give screen background
screen.fill(GREY)

#Create A Level
def map_create():
    pass

#Game State Functions:
def game_run_screen():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    # --- Game Logic ---
    for sword in swords:
        enemy_hit = pygame.sprite.spritecollide(sword, enemies, True)

    for e in enemies:
        e.setPlayer(player)
    all_sprites.update()

    camera_y = player.rect.centery - HEIGHT // 2
    camera_x = player.rect.centerx - WIDTH // 2

    # --- Drawing ---
    screen.fill(GREY)
    for sprite in all_sprites:
        screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y - camera_y))

# --- Game Loop ---
FPS = 60
game_state = "RUN"
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    if game_state == "RUN":
        game_run_screen()

    elif game_state == "PAUSE":
        pass

    elif game_state == "START":
        pass

    elif game_state == "WIN":
        pass

    elif game_state == "DEAD":
        pass

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()