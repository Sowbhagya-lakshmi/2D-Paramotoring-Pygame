import pygame
import global_config
from module import player_module


def draw_control_screen(win):
    
    color = (0,0,0)
    x = global_config.window_width - 300
    y = 0  
    w = 300
    h = 300
    pygame.draw.rect(win, color, pygame.Rect(x, y, w, h))

    color1 =(0,255,0)
    start_pos = (global_config.window_width - 300, 150)
    end_pos = (global_config.window_width, 150)
    
    pygame.draw.line(win, color1, start_pos, end_pos, width=3)


def draw_control_screen_actual(win):

    color = (0,0,0)
    x = global_config.window_width - 0.25*global_config.window_width
    y = 10
    w = 0.25*global_config.window_width
    h = 0.25*global_config.window_height
    
    pygame.draw.rect(win, color, pygame.Rect(x, y, w, h))

    color1 = (0,255,0)
    start_pos = (x, (0.25*global_config.window_height)//2)
    end_pos = (global_config.window_width, (0.25*global_config.window_height)//2)
    
    pygame.draw.line(win, color1, start_pos, end_pos, width=3)    

def draw_player_position(win):
    x_pos, y_pos = player_module.player.x, player_module.player.y
    player_x = 0.25*x_pos + 0.75*global_config.window_width
    player_y = 0.25*y_pos + 20
    #print(player_x,player_y)
    pygame.draw.circle(win, (255,0,0), (player_x,player_y), 15, 15)

