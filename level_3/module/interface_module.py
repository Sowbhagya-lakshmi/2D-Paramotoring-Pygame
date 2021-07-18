import sys
import os
import pygame

import global_config
from level_3.module import music_module
from level_3.module import coins_module


# Global variables
win = None
cursor = None

right_click = False
value = 0

mute_button, unmute_button = None, None

#Loading Button and Screen Images
screen_end =  pygame.image.load(os.path.join(r'level_1/Utils/Pics/Interface','Screen_End.png'))
screen_win =  pygame.image.load(os.path.join(r'level_3/Utils/Pics/Interface','Screen_Winscreen.png'))

button_home =  pygame.image.load(os.path.join(r'level_1/Utils/Pics/Interface','Button_Home.png'))
button_home_small = pygame.transform.scale(button_home, (int(button_home.get_width()*0.7),int(button_home.get_height()*0.7)))
button_home_enlarge = pygame.transform.scale(button_home, (int(button_home.get_width()*0.8),int(button_home.get_height()*0.8)))

button_restart =  pygame.image.load(os.path.join(r'level_1/Utils/Pics/Interface/Buttons','Button_Restart.png'))
button_restart_enlarge = pygame.transform.scale(button_restart, (int(button_restart.get_width()*1.1),int(button_restart.get_height()*1.1)))

button_quit =  pygame.image.load(os.path.join(r'level_1/Utils/Pics/Interface/Buttons','Button_Quit.png'))
button_quit_enlarge = pygame.transform.scale(button_quit, (int(button_quit.get_width()*1.1),int(button_quit.get_height()*1.1)))

button_highscore =  pygame.image.load(os.path.join(r'level_1/Utils/Pics/Interface/Buttons','Button_HighScore.png'))
button_score =  pygame.image.load(os.path.join(r'level_1/Utils/Pics/Interface/Buttons','Button_Score.png'))

button_inverted =  pygame.image.load(os.path.join(r'level_1/Utils/Pics/Interface/Buttons','Button_inverted.png'))
button_inverted_enlarge = pygame.transform.scale(button_inverted, (int(button_inverted.get_width()*1.1),int(button_inverted.get_height()*1.1)))

button_instructions =  pygame.image.load(os.path.join(r'level_1/Utils/Pics/Interface/Buttons','Button_Instructions.png'))
button_instructions_enlarge = pygame.transform.scale(button_instructions, (int(button_instructions.get_width()*1.1),int(button_instructions.get_height()*1.1)))

button_resume =  pygame.image.load(os.path.join(r'level_1/Utils/Pics/Interface/Buttons','Button_Resume.png'))
button_resume_enlarge = pygame.transform.scale(button_resume, (int(button_resume.get_width()*1.1),int(button_resume.get_height()*1.1)))


def check_end():
	"""
	Checks if quit button is clicked in the end screen and returns the value 1
	"""
	global value, right_click
	value = 0
	mouse = pygame.mouse.get_pos()
		
	if 320 <= mouse[1] <= 480 and 450 <= mouse[0] <=500:
		if right_click:
			value = 1 
	return value


class Cursor:
	"""
	Define a custom cursor for the game instead of the system's cursor. Placing an image of a cursor at the mouse coordinates.
	"""
	def __init__(self):
		self.img = pygame.image.load(os.path.join(r'level_1/Utils/Pics/Interface', 'cursor.png')).convert_alpha()
		self.x, self.y  = pygame.mouse.get_pos()

	def draw(self,win):
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

	offset = button.centroid_x-cursor.x, button.centroid_y-cursor.y
	collision = cursor_mask.overlap(button_mask, offset)    # returns bool

	return collision


class Volume_control:
	"""
	Creates a dropdown when the settings is clicked. 
	"""
	x = 760
	y = 40

	button_flag = False
	
	def __init__(self):
		self.buttons_list = [unmute_button, mute_button]
		self.img = self.buttons_list[0].img
	
	def check_status(self, button, pop_sound_play):
		"""
		Checks whether the cursor is over the button. And if it is clicked inverts the status of the button i.e mute to unmute or vice versa.
		"""
		collision_with_button = cursor_over_button(cursor, button)

		# If the cursor is over button, button enlarges
		if collision_with_button:
			button.img = button.img_big		

			# If clicked, button is changed
			if right_click:
				button = self.buttons_list[not(self.buttons_list.index(button))]
				# Sound effect
				if pop_sound_play == False:
					music_module.sound_button_enlarge.play()
					pop_sound_play = True
				else:
					pop_sound_play = False
		else:
			button.img = button.img_small		

		self.draw(button)		
		self.functionality(button)

		return button, pop_sound_play

	def functionality(self, volume_button):
		
		if self.buttons_list.index(volume_button) == 1:
			pygame.mixer.music.stop()
			self.button_flag = True
		elif self.buttons_list.index(volume_button) == 0 and self.button_flag:
			pygame.mixer.music.play(-1)
			self.button_flag = False

	def draw(self, button):
		button.centroid_x = Volume_control.x - button.img.get_width()//2
		button.centroid_y = Volume_control.y - button.img.get_height()//2

		win.blit(button.img, (button.centroid_x, button.centroid_y))


