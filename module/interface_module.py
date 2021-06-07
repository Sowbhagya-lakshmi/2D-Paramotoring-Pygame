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
	
	screen.blit(button_original, (440,200))
	font_size = 30
	font = pygame.font.Font('freesansbold.ttf', font_size)
	text_x_pos, text_y_pos = 470, 235
	text = font.render('Play' , True, (0,0,0))
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





    


       
       
       
       
       
       

