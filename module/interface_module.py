import pygame
import sys
import os

import main
from module import music_module

# Global variables
win = None
cursor = None

right_click = False
dropdown_bool = False
value = 0

#Loading Button Images
screen =  pygame.image.load(os.path.join('Utils/Pics/Interface','Para Escapade.png'))

button_about =  pygame.image.load(os.path.join('Utils/Pics/Interface','button_about.png'))
button_about_enlarge = pygame.transform.scale(button_about, (int(button_about.get_width()*1.2),int(button_about.get_height()*1.2)))

button_highscore =  pygame.image.load(os.path.join('Utils/Pics/Interface','button_highscore.png'))
button_highscore_enlarge = pygame.transform.scale(button_highscore, (int(button_highscore.get_width()*1.2),int(button_highscore.get_height()*1.2)))

button_instructions =  pygame.image.load(os.path.join('Utils/Pics/Interface','button_instructions.png'))
button_instructions_enlarge = pygame.transform.scale(button_instructions, (int(button_instructions.get_width()*1.2),int(button_instructions.get_height()*1.2)))

button_play =  pygame.image.load(os.path.join('Utils/Pics/Interface','button_play.png'))
button_play_enlarge = pygame.transform.scale(button_play, (int(button_play.get_width()*1.2),int(button_play.get_height()*1.2)))

button_resume =  pygame.image.load(os.path.join('Utils/Pics/Interface','button_resume.png'))
button_resume_enlarge = pygame.transform.scale(button_resume, (int(button_resume.get_width()*1.2),int(button_resume.get_height()*1.2)))


def check_play():
	global value, right_click
	mouse = pygame.mouse.get_pos()
	if 320 <= mouse[0] <= 480 and ((100 <= mouse[1] <= 150) or (200 <= mouse[1] <= 250)):
		if right_click:
			value = 1 
	return value

class Settings_button:
	"""
	Describes the settings button and its functionality.
	"""
	x = 730
	y = 80
	def __init__(self):
		self.img_original = pygame.image.load(os.path.join('Utils/Pics/Interface','settings.png')).convert_alpha()
		self.img_small = pygame.transform.scale(self.img_original,(int(self.img_original.get_width()/7), int(self.img_original.get_height()/7)))
		self.img_big = pygame.transform.scale(self.img_original,(int(self.img_original.get_width()/6), int(self.img_original.get_height()/6)))
		self.img = self.img_small
		# self.x = self.x
		# self.y = self.y

	def draw(self):
		win.blit(self.img, (self.x - self.img.get_width()//2, self.y - self.img.get_height()//2))

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

class Dropdown:
	"""
	Creates a dropdown when the settings is clicked. 
	"""
	def __init__(self):
		self.x = 700
		self.y = 100
	
	def volume_control(self, button):
		"""
		Volume icon in dropdown
		"""
		if dropdown_bool:
			button.draw()     	# if settings button is clicked, volume button should be displayed
			cursor_over_button(cursor, button)
			if button.y <=button.y_max:
				button.y += 20	# pixel change 
		else:
			if button.y >= button.y_min:
				button.draw()	# Volume button should be displayed only until transition
				button.y -= 20
		
class Mute_button:
	def __init__(self):
		self.img_original = pygame.image.load(os.path.join('Utils/Pics/Interface', 'mute.png')).convert_alpha()
		self.img_small = pygame.transform.scale(self.img_original,(int(self.img_original.get_width()/6), int(self.img_original.get_height()/6)))
		self.img_big = pygame.transform.scale(self.img_original,(int(self.img_original.get_width()/5), int(self.img_original.get_height()/5)))

		self.img = self.img_small
		self.x = Settings_button.x
		self.y = 0
		self.y_min = Settings_button.y
		self.y_max = 160
	
	def draw(self):
		win.blit(self.img, (self.x - self.img.get_width()//2, self.y - self.img.get_height()//2)) 

class Unmute_button:
	def __init__(self):
		self.img_original = pygame.image.load(os.path.join('Utils/Pics/Interface', 'unmute.png')).convert_alpha()		
		self.img_small = pygame.transform.scale(self.img_original,(int(self.img_original.get_width()/6), int(self.img_original.get_height()/6)))
		self.img_big = pygame.transform.scale(self.img_original,(int(self.img_original.get_width()/5), int(self.img_original.get_height()/5)))

		self.img = self.img_small
		self.x = Settings_button.x
		self.y = 0
		self.y_min = Settings_button.y
		self.y_max = 160
	
	def draw(self):
		win.blit(self.img, (self.x - self.img.get_width()//2, self.y - self.img.get_height()//2))   

def display_buttons():

	global win, cursor, dropdown_bool
	
	main.speed = 60		# fps
	main.run = True
	count = 0
	
	
	# Home screen interface
	width, height = 800,600
	win = pygame.display.set_mode((width, height))
	
	pygame.display.set_caption('Game Interface')

	# Creating objects of classes
	mute_button = Mute_button()
	unmute_button = Unmute_button()
	dropdrown = Dropdown()
	cursor = Cursor()
	settings_button = Settings_button()
        
	all_buttons_list = [settings_button]

	clock = pygame.time.Clock()

	# Hide the original cursor
	pygame.mouse.set_visible(False)

	pop_sound_play = False

	#Music Variable
	Music_Background = pygame.mixer.music.load(os.path.join('Utils\Music\BGmusic_Level1.wav'))
	pygame.mixer.music.play(-1)

	volume_button = unmute_button

	while True:	

		value = check_play()
		if value == 1: break 	# breaks interface loop

		win.fill((255,255,255))

		win.blit(screen,(0,0))
		win.blit(button_play, (320,100))
		win.blit(button_resume, (320,200))
		win.blit(button_highscore, (320,300))
		win.blit(button_instructions, (320,400))
		win.blit(button_about, (320,500))

		event_loop()

		mouse = pygame.mouse.get_pos()

		if 320 <= mouse[0] <= 480 and 100 <= mouse[1] <= 150 :
			win.blit(button_play_enlarge, (310,100))
			if pop_sound_play == False:
				music_module.sound_button_enlarge.play()
			pop_sound_play = True
			  	
		elif 320 <= mouse[0] <= 480 and 200 <= mouse[1] <= 250 :
			win.blit(button_resume_enlarge, (310,200))
			if pop_sound_play == False:
				music_module.sound_button_enlarge.play()
			pop_sound_play = True

		elif 320 <= mouse[0] <= 480 and 300 <= mouse[1] <= 350 :
			win.blit(button_highscore_enlarge, (310,300))
			if pop_sound_play == False:
				music_module.sound_button_enlarge.play()
			pop_sound_play = True
			
		elif 320 <= mouse[0] <= 480 and 400 <= mouse[1] <= 450 :
			win.blit(button_instructions_enlarge, (310,400))
			if pop_sound_play == False:
				music_module.sound_button_enlarge.play()
			pop_sound_play = True
			
		elif 320 <= mouse[0] <= 480 and 500 <= mouse[1] <= 550 :
			win.blit(button_about_enlarge, (310,500))
			if pop_sound_play == False:
				music_module.sound_button_enlarge.play()
			pop_sound_play = True

		else:
			pop_sound_play = False

		dropdrown.volume_control(volume_button)
		
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