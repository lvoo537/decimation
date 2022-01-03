import pygame
from Player import Player
class PlayerInterim():

    def __init__(self,health,ammo,cooldown,bullet_interim_list:list,vertical_velocity,is_in_air,can_jump,is_alive,update_timer,player_type,players_action,action_number,flip,x,y):
        self.health = health
        self.ammo = ammo
        self.bullet_interim_list = bullet_interim_list
        self.vertical_velocity = vertical_velocity
        self.is_in_air = is_in_air
        self.can_jump = can_jump
        self.is_alive = is_alive
        self.update_timer = update_timer
        self.flip = flip
        self.action_number = action_number
        self.player_type = player_type
        self.players_action = players_action
        self.x = x
        self.y = y
        self.cooldown = cooldown

    def copy(self, p: Player):
        self.health = p.health
        self.ammo = p.ammo
        self.bullet_interim_list = p.bullet_interim_list.copy()
        self.vertical_velocity = p.vertical_velocity
        self.is_in_air = p.is_in_air
        self.can_jump = p.can_jump
        self.is_alive = p.is_alive
        self.update_timer = p.update_timer
        self.flip = p.flip
        self.action_number = p.action_number
        self.player_type = p.player_type
        self.players_action = p.players_action
        self.x = p.rect.centerx
        self.y = p.rect.centery
        self.cooldown = p.cooldown

