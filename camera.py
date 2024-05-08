import pygame
import math

screen_width = 1920
screen_height = 1080

pygame.init()

pos_x, pos_y = 200, 1000
enemy_x, enemy_y = 800, 420
enemy2_x, enemy2_y = 400, 420
heal_x, heal_y= 2000, 450
round_heal_x, round_heal_y = 2200, 450
box_x, box_y = 2200, 900
box2_x, box2_y = 2200, 900
hay_x, hay_y = 1000, 500
inv_x, inv_y = 200, 200

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
inventory = 0
can_attack_hay = False  # Initialize the variable to Fals
hay_cooldown = 0 # Timer for enemy attack in milliseconds
cursor_setting = -1

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Noctrium - Fighter')

pygame.mouse.set_visible(False)

font = pygame.font.Font('data/fonts/anonymous.ttf', 40)

clock = pygame.time.Clock()

# Load the images
player_stand = pygame.image.load('data/images/player.png').convert_alpha()
player_stand = pygame.transform.scale(player_stand, (95, 90))

#add-ons
sword_image = pygame.image.load('data/images/knife.png').convert_alpha()  
sword_image = pygame.transform.scale(sword_image, (60, 50))  # Adjust size as needed

inv1_image = pygame.image.load('data/images/inv1.png').convert_alpha()
inv1_image = pygame.transform.scale(inv1_image, (100, 100))

cursor_image_white = pygame.image.load('data/images/cursor_white.png').convert_alpha()
cursor_image_white = pygame.transform.scale(cursor_image_white, (40, 40))
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

correct_right_joystick_x_axis_index = 0  # Replace with the correct X-axis index
correct_right_joystick_y_axis_index = 1  

# playerz
def draw_player():
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
    

def inventorys():
    nubs = True
    keys = pygame.key.get_pressed()
    if nubs == True and keys[pygame.K_i]:
        screen.blit(inv1_image, (inv_x, inv_y))

coins = 0
running = True

while running:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_c]:
        running = False

    #screen.blit(bg_image, (0, 0))
    #rects

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
    
    if hay_cooldown > 0:
        hay_cooldown -= clock.get_time()

    if hay_cooldown > 0:
        hay_cooldown -= clock.get_time()

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
    # If hay's HP reaches 0, hide it and start the cooldown
    if HayHP <= 0:
        hay_x = -1000  # Move hay off-screen (you can adjust this value as needed)
        hay_y = -1000
        hay_cooldown = 10000  # Set the cooldown to 10 seconds (10000 milliseconds)
    # If the cooldown has elapsed, bring hay back to the screen
    if hay_cooldown <= 0:
        hay_x = 1000  # Adjust these values to position hay back on-screen
        hay_y = 500

    
    
    mouse_pos = pygame.mouse.get_pos()

    screen.fill((52, 52, 52))

    screen.blit(cursor_image_white, mouse_pos)

    inventorys()

    draw_player()

    print(clock.get_fps())
    pygame.display.flip()
    clock.tick(60)

pygame.quit()