import pygame
import math

screen_width = 1920
screen_height = 1080

def show_splash_screen():
    splash_font = pygame.font.SysFont('Sans-Serif', 50)
    splash_text = splash_font.render('Welcome to Platon!', True, (255, 255, 255))

    # Initial position of the splash text
    text_x = screen_width / 2 - 200
    text_y = screen_height / 2 - 50

    start_time = pygame.time.get_ticks()  # Get the start time

    while pygame.time.get_ticks() - start_time < 2000:  # Display for 2 seconds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill((0, 0, 0))
        screen.blit(splash_text, (text_x, text_y))
        pygame.display.flip()

        # Update the position of the text to create the floating effect
        text_y += math.sin(pygame.time.get_ticks() * 0.01) * 2  # Adjust the values for desired movement

        pygame.time.Clock().tick(60)

    show_main_menu()

def show_main_menu():
    global running
    menu_font = pygame.font.SysFont('Sans-Serif', 36)
    menu_options = ['Play', 'Shop', 'Quit']
    selected_option = 0
    fruning = True
    while fruning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        # Start the game
                        fruning = False
                    elif selected_option == 1:
                        # Show options
                        pass
                    elif selected_option == 2:
                        pygame.quit()
                        
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
        screen.fill((0, 0, 0))

        for i, option in enumerate(menu_options):
            color = (255, 255, 255) if i == selected_option else (150, 150, 150)
            text = menu_font.render(option, True, color)
            text_rect = text.get_rect(center=(screen.get_width() // 2, 200 + i * 80))
            screen.blit(text, text_rect)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

pygame.init()


pos_x, pos_y = 200, 1000
enemy_x, enemy_y = 800, 420
enemy2_x, enemy2_y = 400, 420
heal_x, heal_y= 2000, 450
round_heal_x, round_heal_y = 2200, 450
box_x, box_y = 2200, 900
box2_x, box2_y = 2200, 900
hay_x, hay_y = 1000, 500

distance_threshold = 100
playerHP = 100
enemyHP = 100
HayHP = 100
attack_cooldown = 0  # Timer in milliseconds
attack_enemy_cooldown = 0  # Timer for enemy attack in milliseconds
roundHP = 0
kills = 0
heal_cooldown = 0  # Timer in milliseconds
attack_hay_cooldown = 0 # Timer for enemy attack in milliseconds
can_attack_hay = False  # Initialize the variable to False

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Hello World')

font = pygame.font.Font('data/fonts/anonymous.ttf', 40)

clock = pygame.time.Clock()

# Load the images
player_stand = pygame.image.load('data/images/player.png').convert_alpha()
player_stand = pygame.transform.scale(player_stand, (95, 90))

enemy_stand = pygame.image.load('data/images/enemy_stand.png').convert_alpha()  
enemy_stand = pygame.transform.scale(enemy_stand, (95, 90))
#add-ons
sword_image = pygame.image.load('data/images/knife.png').convert_alpha()  
sword_image = pygame.transform.scale(sword_image, (60, 50))  # Adjust size as needed

hay_image = pygame.image.load('data/images/hay.png').convert_alpha()
hay_image = pygame.transform.scale(hay_image, (60, 50)) 

bg_image = pygame.image.load('data/images/bg.png').convert_alpha()
bg_image = pygame.transform.scale(bg_image, (1920, 1080))

#distance
def distance_between_points(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def calculate_distance(point1, point2):
    return pygame.math.Vector2(point2[0] - point1[0], point2[1] - point1[1]).length()

def draw_sword():
    # Position the sword relative to the player's position
    sword_x = pos_x + 61  # Adjust the x-coordinate as needed to position the sword correctly
    sword_y = pos_y + 30  # Adjust the y-coordinate as needed to position the sword correctly

    # Draw the sword
    screen.blit(sword_image, (sword_x, sword_y))
def draw_hay():
    screen.blit(hay_image, (hay_x, hay_y))
def draw_enemy_sword():
        # Position the sword relative to the player's position
    sword_x = enemy_x + 61  # Adjust the x-coordinate as needed to position the sword correctly
    sword_y = enemy_y + 30  # Adjust the y-coordinate as needed to position the sword correctly

    # Draw the sword
    screen.blit(sword_image, (sword_x, sword_y))
def draw_name_player(player_x, player_y):
    playername = font.render('Numbis', False, (255, 255, 255))
    # Calculate the position for the player's name to appear above the head
    name_x = player_x + (player_stand.get_width() - playername.get_width()) // 2
    name_y = player_y - playername.get_height()
    screen.blit(playername, (name_x, name_y))

def name_enemy(enemy_x, enemy_y):
    enemyname = font.render('Prixie', False, (255, 255, 255))
    # Calculate the position for the enemy's name to appear above the head
    name_x = enemy_x + (enemy_stand.get_width() - enemyname.get_width()) // 2
    name_y = enemy_y - enemyname.get_height()
    screen.blit(enemyname, (name_x, name_y))

correct_right_joystick_x_axis_index = 0  # Replace with the correct X-axis index
correct_right_joystick_y_axis_index = 1  
# playerz
def player():
    global moving_rect, pos_x, pos_y, heal_cooldown, playerHP
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
    draw_name_player(pos_x, pos_y)
# enemy
def enemy():
    global enemy_x, enemy_y

    # Move the enemy towards the player at a constant speed
    if enemy_x > pos_x:
        enemy_x -= 1.5
    elif enemy_x < pos_x:
        enemy_x += 1.5

    if enemy_y > pos_y:  # Separate condition for moving down
        enemy_y -= 1.5
    elif enemy_y < pos_y:  # Separate condition for moving up
        enemy_y += 1.5
    
    current_enemy_image = enemy_stand
    # Draw the enemy
    screen.blit(current_enemy_image, (enemy_x, enemy_y))
    draw_enemy_sword()  # Draw the sword for the enemy as well
    name_enemy(enemy_x, enemy_y)

'''
def enemy2():
    global enemy2_x, enemy2_y
    #pygame.draw.rect(screen, (255, 51, 51), enemy_rect)

    # Move the enemy towards the player at a constant speed
    if enemy2_x > pos_x:
        enemy2_x -= 1.5
    elif enemy2_x < pos_x:
        enemy2_x += 1.5
    elif enemy2_y >= pos_y:
        enemy2_y -= 1.5
    elif enemy2_y <= pos_y:
        enemy2_y += 1.5
    current_enemy_image = enemy_stand
    # Draw the player
    screen.blit(current_enemy_image, (enemy2_x, enemy2_y))
'''
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
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
                #print('Attacking the enemy!')
                enemyHP -= 15
                attack_enemy_cooldown = 1500
        if keys[pygame.K_1]:
            #print('Attacking the enemy!')
            enemyHP -= 15
            attack_enemy_cooldown = 1500
def attack_hay():
    global HayHP, attack_hay_cooldown
    keys = pygame.key.get_pressed()
    dist = distance_between_points(pos_x, pos_y, hay_x, hay_y)

    if dist <= distance_threshold and attack_hay_cooldown <= 0:
    # Check for mouse events
        mouse_buttons = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        if mouse_buttons[2]:
        #print('Attacking the hay!')
            HayHP -= 15
            attack_hay_cooldown = 2000
        if keys[pygame.K_2]:
            #print('Attacking the hay!')
            HayHP -= 15
            attack_hay_cooldown = 2000
def draw_hp_text_above_hay(player_pos, hay_pos):
    global hp_text, can_attack_hay, attack_hay_cooldown, HayHP
    distance_to_hay = calculate_distance(player_pos, hay_pos)
    if distance_to_hay < 100:
        hp_text = font.render(f"HP: {HayHP}", True, (255, 255, 255))
        text_x = hay_pos[0] - hp_text.get_width() // 2
        text_y = hay_pos[1] - 50
        screen.blit(hp_text, (text_x, text_y))

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
    kills_text = font.render(f'Kills / Coins: {kills}', False, (255, 255, 255))
    screen.blit(kills_text, (10, 100))
show_splash_screen()
coins = 0
running = True
while running:
    global can
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False 
    #screen.blit(bg_image, (0, 0))
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

    if attack_hay_cooldown > 0:
        attack_hay_cooldown -= clock.get_time()

    # If player is dead, pos_x and pos_y are reset to pos_x = 200 and pos_y = 440
    if playerHP < 0:
        pos_x = 200
        pos_y = 420
        enemy_x = 800
        enemy_y = 420
        playerHP = 100
        coins -= 5
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
        heal_x = 2200
    if moving_rect.colliderect(round_rect):
        playerHP += 50
        round_heal_x = 2200
        roundHP = 0
    
    attack_player()
    attack_enemy()
    attack_hay()

    screen.fill((52, 52, 52))
    draw_player_hp()
    draw_enemy_hp()
    draw_round_hp()
    draw_kills()
    draw_hay()
    draw_hp_text_above_hay((pos_x, pos_y), (hay_x, hay_y))

    player()
    enemy()
    #enemy2()
    heal_player()
    round_heal()
    #print(clock.get_fps())
    pygame.display.flip()
    clock.tick(60)

pygame.quit()