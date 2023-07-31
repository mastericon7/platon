import pygame

pygame.init()
pos_x, pos_y = 200, 440
enemy_x, enemy_y = 800, 440

screen = pygame.display.set_mode((1000, 500))
pygame.display.set_caption('Hello World')

font = pygame.font.SysFont('Sans-Serif', 40)

clock = pygame.time.Clock()
def player():
    global moving_rect, pos_x, pos_y
    pygame.draw.rect(screen, (51, 51, 255), moving_rect)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        pos_x -= 10
    if keys[pygame.K_RIGHT]:
        pos_x += 10
    if keys[pygame.K_UP]:
        pos_y -= 10
    if keys[pygame.K_DOWN]:
        pos_y += 10
    if pos_x < 0:
        pos_x = 0
    if pos_x > 950:
        pos_x = 950
    if pos_y < 0:
        pos_y = 0
    if pos_y > 500:
        pos_y = 500
    moving_rect = pygame.Rect(pos_x,pos_y,55,50)
def enemy():
    pygame.draw.rect(screen, (255, 51, 51), enemy_rect)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            #pygame.quit()
    screen.fill((52, 52, 52))
    playername = font.render('Numbis', False, (255, 255, 255))
    screen.blit(playername, (180, 390))
    enemyname = font.render('Prixie', False, (255, 255, 255))
    screen.blit(enemyname, (790, 390))
    moving_rect = pygame.Rect(pos_x,pos_y,55,50)
    enemy_rect = pygame.Rect(enemy_x,enemy_y,55,50)
    player()
    enemy()
    pygame.display.flip()
    clock.tick(60)