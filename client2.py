import pygame
from debug import debug
import sys
from Player import Player
from network import Network
from bullet import Bullet
print(sys.version)
#network stuff
network = Network()
player1interim = network.getP()
player1 = Player(player1interim.health,player1interim.ammo,player1interim.cooldown,player1interim.bullet_interim_list,player1interim.vertical_velocity,player1interim.is_in_air,player1interim.can_jump,player1interim.is_alive,player1interim.update_timer,player1interim.player_type,player1interim.players_action,player1interim.action_number,player1interim.flip,player1interim.x,player1interim.y)

#pygame stuff
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 650
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Decimation")
game_is_running = True
FPS_of_game = 60
clock = pygame.time.Clock()


player_is_moving_left = False
player_is_moving_right = False

#bullet shooting
bullet_group_player1 = pygame.sprite.Group()
bullet_group_player2 = pygame.sprite.Group()


while game_is_running:
    clock.tick(FPS_of_game)
    screen.fill((100,100,200))

    for event in pygame.event.get():
        if event.type == pygame.QUIT or(event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            game_is_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player_is_moving_left = True
            if event.key == pygame.K_w and player1.is_alive:
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
        player1.move(player_is_moving_right,player_is_moving_left)
    if player1.is_alive:
        player1.shoot()
    player1.update_cooldown()

    # debug(player1.rect.bottom,10,30)
    # debug(pygame.mouse.get_pos(),10,50)

    player1interim.copy(player1)S


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
    bullet_group_player1.update()
    player1.draw(screen)
    bullet_group_player2.draw(screen)
    bullet_group_player2.update()
    player2.draw(screen)
    debug(player1.health,100,10)
    debug(player2.health,100,30)
    debug(player1.ammo,200,10)
    debug(player2.ammo,200,30)
    if len(player1.bullet_interim_list) >= 1:
        player1.bullet_interim_list.pop(0)
    # player2.move(player_is_moving_right,player_is_moving_left)
    pygame.display.update()
pygame.quit()


