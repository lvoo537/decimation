import pygame

import sys
from Player import Player
from network import Network
from bullet import Bullet
import csv
import time
import map_reader
print(sys.version)
#pygame stuff
pygame.init()

# SCREEN_WIDTH = 800
# SCREEN_HEIGHT = 650
# SCREEN_WIDTH = 1920
# SCREEN_HEIGHT = 1080
display_surface = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
SCREEN_HEIGHT = display_surface.get_height()
SCREEN_WIDTH = display_surface.get_width()
screen = pygame.Surface((1920,1080))

pygame.display.set_caption("Decimation")
game_is_running = True
FPS_of_game = 144
clock = pygame.time.Clock()


player_is_moving_left = False
player_is_moving_right = False

#network stuff
network = Network()
player1interim = network.getP()
while player1interim == None:
    network.connect()
    player1interim = network.getP()
player1 = Player(screen,player1interim.health,player1interim.ammo,player1interim.cooldown,player1interim.bullet_interim_list,player1interim.vertical_velocity,player1interim.is_in_air,player1interim.can_jump,player1interim.is_alive,player1interim.update_timer,player1interim.player_type,player1interim.players_action,player1interim.action_number,player1interim.flip,player1interim.x,player1interim.y)



# bullet shooting
bullet_group_player1 = pygame.sprite.Group()
bullet_group_player2 = pygame.sprite.Group()

# loading map stuff
NUM_OF_TILES = 160
ROWS = 34
COLUMNS = 60
TILE_SIZE = 32
TILE_HEIGHT = screen.get_height() / ROWS
print(screen.get_height())
TILE_WIDTH = screen.get_width() / COLUMNS
print(screen.get_width())
map_data = []
obstacle_list_of_tuples = []
# temporariliy fill map_data with -1's so we can fill it properly later
for i in range(ROWS):
    r = [-1] * COLUMNS
    map_data.append(r)
with open("icy_map2.csv", newline='') as csv_map:
    csv_reader_object = csv.reader(csv_map, delimiter=',')
    for i, row in enumerate(csv_reader_object):
        for j, col in enumerate(row):
            if i< ROWS and j < COLUMNS:
                map_data[i][j] = int(col)
# load all images  into the image list
map_tile_images = []
for i in range(NUM_OF_TILES):
    img = pygame.image.load('tiles/0 (' + str(i)+').png').convert_alpha()
    img = pygame.transform.scale(img, (int(TILE_WIDTH), int(TILE_HEIGHT)))
    map_tile_images.append(img)
collidable_objects = []
for i, row in enumerate(map_data):
    for j, col in enumerate(row):
        # skipping all the -1's in the map data
        if col >= 0:
            image = map_tile_images[col]
            height = image.get_height
            width = image.get_width
            image_rect = image.get_rect()
            image_rect.x = j * TILE_WIDTH
            image_rect.y = i * TILE_HEIGHT
            tup = (image,image_rect)
            if (col>=5 and col <=10) or(col == 16) or (col == 20) or (col>=23 and col <=26) or (col>=23 and col <=26)or (col==32)or (col>=35 and col <=37)or (col==39) or (col>=48 and col <=49) or (col == 52) or (col>=54 and col <=57)or (col>=65 and col <=66) or (col == 68) or (col>=70 and col <=71) or (col>=80 and col <=95) or (col>=97 and col <=103) or (col == 106) or (col>=129 and col <=131) or col ==133 or(col == 122) or col == 124 or col ==126 or (col==141) or (col ==143):
                obstacle_list_of_tuples.append(tup)
            if (col == 20) or (col>=23 and col <=25) or (col>=23 and col <=26)  or (col == 52) or (col == 68) or (col>=83 and col <=85) or (col>=129 and col <=131) or col ==133:
                collidable_objects.append(tup)



crosshair = pygame.image.load('crosshair.png').convert_alpha()
scaled_crosshair = pygame.transform.scale(crosshair,(30,30))
crosshair_rect = scaled_crosshair.get_rect()

#game over stuff
game_over_type = 0
def is_game_over(player1: Player,player2:Player):
    global game_over_type
    if (player1.players_action == 'Death' and player1.action_number == (len(player1.animation_types[player1.players_action]) -1)):
        game_over_type = 2
        return True
    elif (player2.players_action == 'Death' and player2.action_number == (len(player2.animation_types[player2.players_action]) -1)):
        game_over_type = 1
        return True
    elif player1.ammo == 0 and player2.ammo == 0:
        game_over_type = 3
        return True
    else:
        return False


