import pygame
import sys
import os
import main

button_original = pygame.image.load(os.path.join('Utils/Pics/Interface','Button.png'))
button_enlarge =  pygame.image.load(os.path.join('Utils/Pics/Interface','Button_Enlarge.png'))
button_click =  pygame.image.load(os.path.join('Utils/Pics/Interface','Button_click.png'))

def display_play_button(screen):
	
	screen.blit(button_original, (440,200))
	font_size = 30
	font = pygame.font.Font('freesansbold.ttf', font_size)
	text_x_pos, text_y_pos = 470, 235
	text = font.render('Play' , True, (0,0,0))
	screen.blit(text, (text_x_pos, text_y_pos))

def display_buttons():
    
    main.speed = 60		# fps
    main.run = True

    count = 0
    
    while count < 1000:
        width, height = 1000,600
        win = pygame.display.set_mode((width, height))
        win.fill((255,255,255))
        pygame.display.set_caption('Game Interface') 

        display_play_button(win);

        pygame.display.update()

        count += 1 




    


       
       
       
       
       
       

