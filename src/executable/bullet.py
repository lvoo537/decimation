import pygame
import math
class Bullet(pygame.sprite.Sprite):
    def __init__(self,player1,player2,player1_bullets,player2_bullets,x:float,y:float,targetx,targety,screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.player1 = player1
        self.player2 = player2
        self.player1_bullets = player1_bullets
        self.player2_bullets = player2_bullets
        self.image = pygame.image.load('img/icons/bullet.png')
        self.image = pygame.transform.scale(self.image,(int(self.image.get_width()*(self.screen.get_width()/1920)),int(self.image.get_height()*(self.screen.get_height()/1080))))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (int(x),int(y))
        self.targetx = targetx
        self.targety = targety
        self.angle = math.atan2(self.targety-y,self.targetx-x)
        # self.dx = math.cos(self.angle)*70
        # self.dy = math.sin(self.angle)*70

        self.dx = (math.cos(self.angle) *(self.screen.get_width()/1920))
        self.dy = (math.sin(self.angle) * (self.screen.get_height()/1080))


    def update(self, collidable_objects):
        #moving the bullet
        #we have to make this intermediate step unless there would be rounding
        #problems with bullet trajectory
        for i in range(70):
            self.x += self.dx
            self.y += self.dy
            self.rect.centerx = int(self.x)
            self.rect.centery = int(self.y)
            #check if bullet has gone off the screen, note 1000,650 is screen width
            #and height respectively
            if self.rect.right < 0 or self.rect.left > 1920 or self.rect.bottom < 0 or self.rect.top > 1080:
                self.kill()
            for tile in collidable_objects:
                if tile[1].colliderect(self.rect):
                    self.kill()

            #checking collion of player1 and player 2 bullets group
            if pygame.sprite.spritecollide(self.player1,self.player2_bullets,False):
                if self.player1.alive:
                    self.kill()
                    self.player1.health -= 10
            #checking collion of player2 and player 1 bullets group
            if pygame.sprite.spritecollide(self.player2,self.player1_bullets,False):
                if self.player2.alive:
                    self.kill()
                    self.player2.health -= 10




