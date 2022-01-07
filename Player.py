import pygame
import math
from bullet_interim import BulletInterim
class Player(pygame.sprite.Sprite):

    def __init__(self,health,ammo,cooldown,bullet_interim_list:list,vertical_velocity,is_in_air,can_jump,is_alive,update_timer,player_type,players_action,action_number,flip,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.max_health = 200
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
        self.animation_types = {}
        temp_animationList = []
        for i in range(5):
            temp_image1 = pygame.image.load('img/' + player_type+'/' + 'Idle/' + str(i)+'.png')
            temp_image2 = pygame.transform.scale(temp_image1,((int(temp_image1.get_width()*2)),(int(temp_image1.get_width()*2))))
            temp_animationList.append(temp_image2)
        self.animation_types['Idle'] = temp_animationList
        temp_animationList = []
        for i in range(6):
            temp_image1 = pygame.image.load('img/' + player_type+'/' + 'Run/' + str(i)+'.png')
            temp_image2 = pygame.transform.scale(temp_image1,((int(temp_image1.get_width()*2)),(int(temp_image1.get_width()*2))))
            temp_animationList.append(temp_image2)
        self.animation_types['Run'] = temp_animationList
        temp_image1 = pygame.image.load('img/' + player_type+'/' + 'Jump/' +'0.png')
        temp_image2 = pygame.transform.scale(temp_image1,((int(temp_image1.get_width()*2)),(int(temp_image1.get_width()*2))))
        self.animation_types['Jump'] = [temp_image2]
        temp_animationList = []
        for i in range(8):
            temp_image1 = pygame.image.load('img/' + player_type+'/' + 'Death/' + str(i)+'.png')
            temp_image2 = pygame.transform.scale(temp_image1,((int(temp_image1.get_width()*2)),(int(temp_image1.get_width()*2))))
            temp_animationList.append(temp_image2)
        self.animation_types['Death'] = temp_animationList
        self.scaled_image = self.animation_types[players_action][int(action_number)]
        self.rect = self.scaled_image.get_rect()
        self.rect.center=(x,y)
        self.cooldown = cooldown

    def draw_health_bar(self,x,y):
        font = pygame.font.SysFont('Futura',30)
        text = font.render(self.player_type.upper() + "'S HEALTH:",True,(255,255,255))
        pygame.display.get_surface().blit(text,(x - 200,y))
        pygame.draw.rect(pygame.display.get_surface(), (255, 255, 255), (x -2,y-2,400+4,20+4))
        pygame.draw.rect(pygame.display.get_surface(), (255, 0, 0), (x,y,400,20))
        pygame.draw.rect(pygame.display.get_surface(), (0, 255, 0), (x,y,(400 * (self.health / self.max_health)),20))

    def draw_ammo(self,x,y):
        font = pygame.font.SysFont('Futura',30)
        text = font.render(self.player_type.upper() + "'S AMMO: " + str(self.ammo),True,(255,255,255))
        pygame.display.get_surface().blit(text,(x - 200,y))


    def is_alive_now(self):
        if self.health <= 0:
            self.is_alive = False
            self.health = 0
            self.update_animation('Death')

    def shoot(self):
        x,y = pygame.mouse.get_pos()
        # x_dist = (mouse_pos[0] - self.rect.midleft[0])
        # y_dist = (mouse_pos[1] - self.rect.midleft[1])
        # angle = math.atan2(mouse_pos[1] - self.rect.midleft[1],mouse_pos[0] - self.rect.midleft[0])
        # distance = math.hypot(mouse_pos[1] - self.rect.midleft[1],mouse_pos[0] - self.rect.midleft[0])/10
        # distance = int(distance)
        #get mouseclick
        # the things after the and statement anre just to make sure that the
        # player is not clicking on themselves or clicking in places that make
        # bullets hit the player
        if pygame.mouse.get_pressed()[0] and not((x<= self.rect.right and x>=self.rect.left)and(y<=self.rect.bottom+10 and y>= self.rect.top-10)):

            muzzle_img = pygame.image.load('img/MuzzleFlash.png')
            muzzle_img_rect = muzzle_img.get_rect()
            if x < self.rect.right and x < self.rect.left:
                 self.flip = True
            elif x > self.rect.left and x> self.rect.right:
                self.flip = False
            if self.cooldown <= 0 and self.flip == False and self.ammo > 0:

                muzzle_img_rect.center = self.rect.midright[0]+5,self.rect.midright[1]
                bullet = BulletInterim(self.rect.midright[0] +12, self.rect.midright[1],x,y)
                self.bullet_interim_list.append(bullet)
                pygame.display.get_surface().blit(muzzle_img,muzzle_img_rect)
                self.cooldown = 10
                self.ammo -= 1
                # if self.ammo % 5 == 0:
                #     self.cooldown = 120

            elif self.cooldown <= 0 and self.flip == True and self.ammo > 0:
                muzzle_img_rect.center = self.rect.midleft[0] -5 ,self.rect.midleft[1]
                muzzle_img = pygame.transform.flip(muzzle_img,True,False)
                bullet = BulletInterim(self.rect.midleft[0]-12, self.rect.midleft[1],x,y)
                self.bullet_interim_list.append(bullet)
                pygame.display.get_surface().blit(muzzle_img,muzzle_img_rect)
                self.cooldown = 10
                self.ammo -= 1
                # if self.ammo % 5 == 0:
                #     self.cooldown = 120
            # if self.flip == False:
            #     if x < self.rect.right and x < self.rect.left:
            #         self.flip = True
            #     muzzle_img_rect.center = self.rect.midright
            #     bullet = BulletInterim(self.rect.midright[0] +12, self.rect.midright[1],x,y)
            #     self.bullet_interim_list.append(bullet)
            # else:
            #     if x > self.rect.left and x> self.rect.right:
            #         self.flip = False
            #     muzzle_img_rect.center = self.rect.midleft
            #     bullet = BulletInterim(self.rect.midleft[0]-12, self.rect.midleft[1],x,y)
            #     self.bullet_interim_list.append(bullet)


    def update_cooldown(self):
        if self.cooldown >0:
            self.cooldown -= 2

    def animate(self):
        ANIMATION_TIMER = 150
        self.scaled_image = self.animation_types[self.players_action][int(self.action_number)]
        if pygame.time.get_ticks() - self.update_timer >= ANIMATION_TIMER:
            self.action_number = str(int(self.action_number)+1)
            self.update_timer = pygame.time.get_ticks()
        if int(self.action_number) >= len(self.animation_types[self.players_action]):
            if self.players_action == 'Death':
                self.action_number = len(self.animation_types[self.players_action]) -1
            else:
                self.action_number = str(0)

    def update_animation(self,new_action):
        if self.players_action != new_action:
            self.players_action = new_action
            #reset timer and action number
            self.action_number = str(0)
            self.update_timer = pygame.time.get_ticks()


    def draw(self,surface):
        surface.blit(pygame.transform.flip(self.scaled_image,self.flip,False),(self.rect.x,self.rect.y))

    def move(self,is_moving_right,is_moving_left,collidable_objects_list:list):
        #check to see if player is in air
        if self.vertical_velocity!= 0:
            self.is_in_air = True
#reset the dx and dy
        dx = 0
        dy = 0
        if is_moving_right:
            dx += 15
            self.flip = False

        if is_moving_left:
            dx -= 15
            self.flip = True

#control jumps
        if self.can_jump and not self.is_in_air:
            self.vertical_velocity -= 15
            self.can_jump = False
            self.is_in_air = True
#add gravity so player is still moving up but now moving up at a slower velocity
# remember we add gravity and not subtract cuz bigger y in pygame means lower
# height
        self.vertical_velocity += 1
# but still we don't want the player to fall too fast so we'll cap it's falling
# speed
#         if self.vertical_velocity >10:
#             self.vertical_velocity = 10

        dy += self.vertical_velocity
# now we check that the player stops falling once it hits the ground
# but if he's close to the ground then it would fall just enough to land on the
# ground and set the player to not be in the air
        #check for collison
        for tile in collidable_objects_list:
            #check for collison in x direction
            if tile[1].colliderect(self.rect.x + dx,self.rect.y,self.scaled_image.get_width(),self.scaled_image.get_height()):
                dx = 0
            #check for collison in x direction
            if tile[1].colliderect(self.rect.x,self.rect.y + dy,self.scaled_image.get_width(),self.scaled_image.get_height()):
# check when going up or jumping
                if self.vertical_velocity < 0:
                    self.vertical_velocity = 0
                    dy = tile[1].bottom - self.rect.top
                    # self.is_in_air = False
                    self.can_jump = False
                elif self.vertical_velocity >= 0:
                    self.vertical_velocity = 0
                    dy = tile[1].top - self.rect.bottom
                    self.is_in_air = False
                    self.can_jump = False

#update the x and y of the character
        self.rect.centerx += dx
        self.rect.centery += dy
