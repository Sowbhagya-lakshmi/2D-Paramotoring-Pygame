import pygame
import sys
import os

import main
from module import music_module , interface_module

win = None
cursor = None

right_click = False
value = 0

pygame.init()

screen_home =  pygame.image.load(os.path.join('Utils/Pics/Background','bg.png'))

button_instructions =  pygame.image.load(os.path.join('Utils/Pics/Interface/Buttons','Button_Instructions.png'))
button_instructions_small = pygame.transform.scale(button_instructions, (int(button_instructions.get_width()*0.8),int(button_instructions.get_height()*0.8)))

button_skip =  pygame.image.load(os.path.join('Utils/Pics/Interface/Buttons','Button_Skip.png'))
button_skip_enlarge = pygame.transform.scale(button_skip, (int(button_skip.get_width()*1.1),int(button_skip.get_height()*1.1)))

button_restart =  pygame.image.load(os.path.join('Utils/Pics/Interface/Buttons','Button_Restart.png'))
button_restart_enlarge = pygame.transform.scale(button_restart, (int(button_restart.get_width()*1.1),int(button_restart.get_height()*1.1)))

button_resume =  pygame.image.load(os.path.join('Utils/Pics/Interface/Buttons','Button_Resume.png'))
button_resume_enlarge = pygame.transform.scale(button_resume, (int(button_resume.get_width()*1.1),int(button_resume.get_height()*1.1)))

button_home =  pygame.image.load(os.path.join('Utils/Pics/Interface','Button_Home.png'))
button_home_small = pygame.transform.scale(button_home, (int(button_home.get_width()*0.7),int(button_home.get_height()*0.7)))
button_home_enlarge = pygame.transform.scale(button_home, (int(button_home.get_width()*0.8),int(button_home.get_height()*0.8)))

button_mode_gesture =  pygame.image.load(os.path.join('Utils/Pics/Interface/ModeOfGame','Mode_HandGesture.png'))
button_mode_gesture_enlarge = pygame.transform.scale(button_mode_gesture, (int(button_mode_gesture.get_width()*1.1),int(button_mode_gesture.get_height()*1.1)))

button_mode_mouse =  pygame.image.load(os.path.join('Utils/Pics/Interface/ModeOfGame','Mode_Mouse.png'))
button_mode_mouse_enlarge = pygame.transform.scale(button_mode_mouse, (int(button_mode_mouse.get_width()*1.1),int(button_mode_mouse.get_height()*1.1)))

def check_mode_playbutton( ):
	global value, right_click
	i=0
	mouse = pygame.mouse.get_pos()

	mode = None
	
	if 50 <= mouse[0] <= 170 and 150 <= mouse[1] <= 310:
		if right_click:
			mode = 1
	elif 320 <= mouse[0] <= 440 and 150 <= mouse[1] <= 310:
		if right_click:
			mode = 2
	elif 215 <= mouse[0] <= 285 and 355 <= mouse[1] <= 425:
		if right_click:
			mode = 3
	elif 185 <= mouse[0] <= 310 and 280 <= mouse[1] <= 320:
		if right_click:
			mode = 4
	else:
		mode = None
		
	clock = pygame.time.Clock()		
	clock.tick(main.speed)		
	pygame.display.update()
	return mode

def check_mode_pausebutton( ):
	global value, right_click
	i=0
	mouse = pygame.mouse.get_pos()

	mode = None
	
	if 170 <= mouse[0] <= 330 and 150 <= mouse[1] <= 200:
		if right_click:
			mode = 1
	elif 170 <= mouse[1] <= 330 and 250 <= mouse[1] <= 300:
		if right_click:
			mode = 2
	elif 215 <= mouse[0] <= 285 and 355 <= mouse[1] <= 425 :
			if right_click:
				mode = 3
	else:
		mode = None
		
	clock = pygame.time.Clock()		
	clock.tick(main.speed)		
	pygame.display.update()
	return mode

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


