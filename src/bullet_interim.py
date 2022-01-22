import pygame
from bullet import Bullet


class BulletInterim:
    def __init__(self,x,y,targetx,targety):
        self.x = x
        self.y = y
        self.targetx = targetx
        self.targety =targety

    def copy(self,b:Bullet):
        self.x = b.rect.centerx
        self.y = b.rect.centery
        self.targetx = b.targetx
        self.targety = b.targety
