import pygame
import math

pygame.init()
pos_x, pos_y = 200, 400
enemy_x, enemy_y = 800, 440
heal_x, heal_y = 1200, 450
round_heal_x, round_heal_y = 1400, 450

distance_threshold = 100
playerHP = 100
enemyHP = 100
attack_cooldown = 0  # Timer in milliseconds
attack_enemy_cooldown = 0  # Timer for enemy attack in milliseconds
roundHP = 0

screen = pygame.display.set_mode((1000, 500))
pygame.display.set_caption('Hello World')

font = pygame.font.SysFont('Sans-Serif', 40)

clock = pygame.time.Clock()

# Load the images
player_stand = pygame.image.load('data/images/player_stand.png')
player_stand = pygame.transform.scale(player_stand, (95, 90))

def distance_between_points(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def player():
    global moving_rect, pos_x, pos_y
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
def enemy():
    global enemy_x, enemy_y
    pygame.draw.rect(screen, (255, 51, 51), enemy_rect)

    # Move the enemy towards the player at a constant speed
    if enemy_x > pos_x:
        enemy_x -= 1
    elif enemy_x < pos_x:
        enemy_x += 1
def heal_player():
    global heal_x, heal_y
    pygame.draw.rect(screen, (255, 255, 255), heal_rect)

def round_heal():
    global round_heal_x, round_heal_y
    pygame.draw.rect(screen, (0, 156, 73), round_rect)

def attack_player():
    global playerHP, attack_cooldown
    dist = distance_between_points(pos_x, pos_y, enemy_x, enemy_y)

    if dist <= distance_threshold and attack_cooldown <= 0:
        #print("Attacking the player!")
        playerHP -= 7
        attack_cooldown = 2000

def attack_enemy():
    global enemyHP, attack_enemy_cooldown
    keys = pygame.key.get_pressed()
    dist = distance_between_points(pos_x, pos_y, enemy_x, enemy_y)

    if dist <= distance_threshold and attack_enemy_cooldown <= 0:
        # Check for mouse events
        if keys[pygame.K_1]:
                #print("Attacking the enemy!")
                enemyHP -= 15
                attack_enemy_cooldown = 1500

def draw_player_hp():
    player_hp_text = font.render(f'Numbis HP: {playerHP}', False, (255, 255, 255))
    screen.blit(player_hp_text, (10, 10))

def draw_enemy_hp():
    enemy_hp_text = font.render(f'Prixie HP: {enemyHP}', False, (255, 255, 255))
    screen.blit(enemy_hp_text, (10, 40))

def draw_round_hp():
    round_hp_text = font.render(f'Rounds: {roundHP}', False, (255, 255, 255))
    screen.blit(round_hp_text, (10, 70))
running = True
while running:
    #rects
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

    # If player is dead, pos_x and pos_y are reset to pos_x = 200 and pos_y = 440
    if playerHP < 0:
        pos_x = 200
        pos_y = 440
        enemy_x = 800
        enemy_y = 440
        playerHP = 100
    if enemyHP <= 0:
        enemy_x = 800
        enemy_y = 440
        enemyHP = 100
        heal_x = 200
        roundHP += 1
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
    '''
    playername = font.render('Numbis', False, (255, 255, 255))
    screen.blit(playername, (180, 390))
    
    enemyname = font.render('Prixie', False, (255, 255, 255))
    screen.blit(enemyname, (790, 390))
    '''

    player()
    enemy()
    heal_player()
    round_heal()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()