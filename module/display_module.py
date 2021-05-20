import os
import pygame

import main
from module import player_module

# LIVES
heart = pygame.image.load(os.path.join('Utils/Pics/Display/', 'life.png'))

def display_lives(win, num_of_lives):
    x_pos = 20
    for _ in range(num_of_lives):
        win.blit(heart, (x_pos,75))
        x_pos += 50


# MINIMAP
line = pygame.image.load(os.path.join('Utils/Pics/Display/','line.png'))
line = pygame.transform.scale(line, (line.get_width()//2, line.get_height()//5))

player_img = player_module.player.imgs[0]
player_icon = pygame.transform.scale(player_img, (player_img.get_width()//3, player_img.get_height()//3))  

start = pygame.image.load(os.path.join('Utils/Pics/Display/','start.png'))
start = pygame.transform.scale(start, (start.get_width()//10, start.get_height()//10))

finish = pygame.image.load(os.path.join('Utils/Pics/Display/','finish.png'))
finish = pygame.transform.scale(finish, (finish.get_width()//10, finish.get_height()//10))

line_pos_x = 1140
line_pos_y = 770

def draw_progression_bar(win,progress):
    max_progress = main.game_duration*main.speed
    current_progress = progress/max_progress
    win.blit(line, (line_pos_x, line_pos_y))
    win.blit(start, (line_pos_x-25,line_pos_y-45))
    win.blit(finish, (line_pos_x+320,line_pos_y-45))
    win.blit(player_icon, (line_pos_x+(line.get_width()-50)*current_progress,line_pos_y-player_icon.get_height()))