class Mute_button:
	"""
	Defines the mute button
	"""
	def __init__(self):
		self.centroid_x = 0
		self.centroid_y = 0

		self.img_original = pygame.image.load(os.path.join(r'level_1/Utils/Pics/Interface', 'mute.png')).convert_alpha()
		self.img_small = pygame.transform.scale(self.img_original,(int(self.img_original.get_width()/1.5), int(self.img_original.get_height()/1.5)))
		self.img_big = pygame.transform.scale(self.img_original,(int(self.img_original.get_width()/1.3), int(self.img_original.get_height()/1.3)))

		self.img = self.img_small


class Unmute_button:
	"""
	Defines the unmute button
	"""
	def __init__(self):
		self.centroid_x = 0
		self.centroid_y = 0

		self.img_original = pygame.image.load(os.path.join(r'level_1/Utils/Pics/Interface', 'unmute.png')).convert_alpha()		
		self.img_small = pygame.transform.scale(self.img_original,(int(self.img_original.get_width()/1.5), int(self.img_original.get_height()/1.5)))
		self.img_big = pygame.transform.scale(self.img_original,(int(self.img_original.get_width()/1.3), int(self.img_original.get_height()/1.3)))

		self.img = self.img_small
   

def display_endscreen():
	
	"""
	Creates a screen to display the buttons at the end of the game after losing
	"""

	global win, cursor
	global mute_button, unmute_button
	
	global_config.fps = 60		# fps
	
	coin = coins_module.Coin.num_coins_collected

	# Home screen interface
	width, height = 800,600
	win = pygame.display.set_mode((width, height))	
	pygame.display.set_caption('End Screen')

	# Creating objects of classes
	cursor = Cursor()
	clock = pygame.time.Clock()

	# Hide the original cursor
	pygame.mouse.set_visible(False)

	pop_sound_play = False

	#Music Variable
	pygame.mixer.music.load(os.path.join(r'level_1\Utils\Music\InterfaceBG.wav'))
	pygame.mixer.music.play(-1)

	i=0
	while i<20000:
		val = check_end()
		if val == 1:
			pygame.quit()

		win.blit(screen_end,(0,0))
		win.blit(button_score, (320,300))
		win.blit(button_quit,(320,450))
		event_loop()

		mouse = pygame.mouse.get_pos()

		if 320 <= mouse[0] <= 480 and 300 <= mouse[1] <= 350 :
			if right_click == 0:
				win.blit(button_inverted_enlarge, (310,300))
				font_size = 40
				font = pygame.font.Font(r'level_1\Utils\Font\FreeSansBold.ttf', font_size)
				text = font.render(str(coin), True, (255,255,255))
				win.blit(text, (380, 310))
			if pop_sound_play == False:
				music_module.sound_button_enlarge.play()
			pop_sound_play = True
	
		if 320 <= mouse[0] <= 480 and 450 <= mouse[1] <= 500 :
			if right_click == 0:
				win.blit(button_quit_enlarge, (310,450))
			if pop_sound_play == False:
				music_module.sound_button_enlarge.play()
			pop_sound_play = True
		else:
			pop_sound_play = False
							

		cursor.draw(win)  
		clock.tick(global_config.fps)
		pygame.display.update()
	
	# Bring back the original cursor
	pygame.mouse.set_visible(True)


def display_winscreen():
	
	"""
	Creates a screen to display the buttons at the end after winning the game
	"""

	global win, cursor, right_click
	global mute_button, unmute_button
	
	break_bool = False

	global_config.fps = 60		# fps
	
	coin = coins_module.Coin.num_coins_collected

	# Home screen interface
	width, height = 800,600
	win = pygame.display.set_mode((width, height))	
	pygame.display.set_caption('End Screen')

	win.blit(screen_win,(0,0))
	win.blit(button_score, (320,300))
	win.blit(button_restart, (320,450))

	pygame.display.update()

	# Creating objects of classes
	cursor = Cursor()

	clock = pygame.time.Clock()

	# Hide the original cursor
	pygame.mouse.set_visible(False)

	pop_sound_play = False

	#Music Variable
	pygame.mixer.music.load(os.path.join(r'level_1\Utils\Music\InterfaceBG.wav'))
	pygame.mixer.music.play(-1)

	i=0
	while i<20000:

		win.blit(screen_win,(0,0))
		win.blit(button_score, (320,300))
		win.blit(button_restart, (320,450))

		event_loop()

		mouse = pygame.mouse.get_pos()


		if 320 <= mouse[0] <= 480 and 300 <= mouse[1] <= 350 :
			if right_click == 0:
				win.blit(button_inverted_enlarge, (310,300))
				font_size = 40
				font = pygame.font.Font(r'level_1\Utils\Font\FreeSansBold.ttf', font_size)
				text = font.render(str(coin), True, (255,255,255))
				win.blit(text, (380, 310))
			if pop_sound_play == False:
				music_module.sound_button_enlarge.play()
			pop_sound_play = True

		if 320 <= mouse[0] <= 480 and 450 <= mouse[1] <= 500 :
			if right_click == 0:				
				win.blit(button_restart_enlarge, (310,450))
			elif right_click:
				break_bool = True
				return break_bool
			if pop_sound_play == False:
				music_module.sound_button_enlarge.play()
			pop_sound_play = True
			
		else:
			pop_sound_play = False							

		cursor.draw(win)   # should be at last, to avoid overlapping

		clock.tick(global_config.fps)
		pygame.display.update()

	# Bring back the original cursor
	pygame.mouse.set_visible(True)