def game_over_screen():
    current_time = time.time()
    run = True
    while time.time() - current_time <= 10 and run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or(event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False
        game_over_image = pygame.image.load('game_over.png').convert_alpha()
        scaled_game_over_image = pygame.transform.scale(game_over_image,(SCREEN_WIDTH,SCREEN_HEIGHT))
        # scaled_game_over_image_rect= scaled_game_over_image.get_rect()
        # scaled_game_over_image_rect.x = 0
        # scaled_game_over_image_rect.y = 0
        screen.blit(scaled_game_over_image,(0,0))
        pygame.display.update()


while game_is_running:
    clock.tick(FPS_of_game)
    screen.fill((100,100,200))
    # draw background
    background = pygame.image.load('Background/single_background.png').convert_alpha()
    scaled_background = pygame.transform.scale(background,(screen.get_width(),screen.get_height()))
    screen.blit(scaled_background,(0,0))
    # map_reader.draw(obstacle_list_of_tuples,screen)
    for element in obstacle_list_of_tuples:
        screen.blit(element[0],element[1])

    for event in pygame.event.get():
        if event.type == pygame.QUIT or(event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            game_is_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player_is_moving_left = True
            if event.key == pygame.K_w and player1.is_alive and not player1.is_in_air:
                player1.can_jump = True
            if event.key == pygame.K_d:
                player_is_moving_right = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player_is_moving_left = False
            if event.key == pygame.K_d:
                player_is_moving_right = False
    if player1.is_alive:
        if player1.is_in_air:
            player1.update_animation('Jump')
        elif player_is_moving_right or player_is_moving_left:
            player1.update_animation('Run')
        else:
            player1.update_animation('Idle')

    player1.animate()
    player1.is_alive_now()
    if player1.is_alive:
        player1.move(player_is_moving_right,player_is_moving_left,collidable_objects)

    if player1.is_alive:
        player1.shoot()
    player1.update_cooldown()

    # debug(player1.rect.bottom,10,30)
    # debug(pygame.mouse.get_pos(),10,50)

    player1interim.copy(player1)


    # player2interim = network.send(player1interim)
    data_to_send = (player1interim,player1interim.bullet_interim_list)
    data_from_server = network.send(data_to_send)


    player2interim = data_from_server[0]
    player2 = Player(screen,player2interim.health,player2interim.ammo,player2interim.cooldown,player2interim.bullet_interim_list,player2interim.vertical_velocity,player2interim.is_in_air,player2interim.can_jump,player2interim.is_alive,player2interim.update_timer,player2interim.player_type,player2interim.players_action,player2interim.action_number,player2interim.flip,player2interim.x,player2interim.y)
    # player2.animate()
    for bulletInterim in data_from_server[1]:
        bullet2 = Bullet(player1,player2,bullet_group_player1,bullet_group_player2,bulletInterim.x,bulletInterim.y,bulletInterim.targetx,bulletInterim.targety,screen)
        bullet_group_player2.add(bullet2)
    if len(player1.bullet_interim_list) >= 1:
        bullet = Bullet(player1,player2,bullet_group_player1,bullet_group_player2,player1.bullet_interim_list[0].x,player1.bullet_interim_list[0].y,player1.bullet_interim_list[0].targetx,player1.bullet_interim_list[0].targety,screen)
        bullet_group_player1.add(bullet)
    bullet_group_player1.draw(screen)
    bullet_group_player1.update(collidable_objects)
    player1.draw(screen)
    player1.draw_health_bar('PLAYER',220,30)
    player1.draw_ammo('PLAYER',220,60)
    bullet_group_player2.draw(screen)
    bullet_group_player2.update(collidable_objects)
    player2.draw(screen)
    player2.draw_health_bar('ENEMY',1500,30)
    player2.draw_ammo('ENEMY',1500,60)
    # debug(player1.health,100,10)
    # debug(player2.health,100,30)
    # debug(player1.ammo,200,10)
    # debug(player2.ammo,200,30)
    if len(player1.bullet_interim_list) >= 1:
        player1.bullet_interim_list.pop(0)
    # player2.move(player_is_moving_right,player_is_moving_left)
    # draw cross hair
    pygame.mouse.set_visible(False)
    mouse_position = pygame.mouse.get_pos()
    crosshair_rect.center = mouse_position
    screen.blit(scaled_crosshair,crosshair_rect)
    if is_game_over(player1,player2) and (not bullet_group_player1) and (not bullet_group_player2):
        font = pygame.font.SysFont('Futura',100)
        if game_over_type ==1:
            game_over_text = font.render('YOU '+ ' WIN!!!!!!!!',True,(255,255,255))
            screen.blit(game_over_text,(int(SCREEN_WIDTH/2)-300,int(SCREEN_HEIGHT/2)))
        elif game_over_type ==2:
            game_over_text = font.render('ENEMY '+ ' WINS :(',True,(255,255,255))
            screen.blit(game_over_text,(int(SCREEN_WIDTH/2)-300,int(SCREEN_HEIGHT/2)))
        else:
            game_over_text = font.render('IT IS A TIE!!!!!!',True,(255,255,255))
            screen.blit(game_over_text,(int(SCREEN_WIDTH/2)-300,int(SCREEN_HEIGHT/2)))
        pygame.display.update()
        time.sleep(3)
        game_over_screen()
        game_is_running = False

    # blit the surface to the screen
    pygame.transform.scale(screen,(int(SCREEN_WIDTH/1920) ,int( SCREEN_HEIGHT/1080)))
    display_surface.blit(screen,(0,0))
    pygame.display.update()


pygame.quit()



