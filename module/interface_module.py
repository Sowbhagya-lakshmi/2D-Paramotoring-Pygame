import pygame
import sys
import os
import main


button_original = pygame.image.load(os.path.join('Utils/Pics/Interface','Button.png'))
button_enlarge =  pygame.image.load(os.path.join('Utils/Pics/Interface','Button_Enlarge.png'))
button_click =  pygame.image.load(os.path.join('Utils/Pics/Interface','Button_click.png'))



def display_play_button(screen):
	
	screen.blit(button_original, (440,100))
	font_size = 30
	font = pygame.font.Font('freesansbold.ttf', font_size)
	text_x_pos, text_y_pos = 468, 135
	text = font.render('Play' , True, (255,255,255))
	screen.blit(text, (text_x_pos, text_y_pos))



def display_buttons():
    
    main.speed = 60		# fps
    main.run = True

    
    while True:

        width, height = 1000,600

        win = pygame.display.set_mode((width, height))
        win.fill((255,255,255))
        pygame.display.set_caption('Game Interface') 

        display_play_button(win);

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()

            mouse = pygame.mouse.get_pos()

            if 440 <= mouse[0] <= 560 and 140 <= mouse[1] <= 180 :
                win.blit(button_enlarge, (430,60))
                font_size = 40
                font = pygame.font.Font('freesansbold.ttf', font_size)
                text_x_pos, text_y_pos = 465, 135
                text = font.render('Play' , True, (255,255,255))
                win.blit(text, (text_x_pos, text_y_pos))


        pygame.display.update()
        
              