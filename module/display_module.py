import os
import pygame

import main

# LIVES
heart = pygame.image.load(os.path.join('Utils/Pics/Display/', 'life.png'))

def display_lives(win, num_of_lives):
    """
    Displays the lives of the player.
    """
    x_pos = 20
    for _ in range(num_of_lives):
        win.blit(heart, (x_pos,75))
        x_pos += heart.get_width() + 3


# MINIMAP
line = pygame.image.load(os.path.join('Utils/Pics/Display/','line.png'))
line = pygame.transform.scale(line, (line.get_width()//2, line.get_height()//5))

icon_big = pygame.image.load(os.path.join('Utils/Pics/Display/','player_location.png'))
player_icon = pygame.transform.scale(icon_big, (icon_big.get_width()//5, icon_big.get_height()//5)) 

start = pygame.image.load(os.path.join('Utils/Pics/Display/','start.png'))
start = pygame.transform.scale(start, (start.get_width()//10, start.get_height()//10))

finish = pygame.image.load(os.path.join('Utils/Pics/Display/','finish.png'))
finish = pygame.transform.scale(finish, (finish.get_width()//10, finish.get_height()//10))

line_pos_x = 1140
line_pos_y = 770

def draw_minimap(win,progress):
    """
    Minimap shows the position of the player relative to the full distance in a miniature size.
    """
    max_progress = main.game_duration*main.speed
    current_progress = progress/max_progress        # Value btn 0 and 1

    # Line
    win.blit(line, (line_pos_x, line_pos_y))
    # Start point
    win.blit(start, (line_pos_x-25,line_pos_y-45))
    # End point
    win.blit(finish, (line_pos_x+320,line_pos_y-45))

    # Adding the player location icon
    x_pos = line_pos_x + line.get_width()*current_progress
    centroid_x_pos = x_pos - player_icon.get_width()//2   
    y_pos = line_pos_y - player_icon.get_height()
    win.blit(player_icon, (centroid_x_pos, y_pos))