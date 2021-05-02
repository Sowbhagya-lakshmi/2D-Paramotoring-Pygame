import pygame
from pygame.locals import *
import os
import sys
import math

pygame.init()

W, H = 1550, 800
win = pygame.display.set_mode((W,H))
pygame.display.set_caption('Game Window')

bg = pygame.image.load(os.path.join('pics','bg.png')).convert()
bgX = 0
bgX2 = bg.get_width()                             # to get width of the image

clock = pygame.time.Clock()
 
class player(object):
    
    running = [pygame.image.load(os.path.join('pics', "player-"+ str(x) + '.png')) for x in range(1,10)]
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height 
        self.runCount = 0
    
    def draw (self, win):
        if self.runCount > 63:
            self.runCount = 0
        win.blit(self.running[self.runCount//9], (loc[0],loc[1]))
        self.runCount += 1    

def redrawWindow():
    largeFont = pygame.font.SysFont('comicsans', 30)
    win.blit(bg, (bgX, 0))
    win.blit(bg, (bgX2,0))
   
run = True
speed = 60
runner = player(200, 313, 50, 50)

while run:
    redrawWindow()

    x = clock.tick(speed)
    bgX -= 1.4
    bgX2 -= 1.4
    
    if bgX < bg.get_width() * -1:
        bgX = bg.get_width()
    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width() 
  
    (mx, my) = pygame.mouse.get_pos()
       
    if my < 320 :
        rot = 0
        loc = [250, my]
        runner.draw(win)
    else:
        rot = 0
        loc = [250, 320]
        runner.draw(win)
    
    for event in pygame.event.get():
        
        if event.type == QUIT or event.type == KEYDOWN:
            pygame.quit()
            sys.exit()
            run = False

    pygame.display.update()
    clock.tick((speed))