import pygame
import math

pygame.init()
pos_x, pos_y = 200, 420
enemy_x, enemy_y = 800, 420
heal_x, heal_y = 1200, 450
round_heal_x, round_heal_y = 1400, 450

distance_threshold = 100
playerHP = 100
enemyHP = 100
attack_cooldown = 0  # Timer in milliseconds
attack_enemy_cooldown = 0  # Timer for enemy attack in milliseconds
roundHP = 0
kills = 0

screen = pygame.display.set_mode((1000, 500))
pygame.display.set_caption('Hello World')

font = pygame.font.SysFont('Sans-Serif', 40)

clock = pygame.time.Clock()

# Load the images
player_stand = pygame.image.load('data/images/player_stand.png')
player_stand = pygame.transform.scale(player_stand, (95, 90))

enemy_stand = pygame.image.load('data/images/enemy_stand.png')
enemy_stand = pygame.transform.scale(enemy_stand, (95, 90))

sword_image = pygame.image.load('data/images/knife_stand.png')
sword_image = pygame.transform.scale(sword_image, (60, 50))  # Adjust size as needed

# Distance
def distance_between_points(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Sword animation variables
sword_swinging = False
swing_angle = 0

def draw_sword():
    global sword_swinging, swing_angle
    # Position the sword relative to the player's position
    sword_x = pos_x + 70  # Adjust the x-coordinate as needed to position the sword correctly
    sword_y = pos_y + 30  # Adjust the y-coordinate as needed to position the sword correctly

    if sword_swinging:
        # Rotate the sword image based on the swinging angle
        rotated_sword = pygame.transform.rotate(sword_image, swing_angle)
        screen.blit(rotated_sword, (sword_x, sword_y))
        # Increment the swinging angle (adjust the angle increment as needed)
        swing_angle = (swing_angle + 10) % 360
    else:
        # If not swinging, draw the default standing knife frame
        screen.blit(sword_image, (sword_x, sword_y))

# Player
def player():
    global moving_rect, pos_x, pos_y, sword_swinging
    #pygame.draw.rect(screen, (51, 51, 255), moving_rect)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        pos_x -= 10
    if keys[pygame.K_RIGHT]:
        pos_x += 10

    if pos_x < 0:
        pos_x = 0
    if pos_x > 950:
        pos_x = 950
    if pos_y < 0:
        pos_y = 0
    if pos_y > 500:
        pos_y = 500
        
    current_image = player_stand
    # Draw the player
    screen.blit(current_image, (pos_x, pos_y))
    draw_sword()

# Enemy
def enemy():
    global enemy_x, enemy_y
    #pygame.draw.rect(screen, (255, 51, 51), enemy_rect)

    # Move the enemy towards the player at a constant speed
    if enemy_x > pos_x:
        enemy_x -= 1
    elif enemy_x < pos_x:
        enemy_x += 1

    current_enemy_image = enemy_stand
    # Draw the enemy
    screen.blit(current_enemy_image, (enemy_x, enemy_y))

def heal_player():
    global heal_x, heal_y
    pygame.draw.rect(screen, (255, 255, 255), heal_rect)

def round_heal():
    global round_heal_x, round_heal_y
    pygame.draw.rect(screen, (0, 156, 73), round_rect)

# Attacking the player
def attack_player():
    global playerHP, attack_cooldown
    dist = distance_between_points(pos_x, pos_y, enemy_x, enemy_y)

    if dist <= distance_threshold and attack_cooldown <= 0:
        #print("Attacking the player!")
        playerHP -= 7
        attack_cooldown = 2000

# Attacking the enemy
def attack_enemy():
    global enemyHP, attack_enemy_cooldown, sword_swinging
    keys = pygame.key.get_pressed()
    dist = distance_between_points(pos_x, pos_y, enemy_x, enemy_y)

    if dist <= distance_threshold and attack_enemy_cooldown <= 0:
        # Check for mouse events
        if keys[pygame.K_1]:
            #print('Attacking the enemy!')
            enemyHP -= 15
            attack_enemy_cooldown = 1500
            sword_swinging = True
        else:
            sword_swinging = False

# Drawings
def draw_player_hp():
    player_hp_text = font.render(f'Numbis HP: {playerHP}', False, (255, 255, 255))
    screen.blit(player_hp_text, (10, 10))

def draw_enemy_hp():
    enemy_hp_text = font.render(f'Prixie HP: {enemyHP}', False, (255, 255, 255))
    screen.blit(enemy_hp_text, (10, 40))

def draw_round_hp():
    round_text = font.render(f'Rounds: {roundHP}', False, (255, 255, 255))
    screen.blit(round_text, (10, 70))

def draw_kills():
    kills_text = font.render(f'Kills: {kills}', False, (255, 255, 255))
    screen.blit(kills_text, (10, 100))

running = True
while running:
    # Rects
    moving_rect = pygame.Rect(pos_x, pos_y, 55, 50)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, 55, 50)
    heal_rect = pygame.Rect(heal_x, heal_y, 35, 30)
    round_rect = pygame.Rect(round_heal_x, round_heal_y, 35, 30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Updating attack cooldown
    if attack_cooldown > 0:
        attack_cooldown -= clock.get_time()

    if attack_enemy_cooldown > 0:
        attack_enemy_cooldown -= clock.get_time()

    # If player is dead, pos_x and pos_y are reset to pos_x = 200 and pos_y = 420
    if playerHP < 0:
        pos_x = 200
        pos_y = 420
        enemy_x = 800
        enemy_y = 420
        playerHP = 100

    if enemyHP <= 0:
        enemy_x = 800
        enemy_y = 420
        enemyHP = 100
        heal_x = 200
        roundHP += 1
        kills += 1

    if moving_rect.colliderect(heal_rect):
        playerHP += 30
        heal_x = 1200

    if roundHP == 3:
        round_heal_x = 200
        heal_x = 1200

    if moving_rect.colliderect(round_rect):
        playerHP += 50
        round_heal_x = 1400
        roundHP = 0

    attack_player()
    attack_enemy()

    screen.fill((52, 52, 52))
    draw_player_hp()
    draw_enemy_hp()
    draw_round_hp()
    draw_kills()

    player()
    enemy()
    heal_player()
    round_heal()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
