import pygame
from player import Player
from enemy import Enemy
from wall_tile import Wall
from door import Door
from keys import Keys
from exit import Exit

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
YELLOW = (255, 255, 0)
TILE_SIZE = 150

#Fonts
font = pygame.font.SysFont('Arial', 24)# None = default
big_font = pygame.font.SysFont("Arial", 100)

loss = big_font.render("GAME OVER", True, YELLOW)

#Sprites
 #Sprite Groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
swords = pygame.sprite.Group()
walls = pygame.sprite.Group()
doors = pygame.sprite.Group()
exits = pygame.sprite.Group()
keys = pygame.sprite.Group()
tile_sprites = pygame.sprite.Group()

 #Sprite Generation

#Give screen background
screen.fill(BLACK)

#Draw Text function
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#Level Generation
def load_map(filename):
    global enemies, walls, all_sprites, keysx, keysy, player

    with open(filename, 'r') as file:
        lines = file.readlines()

    for row_index, line in enumerate(lines):
        for col_index, char in enumerate(line.strip('\n')):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            if char == 'X':
                wall = Wall(x, y, TILE_SIZE)
                walls.add(wall)
                tile_sprites.add(wall)
            elif char == 'E':
                enemy = Enemy(x, y, 3, WIDTH, HEIGHT, walls, TILE_SIZE)
                enemies.add(enemy)
                all_sprites.add(enemy)
            elif char == 'D':
                door = Door(x, y, TILE_SIZE)
                doors.add(door)
                tile_sprites.add(door)
            elif char == 'K':
                keysx = x
                keysy = y
            elif char == 'T':
                exit = Exit(x, y, TILE_SIZE)
                walls.add(exit)
                tile_sprites.add(exit)
                exits.add(exit)
            elif char == 'P':
                player = Player(x, y, TILE_SIZE//5, TILE_SIZE//5, TILE_SIZE//25, WIDTH, HEIGHT, all_sprites, swords, walls, enemies, exits, TILE_SIZE)
                all_sprites.add(player)

#Game State Functions:
def game_run_screen():
    global running, player_info, player, game_state, gotkey, key_made
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

    door_touch = pygame.sprite.spritecollide(player, doors, False)
    if door_touch:
        player_info = True

    if player_info:
        for e in enemies:
            e.setPlayer(player)

    if player.health == 0:
        game_state = "DEAD"

    if not enemies and not keys and not key_made:
        key = Keys(keysx, keysy)
        all_sprites.add(key)
        keys.add(key)
        key_made = True

    collect = pygame.sprite.spritecollide(player, keys, True)
    if collect:
        gotkey = True
        key = Keys(WIDTH - 10, 10)
        keys.add(key)

    all_sprites.update()

    if gotkey:
        if player.escape:
            game_state = "WIN"

    camera_y = player.rect.centery - HEIGHT // 2
    camera_x = player.rect.centerx - WIDTH // 2

    # --- Drawing ---
    screen.fill(BLACK)
    if gotkey:
        for key in keys:
            screen.blit(key.image, (WIDTH - 30,  10))
    for sprite in tile_sprites:
        screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y - camera_y))
    for sprite in all_sprites:
        if not sprite == player:
            screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y - camera_y))
    screen.blit(player.image, (player.rect.x - camera_x, player.rect.y - camera_y))
    draw_text(f"Health: {player.health}", font, WHITE, 10, 10)

def game_over():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.fill(BLUE)
    draw_text("GAME OVER", big_font, YELLOW, WIDTH // 3, 300)

def win():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.fill(BLUE)
    draw_text("YOU WIN!", big_font, YELLOW, WIDTH // 3, 300)

# --- Game Loop ---
FPS = 60
game_state = "RUN"
running = True
map_loaded = False
player_info = False
keysx = 0
keysx = 0
key_made = False
gotkey = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    if game_state == "RUN":
        if not map_loaded:
            load_map("maps/lvl2.txt")
            map_loaded = True
        game_run_screen()

    elif game_state == "PAUSE":
        pass

    elif game_state == "START":
        pass

    elif game_state == "WIN":
        win()

    elif game_state == "DEAD":
        game_over()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()