import pygame
import sys
import os

import main
from module import music_module

# Global variables
win = None
cursor = None

right_click = False
value = 0

mute_button, unmute_button = None, None

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

	offset = button.centroid_x-cursor.x, button.centroid_y-cursor.y
	collision = cursor_mask.overlap(button_mask, offset)    # returns bool

	return collision

class Volume_control:
	"""
	Creates a dropdown when the settings is clicked. 
	"""
	x = 740
	y = 60

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
				# SOund effect
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

		self.img_original = pygame.image.load(os.path.join('Utils/Pics/Interface', 'mute.png')).convert_alpha()
		self.img_small = pygame.transform.scale(self.img_original,(int(self.img_original.get_width()/6), int(self.img_original.get_height()/6)))
		self.img_big = pygame.transform.scale(self.img_original,(int(self.img_original.get_width()/5), int(self.img_original.get_height()/5)))

		self.img = self.img_small
	
class Unmute_button:
	"""
	Defines the unmute button
	"""
	def __init__(self):
		self.centroid_x = 0
		self.centroid_y = 0

		self.img_original = pygame.image.load(os.path.join('Utils/Pics/Interface', 'unmute.png')).convert_alpha()		
		self.img_small = pygame.transform.scale(self.img_original,(int(self.img_original.get_width()/6), int(self.img_original.get_height()/6)))
		self.img_big = pygame.transform.scale(self.img_original,(int(self.img_original.get_width()/5), int(self.img_original.get_height()/5)))

		self.img = self.img_small
	   

def display_buttons():

	global win, cursor
	global mute_button, unmute_button
	
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
	volume_control = Volume_control()
	cursor = Cursor()

	clock = pygame.time.Clock()

	# Hide the original cursor
	pygame.mouse.set_visible(False)

	pop_sound_play = False
	volume_button = unmute_button

	#Music Variable
	Music_Background = pygame.mixer.music.load(os.path.join('Utils\Music\BGmusic_Level1.wav'))
	pygame.mixer.music.play(-1)

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
		
		volume_button, pop_sound_play = volume_control.check_status(volume_button, pop_sound_play)					

		cursor.draw()   # should be at last, to avoid overlapping

		clock.tick(main.speed)
		pygame.display.update()

		count += 1 
	
	# Bring back the original cursor
	pygame.mouse.set_visible(True)

	return not(volume_control.button_flag)