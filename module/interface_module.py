import pygame
import sys
import os
import main

# Global variables
win = None

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

def display_resume_button(screen):
	
	screen.blit(button_original, (440,200))
	font_size = 26
	font = pygame.font.Font('freesansbold.ttf', font_size)
	text_x_pos, text_y_pos = 448, 235
	text = font.render('Resume' , True, (255,255,255))
	screen.blit(text, (text_x_pos, text_y_pos))

def display_highscore_button(screen):
	
	screen.blit(button_original, (440,300))
	font_size = 22
	font = pygame.font.Font('freesansbold.ttf', font_size)
	text_x_pos, text_y_pos = 445, 340
	text = font.render('HighScore' , True, (255,255,255))
	screen.blit(text, (text_x_pos, text_y_pos))

def display_instruction_button(screen):
	
	screen.blit(button_original, (440,400))
	font_size = 20
	font = pygame.font.Font('freesansbold.ttf', font_size)
	text_x_pos, text_y_pos = 442, 440
	text = font.render('Instruction' , True, (255,255,255))
	screen.blit(text, (text_x_pos, text_y_pos))

def display_about_button(screen):
	
	screen.blit(button_original, (440,500))
	font_size = 30
	font = pygame.font.Font('freesansbold.ttf', font_size)
	text_x_pos, text_y_pos = 455, 535
	text = font.render('About' , True, (255,255,255))
	screen.blit(text, (text_x_pos, text_y_pos))


class Settings_button:
    """
    Describes the settings button and its functionality.
    """
    def __init__(self):
        self.img_small = pygame.image.load(os.path.join('Utils/Pics/Interface','settings.png')).convert_alpha()
        self.img_big = pygame.transform.scale(self.img_small,(int(self.img_small.get_width()*1.1), int(self.img_small.get_height()*1.1)))
        self.img = self.img_small
        self.x = 900
        self.y = 30

    def draw(self):
        win.blit(self.img, (self.x, self.y))

class Cursor:
    """
    Define a custom cursor for the game instead of the system's cursor. Placing an image of a cursor at the mouse coordinates.
    """
    def __init__(self):
        self.img = pygame.image.load(os.path.join('Utils/Pics/Interface', 'cursor.png')).convert_alpha()
        self.x, self.y  = pygame.mouse.get_pos()

    def draw(self):
        self.x, self.y  = pygame.mouse.get_pos()
        win.blit(self.img, (self.x, self.y))
    
def event_loop():
    for event in pygame.event.get():		
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()		
        if event.type == pygame.KEYDOWN:
            if event.key == 27:		# press esc to quit
                pygame.quit()
                sys.exit()

def cursor_over_button(cursor, button):
    """
    Using pixel perfect collision check if the cursor image and the button passed in the argument collide and return boolean.
    """
    cursor_mask = pygame.mask.from_surface(cursor.img)
    button_mask = pygame.mask.from_surface(button.img_small)

    offset = button.x-cursor.x, button.y-cursor.y
    collision = cursor_mask.overlap(button_mask, offset)    # returns bool

    if collision:
        button.img = button.img_big
    else:
        button.img = button.img_small
    

def display_buttons():
    
    main.speed = 60		# fps
    main.run = True

    count = 0

    global win
    width, height = 1000,600
    print('creating window')
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Game Interface')

    cursor = Cursor()
    settings_button = Settings_button()

    # Hide the original cursor
    pygame.mouse.set_visible(False)

    all_buttons_list = [settings_button]

    clock = pygame.time.Clock()
    
    while count < 1000: 
        win.fill((255,255,255))

        event_loop()
        
        display_play_button(win)
        display_resume_button(win)
        display_highscore_button(win)
        display_instruction_button(win)
        display_about_button(win)

        mouse = pygame.mouse.get_pos()
        value = 0

        if 440 <= mouse[0] <= 560 and 140 <= mouse[1] <= 180 :
            win.blit(button_enlarge, (430,60))
            font_size = 40
            font = pygame.font.Font('freesansbold.ttf', font_size)
            text_x_pos, text_y_pos = 465, 135
            text = font.render('Play' , True, (255,255,255))
            win.blit(text, (text_x_pos, text_y_pos))  
            
        if 440 <= mouse[0] <= 560 and 240 <= mouse[1] <= 280 :
            win.blit(button_enlarge, (430,160))
            font_size = 38
            font = pygame.font.Font('freesansbold.ttf', font_size)
            text_x_pos, text_y_pos = 438, 235
            text = font.render('Resume' , True, (255,255,255))
            win.blit(text, (text_x_pos, text_y_pos))
            

        if 440 <= mouse[0] <= 560 and 340 <= mouse[1] <= 380 :
            win.blit(button_enlarge, (430,260))
            font_size = 32
            font = pygame.font.Font('freesansbold.ttf', font_size)
            text_x_pos, text_y_pos = 432, 335
            text = font.render('HighScore' , True, (255,255,255))
            win.blit(text, (text_x_pos, text_y_pos)) 

        if 440 <= mouse[0] <= 560 and 440 <= mouse[1] <= 480 :
            win.blit(button_enlarge, (430,360))
            font_size = 30
            font = pygame.font.Font('freesansbold.ttf', font_size)
            text_x_pos, text_y_pos = 430, 435
            text = font.render('Instruction' , True, (255,255,255))
            win.blit(text, (text_x_pos, text_y_pos)) 

        if 440 <= mouse[0] <= 560 and 540 <= mouse[1] <= 580 :
            win.blit(button_enlarge, (430,460))
            font_size = 40
            font = pygame.font.Font('freesansbold.ttf', font_size)
            text_x_pos, text_y_pos = 448, 535
            text = font.render('About' , True, (255,255,255))
            win.blit(text, (text_x_pos, text_y_pos))
        
        for button in all_buttons_list:
            # Drawing buttons
            button.draw()

            # Enlarging effect while cursor is over button
            cursor_over_button(cursor, button)

        cursor.draw()   # should be at last, to avoid overlapping

        clock.tick(main.speed)
        pygame.display.update()
        count += 1 
    
    
    # Bring back the original cursor
    pygame.mouse.set_visible(True)

value = 0
def check_play():
    mouse = pygame.mouse.get_pos()
    if 440 <= mouse[0] <= 560 and (140 <= mouse[1] <= 180) or (240 <= mouse[1] <= 280) :
        if pygame.mouse.get_pressed() == 1 :
                value = 1 
    return value
        




            

            

        
        
              