import pygame
from player import Player
from enemy import Enemy
from wall_tile import Wall

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
BLACK = (0,0,0)
TILE_SIZE = 200

#Sprites
 #Sprite Groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
swords = pygame.sprite.Group()
walls = pygame.sprite.Group()

 #Sprite Generation
player = Player(40, 40, 7, WIDTH, HEIGHT, all_sprites, swords, walls)
all_sprites.add(player)

#Give screen background
screen.fill(BLACK)

#Level Generation
def load_map(filename):
    global enemies, walls, all_sprites

    with open(filename, 'r') as file:
        lines = file.readlines()

    for row_index, line in enumerate(lines):
        for col_index, char in enumerate(line.strip('\n')):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            if char == 'X':
                wall = Wall(x, y, TILE_SIZE)
                walls.add(wall)
                all_sprites.add(wall)
            elif char == 'E':
                enemy = Enemy(x, y, 3, WIDTH, HEIGHT, walls)
                enemies.add(enemy)
                all_sprites.add(enemy)

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
     # Collisions
    for enemy in enemies:
        enemy_hit = pygame.sprite.spritecollide(enemy, swords,True)
        if enemy_hit:
            enemy.kill()


    #for e in enemies:
     #   e.setPlayer(player)
    all_sprites.update()

    camera_y = player.rect.centery - HEIGHT // 2
    camera_x = player.rect.centerx - WIDTH // 2

    # --- Drawing ---
    screen.fill(BLACK)
    for sprite in all_sprites:
        screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y - camera_y))

# --- Game Loop ---
FPS = 60
game_state = "RUN"
running = True
map_loaded = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    if game_state == "RUN":
        if not map_loaded:
            load_map("maps/lvl1.txt")
            map_loaded = True
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