import math,random,sys
import pygame
from pygame.locals import *

def events():
    for event in pygame.event.get():
        if event.type == QUIT or(event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

W,H = 1000,650
HW,HH =W/2,H/2
AREA = W*H

pygame.init()
CLOCK = pygame.time.Clock()
DS = pygame.display.set_mode((W,H))
pygame.display.set_caption("leks")
FPS =120

BLACK = (0,0,0,255)
WHITE = (255,255,255,255)
x,y = HW,HH
pmx,pmy = x,y
dx,dy = 0,0
distance = 0
speed = 3
while True:
    events()
    m = pygame.mouse.get_pressed()
    if m[0] and not distance:
        mx,my = pygame.mouse.get_pos()

        radians = math.atan2(my-pmy,mx-pmx)
        distance = math.hypot(mx-pmx,my-pmy)/speed
        distance = int(distance)

        dx = math.cos(radians)*speed
        dy = math.sin(radians)*speed

        pmx,pmy = mx,my

    if distance:
        distance -=1
        x+= dx
        y+= dy

    pygame.draw.circle(DS,WHITE,(int(x),int(y)),5,0)
    if distance:
        pygame.draw.circle(DS,(255,0,0),(pmx,pmy),2,0)

    pygame.display.update()
    CLOCK.tick(FPS)
    DS.fill(BLACK)
