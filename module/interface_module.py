import pygame
import sys
import os
import main

# Global variables
win = None
right_click = False
dropdown_bool = False

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
	global right_click

	right_click = False 

	for event in pygame.event.get():		
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()		
		elif event.type == pygame.KEYDOWN:
			if event.key == 27:		# press esc to quit
				pygame.quit()
				sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				right_click = True 

		       
def cursor_over_button(cursor, button):
	"""
	Using pixel perfect collision check if the cursor image and the button passed in the argument collide and return boolean.
	"""
	cursor_mask = pygame.mask.from_surface(cursor.img)
	button_mask = pygame.mask.from_surface(button.img)

	offset = button.x-cursor.x, button.y-cursor.y
	collision = cursor_mask.overlap(button_mask, offset)    # returns bool

	if collision:
		button.img = button.img_big		# If the cursor is over button, button enlarges
	else:
		button.img = button.img_small

	return collision

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

class Dropdown:
	"""
	Creates a dropdown when the settings is clicked. 
	"""
	def __init__(self):
		self.x = 900
		self.y = 100
	
	def volume_control(self, button):
		"""
		Volume icon in dropdown
		"""
		if dropdown_bool:
			button.draw()     	# if settings button is clicked, volume button should be displayed
			if button.y <=button.y_max:
				button.y += 20	# pixel change 
		else:
			if button.y >= button.y_min:
				button.draw()	# Volume button should be displayed only until transition
				button.y -= 20
		
class Mute_button:
	def __init__(self):
		self.img_small = pygame.image.load(os.path.join('Utils/Pics/Interface', 'mute.png')).convert_alpha()
		self.img_big = pygame.transform.scale(self.img_small,(int(self.img_small.get_width()*1.1), int(self.img_small.get_height()*1.1)))

		self.img = self.img_small
		self.x = 900
		self.y = 0
		self.y_min = 30
		self.y_max = 100
	
	def draw(self):
		win.blit(self.img, (self.x, self.y)) 

class Unmute_button:
	def __init__(self):
		self.img_small = pygame.image.load(os.path.join('Utils/Pics/Interface', 'unmute.png')).convert_alpha()
		self.img_big = pygame.transform.scale(self.img_small,(int(self.img_small.get_width()*1.1), int(self.img_small.get_height()*1.1)))

		self.img = self.img_small
		self.x = 900
		self.y = 0
		self.y_min = 30
		self.y_max = 100
	
	def draw(self):
		win.blit(self.img, (self.x, self.y))   

def display_buttons():

	global win, dropdown_bool
	
	main.speed = 60		# fps
	main.run = True
	count = 0

	# Home screen interface
	width, height = 1000,600
	win = pygame.display.set_mode((width, height))
	pygame.display.set_caption('Game Interface')

	# Creating objects of classes
	mute_button = Mute_button()
	unmute_button = Unmute_button()
	dropdrown = Dropdown()
	cursor = Cursor()
	settings_button = Settings_button()
        
    	display_play_button(win)
   	display_resume_button(win)
	display_highscore_button(win)
	display_instruction_button(win)
	display_about_button(win)

	event_loop()

	for event in pygame.event.get() :
		mouse = pygame.mouse.get_pos()

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
         

	dropdrown.volume_control(unmute_button)
		
	for button in all_buttons_list:
		# Drawing buttons
		button.draw()

		# Enlarging effect while cursor is over button
		collision_with_button = cursor_over_button(cursor, button)     # returns bool

		# If the settings button is clicked dropdown option is displayed
		if button == settings_button and right_click and collision_with_button:
			dropdown_bool = not(dropdown_bool)						

	cursor.draw()   # should be at last, to avoid overlapping

	clock.tick(main.speed)
	pygame.display.update()

	count += 1 
	
	# Bring back the original cursor
	pygame.mouse.set_visible(True)