import pygame
from debug import debug
import sys
from Player import Player
from network import Network
from bullet import Bullet
import csv
import map_reader
print(sys.version)
#network stuff
network = Network()
player1interim = network.getP()
player1 = Player(player1interim.health,player1interim.ammo,player1interim.cooldown,player1interim.bullet_interim_list,player1interim.vertical_velocity,player1interim.is_in_air,player1interim.can_jump,player1interim.is_alive,player1interim.update_timer,player1interim.player_type,player1interim.players_action,player1interim.action_number,player1interim.flip,player1interim.x,player1interim.y)

#pygame stuff
pygame.init()

# SCREEN_WIDTH = 800
# SCREEN_HEIGHT = 650
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Decimation")
game_is_running = True
FPS_of_game = 144
clock = pygame.time.Clock()


player_is_moving_left = False
player_is_moving_right = False

# bullet shooting
bullet_group_player1 = pygame.sprite.Group()
bullet_group_player2 = pygame.sprite.Group()

# loading map stuff
NUM_OF_TILES = 160
ROWS = 34
COLUMNS = 60
TILE_SIZE = 32
TILE_HEIGHT = SCREEN_HEIGHT // ROWS
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
            map_data[i][j] = int(col)
# load all images  into the image list
map_tile_images = []
for i in range(NUM_OF_TILES):
    img = pygame.image.load('tiles/0 (' + str(i)+').png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
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
            image_rect.x = j * 32
            image_rect.y = i * 32
            tup = (image,image_rect)
            if (col>=5 and col <=10) or(col == 16) or (col == 20) or (col>=23 and col <=26) or (col>=23 and col <=26)or (col==32)or (col>=35 and col <=37)or (col==39) or (col>=48 and col <=49) or (col == 52) or (col>=54 and col <=57)or (col>=65 and col <=66) or (col == 68) or (col>=70 and col <=71) or (col>=80 and col <=95) or (col>=97 and col <=103) or (col == 106) or (col>=129 and col <=131) or col ==133 or(col == 122) or col == 124 or col ==126 or (col==141) or (col ==143):
                obstacle_list_of_tuples.append(tup)
            if (col == 20) or (col>=23 and col <=25) or (col>=23 and col <=26)  or (col == 52) or (col == 68) or (col>=83 and col <=85) or (col>=129 and col <=131) or col ==133:
                collidable_objects.append(tup)



crosshair = pygame.image.load('crosshair.png').convert_alpha()
scaled_crosshair = pygame.transform.scale(crosshair,(30,30))
crosshair_rect = scaled_crosshair.get_rect()
while game_is_running:
    clock.tick(FPS_of_game)
    screen.fill((100,100,200))
    # draw background
    background = pygame.image.load('Background/single_background.png').convert_alpha()
    scaled_background = pygame.transform.scale(background,(SCREEN_WIDTH,SCREEN_HEIGHT))
    screen.blit(scaled_background,(0,0))
    # map_reader.draw(obstacle_list_of_tuples,screen)
    for element in obstacle_list_of_tuples:
        screen.blit(element[0],element[1])
    # draw cross hair
    pygame.mouse.set_visible(False)
    mouse_position = pygame.mouse.get_pos()
    crosshair_rect.center = mouse_position
    screen.blit(scaled_crosshair,crosshair_rect)

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
    player2 = Player(player2interim.health,player2interim.ammo,player2interim.cooldown,player2interim.bullet_interim_list,player2interim.vertical_velocity,player2interim.is_in_air,player2interim.can_jump,player2interim.is_alive,player2interim.update_timer,player2interim.player_type,player2interim.players_action,player2interim.action_number,player2interim.flip,player2interim.x,player2interim.y)
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
    player1.draw_health_bar('PLAYER',200,40)
    player1.draw_ammo('PLAYER',200,80)
    bullet_group_player2.draw(screen)
    bullet_group_player2.update(collidable_objects)
    player2.draw(screen)
    player2.draw_health_bar('ENEMY',1515,40)
    player2.draw_ammo('ENEMY',1515,80)
    # debug(player1.health,100,10)
    # debug(player2.health,100,30)
    # debug(player1.ammo,200,10)
    # debug(player2.ammo,200,30)
    if len(player1.bullet_interim_list) >= 1:
        player1.bullet_interim_list.pop(0)
    # player2.move(player_is_moving_right,player_is_moving_left)
    pygame.display.update()
pygame.quit()


