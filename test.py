import pygame
import math
'''
def show_splash_screen():
    splash_font = pygame.font.SysFont('Sans-Serif', 50)
    splash_text = splash_font.render('Welcome to Platon!', True, (255, 255, 255))

    # Initial position of the splash text
    text_x = 350
    text_y = 250

    start_time = pygame.time.get_ticks()  # Get the start time

    while pygame.time.get_ticks() - start_time < 2000:  # Display for 2 seconds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    
        screen.fill((0, 0, 0))
        screen.blit(splash_text, (text_x, text_y))
        pygame.display.flip()

        # Update the position of the text to create the floating effect
        text_y += math.sin(pygame.time.get_ticks() * 0.01) * 2  # Adjust the values for desired movement

        pygame.time.Clock().tick(60)
'''
pygame.init()
pos_x, pos_y = 200, 1000
enemy_x, enemy_y = 800, 420
heal_x, heal_y = 2000, 450
round_heal_x, round_heal_y = 2200, 450
box_x, box_y = 500, 400
box2_x, box2_y = 900, 450

distance_threshold = 100
playerHP = 100
enemyHP = 100
attack_cooldown = 0  # Timer in milliseconds
attack_enemy_cooldown = 0  # Timer for enemy attack in milliseconds
roundHP = 0
kills = 0

screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption('Hello World')

font = pygame.font.SysFont('Sans-Serif', 40)

clock = pygame.time.Clock()

# Load the images
player_stand = pygame.image.load('data/images/player_stand.png').convert_alpha()
player_stand = pygame.transform.scale(player_stand, (95, 90))

enemy_stand = pygame.image.load('data/images/enemy_stand.png').convert_alpha()  
enemy_stand = pygame.transform.scale(enemy_stand, (95, 90))

sword_image = pygame.image.load('data/images/knife.png').convert_alpha()  
sword_image = pygame.transform.scale(sword_image, (60, 50))  # Adjust size as needed

bg_image = pygame.image.load('data/images/bg.png').convert_alpha()
bg_image = pygame.transform.scale(bg_image, (1920, 1080))

#distance
def distance_between_points(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def draw_sword():
    # Position the sword relative to the player's position
    sword_x = pos_x + 61  # Adjust the x-coordinate as needed to position the sword correctly
    sword_y = pos_y + 30  # Adjust the y-coordinate as needed to position the sword correctly

    # Draw the sword
    screen.blit(sword_image, (sword_x, sword_y))

# playerz
def player():
    global moving_rect, pos_x, pos_y
    #pygame.draw.rect(screen, (51, 51, 255), moving_rect)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        pos_x -= 10
    if keys[pygame.K_RIGHT]:
        pos_x += 10
    if keys[pygame.K_UP]:
        pos_y -= 10
    if keys[pygame.K_DOWN]:
        pos_y += 10
    if keys[pygame.K_a]:
        pos_x -= 10
    if keys[pygame.K_d]:
        pos_x += 10
    if keys[pygame.K_w]:
        pos_y -= 10
    if keys[pygame.K_s]:
        pos_y += 10
    if pos_x < -15:
        pos_x = -15
    if pos_x > 1840:
        pos_x = 1840
    if pos_y < -15:
        pos_y = -15
    if pos_y > 1000:
        pos_y = 1000
        
    current_image = player_stand
    # Draw the player
    screen.blit(current_image, (pos_x, pos_y))
    draw_sword()
# enemy
def enemy():
    global enemy_x, enemy_y
    #pygame.draw.rect(screen, (255, 51, 51), enemy_rect)

    # Move the enemy towards the player at a constant speed
    if enemy_x > pos_x:
        enemy_x -= 1
    elif enemy_x < pos_x:
        enemy_x += 1
    elif enemy_y >= pos_y:
        enemy_y -= 1
    elif enemy_y <= pos_y:
        enemy_y += 1
    current_enemy_image = enemy_stand
    # Draw the player
    screen.blit(current_enemy_image, (enemy_x, enemy_y))

def boxrects():
    global box_x, box_y, box2_x, box2_y
    pygame.draw.rect(screen, (255, 255, 255), box1_rect)
    pygame.draw.rect(screen, (0, 156, 73), box2_rect)
def heal_player():
    global heal_x, heal_y
    pygame.draw.rect(screen, (255, 255, 255), heal_rect)

def round_heal():
    global round_heal_x, round_heal_y
    pygame.draw.rect(screen, (0, 156, 73), round_rect)
# attacking the player
def attack_player():
    global playerHP, attack_cooldown
    dist = distance_between_points(pos_x, pos_y, enemy_x, enemy_y)

    if dist <= distance_threshold and attack_cooldown <= 0:
        #print("Attacking the player!")
        playerHP -= 7
        attack_cooldown = 2000
# attacking the enemy
def attack_enemy():
    global enemyHP, attack_enemy_cooldown
    keys = pygame.key.get_pressed()
    dist = distance_between_points(pos_x, pos_y, enemy_x, enemy_y)

    if dist <= distance_threshold and attack_enemy_cooldown <= 0:
        # Check for mouse events
        #if keys[pygame.K_1]:
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
                #print('Attacking the enemy!')
                enemyHP -= 15
                attack_enemy_cooldown = 1500
        if keys[pygame.K_1]:
            #print('Attacking the enemy!')
            enemyHP -= 15
            attack_enemy_cooldown = 1500
# drawings
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

#show_splash_screen()
running = True
while running:
    screen.blit(bg_image, (0, 0))
    #rects
    moving_rect = pygame.Rect(pos_x, pos_y, 55, 50)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, 55, 50)
    heal_rect = pygame.Rect(heal_x, heal_y, 35, 30)
    round_rect = pygame.Rect(round_heal_x, round_heal_y, 35, 30)
    box1_rect = pygame.Rect(box_x, box_y, 100, 30)
    box2_rect = pygame.Rect(box2_x, box2_y, 100, 30)
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
        heal_x = 2000
    if roundHP == 3:
        round_heal_x = 200
        heal_x = 1200
    if moving_rect.colliderect(round_rect):
        playerHP += 50
        round_heal_x = 2200
        roundHP = 0
    attack_player()
    attack_enemy()
    

    screen.fill((52, 52, 52))
    draw_player_hp()
    draw_enemy_hp()
    draw_round_hp()
    draw_kills()
    boxrects()
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
    #print(clock.get_fps())
    pygame.display.flip()
    clock.tick(60)

pygame.quit()