def display_playbutton() :

	global win, cursor
	global mute_button, unmute_button
	
	main.speed = 60		# fps
	main.run = True
	
	
	# Home screen interface
	width, height = 500,450
	win = pygame.display.set_mode((width, height))	
	pygame.display.set_caption('Play Button Interface')

	cursor = Cursor()

	clock = pygame.time.Clock()

	# Hide the original cursor
	pygame.mouse.set_visible(False)

	pop_sound_play = False

	#Music Variable
	Music_Background = pygame.mixer.music.load(os.path.join('Utils\Music\BGmusic_Level1.wav'))
	pygame.mixer.music.play(-1)

	i = 0
	while i<1000:

		mode = check_mode_playbutton( )
		if mode == 3: 
			interface_module.display_buttons()
			break 	# breaks interface loop
		elif mode == 2 or mode == 1 :
			display_pausebutton()
			break
		elif mode == 4:
			display_instructions()
			break

		win.fill((255,0,0))
		win.blit(screen_home,(0,0))
		win.blit(button_mode_gesture, (50,150))
		win.blit(button_mode_mouse,(330,150))
		win.blit(button_instructions_small, (185,280))
		win.blit(button_home_small,(210,350))

		event_loop()

		mouse = pygame.mouse.get_pos()
		
		if 50 <= mouse[0] <= 170 and 150 <= mouse[1] <= 310 :
			if right_click == 0:
				win.blit(button_mode_gesture_enlarge, (50,140))
			if pop_sound_play == False:
				music_module.sound_button_enlarge.play()
			pop_sound_play = True

		elif 330 <= mouse[0] <= 450 and 150 <= mouse[1] <= 310 :
			if right_click == 0:
				win.blit(button_mode_mouse_enlarge, (320,140))
			if pop_sound_play == False:
				music_module.sound_button_enlarge.play()
			pop_sound_play = True

		elif 185 <= mouse[0] <= 310 and 280 <= mouse[1] <= 320 :
			if right_click == 0:
				win.blit(button_instructions, (170,280))
			if pop_sound_play == False:
				music_module.sound_button_enlarge.play()
			pop_sound_play = True
		
		elif 215 <= mouse[0] <= 285 and 355 <= mouse[1] <= 425 :
			if right_click == 0:
				win.blit(button_home_enlarge, (205,340))
			if pop_sound_play == False:
				music_module.sound_button_enlarge.play()
			pop_sound_play = True
			
		i=i+1
		cursor.draw()

		pygame.display.update()

	pygame.mouse.set_visible(False)
    
def display_pausebutton() :

	global win, cursor
	global mute_button, unmute_button
	
	main.speed = 60		# fps
	main.run = True
	
	
	# Home screen interface
	width, height = 500,450
	win = pygame.display.set_mode((width, height))	
	pygame.display.set_caption('Pause Button Interface')

	cursor = Cursor()

	clock = pygame.time.Clock()

	# Hide the original cursor
	pygame.mouse.set_visible(False)

	pop_sound_play = False

	#Music Variable
	Music_Background = pygame.mixer.music.load(os.path.join('Utils\Music\BGmusic_Level1.wav'))
	pygame.mixer.music.play(-1)

	i = 0
	while i<1000:

		mode = check_mode_pausebutton( )
		if mode == 1: 
			interface_module.display_buttons()
			break 	# breaks interface loop
	

		win.fill((255,0,0))
		win.blit(screen_home,(0,0))
		win.blit(button_resume, (170,150))
		win.blit(button_restart,(170,250))
		win.blit(button_home_small,(210,350))

		event_loop()

		mouse = pygame.mouse.get_pos()
		
		if 170 <= mouse[0] <= 330 and 150 <= mouse[1] <= 200 :
			if right_click == 0:
				win.blit(button_resume_enlarge, (165,150))
			if pop_sound_play == False:
				music_module.sound_button_enlarge.play()
			pop_sound_play = True

		elif 170 <= mouse[0] <= 330 and 250 <= mouse[1] <= 300 :
			if right_click == 0:
				win.blit(button_restart_enlarge, (165,250))
			if pop_sound_play == False:
				music_module.sound_button_enlarge.play()
			pop_sound_play = True
		
		elif 215 <= mouse[0] <= 285 and 355 <= mouse[1] <= 425 :
			if right_click == 0:
				win.blit(button_home_enlarge, (205,340))
			if pop_sound_play == False:
				music_module.sound_button_enlarge.play()
			pop_sound_play = True
			
		i=i+1
		cursor.draw()

		pygame.display.update()

	pygame.mouse.set_visible(False)
    
	
def display_instructions():

	global win, cursor
	global mute_button, unmute_button
	
	main.speed = 60		# fps
	main.run = True
	
	
	# Home screen interface
	width, height = 800,600
	win = pygame.display.set_mode((width, height))	
	pygame.display.set_caption('Instructions Interface')
	cursor = Cursor()

	clock = pygame.time.Clock()

	# Hide the original cursor
	pygame.mouse.set_visible(False)

	pop_sound_play = False

	#Music Variable
	Music_Background = pygame.mixer.music.load(os.path.join('Utils\Music\BGmusic_Level1.wav'))
	pygame.mixer.music.play(-1)

	i = 0
	while i<1000:	
		win.fill((255,255,255))

		win.blit(screen_home,(0,0))
		win.blit(button_skip,(620,515))

		event_loop()

		mouse = pygame.mouse.get_pos()

		if 620 <= mouse[0] <= 780 and 515 <= mouse[1] <= 565 :
			if right_click == 0:
				win.blit(button_skip_enlarge, (610,515))
			if pop_sound_play == False:
				music_module.sound_button_enlarge.play()
			pop_sound_play = True

		else:
			pop_sound_play = False				

		cursor.draw()   # should be at last, to avoid overlapping

		i = i+1

		clock.tick(main.speed)
		pygame.display.update()

		
	
	# Bring back the original cursor
	pygame.mouse.set_visible(True)
