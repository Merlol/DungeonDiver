import pygame
from player import Player
from enemy import Enemy
from wall_tile import Wall
from keys import Keys
from exit import Exit
from pygame.math import Vector2
from floor import Floor
import math

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
big_font = pygame.font.Font("assets/fonts/pixelfont.ttf", 100)
game_font = pygame.font.Font("assets/fonts/pixelfont.ttf", 32)

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

#Start Screen
def start():
    global running, game_state, titlePos, titlePosMult
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    button = pygame.key.get_pressed()
    if button[pygame.K_RETURN]:
        game_state = "LEVEL1"

    screen.fill(BLACK)
    if titlePos >= 1:
        titlePosMult = -1
    elif titlePos <= -1:
        titlePosMult = 1

    titlePos += 0.04 * titlePosMult

    screen.blit(title_image, ((WIDTH / 2 - (title_image.get_width() / 2)), 40 * math.sin(titlePos) + (HEIGHT / 15)))

    draw_text("Press Enter to Continue", game_font, WHITE, (WIDTH/3.2), 600)

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
    global running, player, game_state, gotkey, key_made, ui_open, exit, level
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
        print("key made")

    collect = pygame.sprite.spritecollide(player, keys, True)
    if collect:
        gotkey = True
        exit.open()
        key = Keys(WIDTH - 10, 10)
        keys.add(key)


    all_sprites.update()

    if gotkey:
        if player.escape:
            level = True

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
            enemy.draw(screen, (camera_x, camera_y))

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

    screen.fill(BLACK)
    draw_text("GAME OVER", big_font, WHITE, WIDTH // 3.5, 300)

def win():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.fill(BLACK)
    draw_text("YOU WON!", big_font, WHITE, WIDTH // 3.5, 300)

# --- Game Loop ---
FPS = 60
game_state = "START"
running = True
map_loaded = False
key_made = False
gotkey = False
ui_open = False
level = False

#Start Screen UI
title_image = pygame.image.load('assets/title.png').convert_alpha()
title_image = pygame.transform.scale(title_image, (500, 500))
title_image.set_colorkey(BLACK)
titlePos = 1
titlePosMult = 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    if game_state == "LEVEL1":
        if not map_loaded:
            load_map("maps/lvl1.txt")
            map_loaded = True
        game_run_screen()
        if level:
            game_state = "LEVEL2"
            map_loaded = False
            key_made = False
            gotkey = False
            ui_open = False
            level = False
            for sprite in all_sprites:
                sprite.kill()
            for tile in tile_sprites:
                tile.kill()
            for key in keys:
                key.kill()

    if game_state == "LEVEL2":
        if not map_loaded:
            load_map("maps/lvl2.txt")
            map_loaded = True
        game_run_screen()
        if level:
            game_state = "WIN"

    elif game_state == "PAUSE":
        pass

    elif game_state == "START":
        start()

    elif game_state == "WIN":
        win()

    elif game_state == "DEAD":
        game_over()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()