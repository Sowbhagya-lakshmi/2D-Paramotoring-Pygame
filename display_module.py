import os
import pygame

#board = pygame.image.load(os.path.join('Utils/Pics/Display/', 'lives_display.png')).convert_alpha()
#life_board = pygame.transform.scale(board, (int(board.get_width()//1.5), int(board.get_height()//1.5)))

heart = pygame.image.load(os.path.join('Utils/Pics/Display/', 'life.png')).convert_alpha()

def display_lives(win, num_of_lives):
    #win.blit(life_board, (10,70))

    x_pos = 20
    for _ in range(num_of_lives):
        win.blit(heart, (x_pos,75))
        x_pos += 50
    
