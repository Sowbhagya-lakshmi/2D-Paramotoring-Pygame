import os
import pygame
import sys
import main 

pygame.init()

button_text = [ "Play" , "Resume" , "High Score" , "Instructions" , "About"]

def Display_Buttons():
    
    main.speed = 60		# fps
    main.run = True

    width, height = 1000,600
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Game Interface') 

    
    button_original = pygame.image.load(os.path.join('Utils/Pics/Interface','Button.png')).convert_alpha()
    button_enlarge =  pygame.image.load(os.path.join('Utils/Pics/Interface','Button_Enlarge.png')).convert_alpha()
    button_click =  pygame.image.load(os.path.join('Utils/Pics/Interface','Button_click.png')).convert_alpha()
    
    #for text in Button_text:
    count = 0
    while count<1000:

        screen_color = (255,255,255)
        win.fill(screen_color)
        pygame.display.update()
        count += 1






    


       
       
       
       
       
       

