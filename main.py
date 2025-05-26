import pygame
from player import Player
from enemy import Enemy
from wall_tile import Wall
from keys import Keys
from exit import Exit
from pygame.math import Vector2
from floor import Floor

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
targetgroup = pygame.sprite.Group()
tile_sprites = pygame.sprite.Group()

 #Sprite Generation

#Give screen background
screen.fill(BLACK)

#Line of Sight function
def has_line_of_sight(enemy, player):
    global walls
    start = Vector2(enemy.rect.center)
    end = Vector2(player.rect.center)
    direction = (end - start).normalize()
    distance = start.distance_to(end)

    current_pos = start
    step = 5

    for i in range(0, int(distance), step):
        current_pos += direction * step
        point_rect = pygame.Rect(current_pos.x, current_pos.y, 1, 1)
        for wall in walls:
            if wall.rect.colliderect(point_rect):
                return False
    return True

#Draw Text function
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#Level Generation
def load_map(filename):
    global enemies, walls, all_sprites, keysx, keysy, player, exit

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
                floor = Floor(x, y, TILE_SIZE)
                tile_sprites.add(floor)
                enemy = Enemy(x + TILE_SIZE//2, y + TILE_SIZE//2, 7, WIDTH, HEIGHT, walls, TILE_SIZE, enemies)
                enemies.add(enemy)
                all_sprites.add(enemy)
            elif char == 'K':
                floor = Floor(x, y, TILE_SIZE)
                tile_sprites.add(floor)
                keysx = x + TILE_SIZE // 2
                keysy = y + TILE_SIZE // 2
            elif char == 'T':
                exit = Exit(x, y, TILE_SIZE, keys)
                walls.add(exit)
                tile_sprites.add(exit)
                exits.add(exit)
            elif char == 'P':
                floor = Floor(x, y, TILE_SIZE)
                tile_sprites.add(floor)
                player = Player(x + TILE_SIZE//2, y + TILE_SIZE//2, TILE_SIZE//5, TILE_SIZE//5, TILE_SIZE//25, WIDTH, HEIGHT, all_sprites, swords, walls, enemies, exits, TILE_SIZE)
                all_sprites.add(player)
            elif char == ' ':
                floor = Floor(x, y, TILE_SIZE)
                tile_sprites.add(floor)

#Game State Functions:
def game_run_screen():
    global running, player_info, player, game_state, gotkey, key_made, ui_open, exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_TAB:
                ui_open = not ui_open

    # --- Game Logic ---
     # Collisions
    for enemy in enemies:
        enemy_hit = pygame.sprite.spritecollide(enemy, swords,True)
        if enemy_hit:
            enemy.kill()

    for e in enemies:
        if e.knows:
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
        exit.open()
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

    for enemy in enemies:
        if has_line_of_sight(enemy, player):
            enemy.knows = True
        button = pygame.key.get_pressed()
        if button[pygame.K_TAB]:
            start = (enemy.rect.centerx - camera_x, enemy.rect.centery - camera_y)
            end = (player.rect.centerx - camera_x, player.rect.centery - camera_y)
            pygame.draw.line(screen, (255, 0, 0), start, end)

            player.draw(screen, (camera_x, camera_y))

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
ui_open = False
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
        win()

    elif game_state == "DEAD":
        game_over()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()