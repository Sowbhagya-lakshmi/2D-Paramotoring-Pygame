import pygame
import sys
import os
import multiprocessing
from multiprocessing import Queue
from module.gesture_control import main_avm


import main
from module import music_module , interface_module


win = None
cursor = None

right_click = False
value = 0

#Loading Button and Screen Images
screen_home =  pygame.image.load(os.path.join('Utils/Pics/Interface','Para Escapade.png'))
screen_playbutton_interface =  pygame.image.load(os.path.join('Utils/Pics/Interface','Screen_PlayButton.png'))
screen_pausebutton_interface =  pygame.image.load(os.path.join('Utils/Pics/Interface','Screen_PauseButton.png'))
screen_aboutbutton_interface =  pygame.image.load(os.path.join('Utils/Pics/Interface','Screen_AboutButton.png'))

screen_instruction1 =  pygame.image.load(os.path.join('Utils/Pics/Interface/Instructions','Instructions_screen1.png'))
screen_instruction2 =  pygame.image.load(os.path.join('Utils/Pics/Interface/Instructions','Instructions_screen2.png'))
screen_instruction3 =  pygame.image.load(os.path.join('Utils/Pics/Interface/Instructions','Instructions_screen3.png'))
screen_instruction4 =  pygame.image.load(os.path.join('Utils/Pics/Interface/Instructions','Instructions_screen4.png'))

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

index_finger_not_detected = pygame.image.load(os.path.join('Utils/Pics/Interface','INDEX_FINGeR_NOT_DETECTED.png'))


queue_shared = multiprocessing.Queue()
process_object = multiprocessing.Process(target = main_avm, args = (queue_shared,))

def check_mode_playbutton( ):
	"""
	Checks the button that is clicked from the play button interface and returns 1 if Hand Gesture mode
	of game is clicked,2 if Mouse control mode of game is clicked,3 if home button is clicked and 4 if 
	instructions button is clicked

	"""
	global right_click
	i=0
	mouse = pygame.mouse.get_pos()

	play_mode = None
	
	if 50 <= mouse[0] <= 170 and 150 <= mouse[1] <= 310:
		if right_click:
			play_mode = 1
	elif 320 <= mouse[0] <= 440 and 150 <= mouse[1] <= 310:
		if right_click:
			play_mode = 2
	elif 215 <= mouse[0] <= 285 and 355 <= mouse[1] <= 435:
		if right_click:
			play_mode = 3
	elif 185 <= mouse[0] <= 310 and 280 <= mouse[1] <= 320:
		if right_click:
			play_mode = 4
	else:
		play_mode = None
		
	clock = pygame.time.Clock()		
	clock.tick(main.speed)		
	pygame.display.update()
	return play_mode

def check_mode_pausebutton( ):
	"""
	Checks the button that is clicked from the pause button interface and returns 1 if resume button is
	clicked, 2 if restart button is clicked, and 3 if home button is clicked
	"""
	global right_click
	mouse = pygame.mouse.get_pos()

	pause_mode = None
	
	if 170 <= mouse[0] <= 330 and 150 <= mouse[1] <= 200:
		if right_click:
			pause_mode = 1
	
	elif 170 <= mouse[1] <= 330 and 250 <= mouse[1] <= 300:
		if right_click:
			pause_mode = 2
	elif 215 <= mouse[0] <= 285 and 355 <= mouse[1] <= 425 :
		if right_click:
			pause_mode = 3
	else:
		pause_mode = None
		
	clock = pygame.time.Clock()		
	clock.tick(main.speed)		
	pygame.display.update()
	return pause_mode

def check_mode_instructions( ):
	"""
	Checks if the skip button is clicked from the instructions button interface and returns 1 if skip button is
	clicked
	"""
	global right_click
	mouse = pygame.mouse.get_pos()

	skip_mode = None
	
	if 620 <= mouse[0] <= 780 and 515 <= mouse[1] <= 565 :
		if right_click:
			skip_mode = 1
	else:
		skip_mode = None
		
	clock = pygame.time.Clock()		
	clock.tick(main.speed)		
	pygame.display.update()
	return skip_mode


def check_mode_aboutbutton( ):
	"""
	Checks if the skip button is clicked from the about button and returns  1 if skip button is clicked
	"""
	global right_click
	i=0
	mouse = pygame.mouse.get_pos()

	about_mode = None
	
	if 365 <= mouse[0] <= 435 and 523 <= mouse[1] <= 587:
			if right_click: 
				about_mode = 1
	
	else:
		about_mode = None
		
	clock = pygame.time.Clock()		
	clock.tick(main.speed)		
	pygame.display.update()
	return about_mode

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


def display_playbutton():
	"""
	Creates a screen when we click the play button to choose the mode of the game 
	"""
	global win, cursor
	
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
	i=0
	

	while i<1000:

		mode = check_mode_playbutton( )

		if mode == 1:	
			process_object.start()
			pass
		
		elif mode == 3: 
			interface_module.display_homescreen()
			break 	# breaks interface loop
		
		elif mode == 4:
			display_instructions()
			break

		win.fill((255,0,0))
		win.blit(screen_playbutton_interface,(0,0))
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
    
def display_pausebutton():
	"""
	Creates a screen when we click the pause button from the game screen
	"""
	global win, cursor
	
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

	while True:

		pause_mode = check_mode_pausebutton( )
		if pause_mode == 3: 
			interface_module.display_homescreen()
			break 	# breaks interface loop
		elif pause_mode == 1:
			display_playbutton()
			break

		win.fill((255,0,0))
		win.blit(screen_pausebutton_interface,(0,0))
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
			
	
		cursor.draw()

		pygame.display.update()

	pygame.mouse.set_visible(False)
    
	
def display_instructions():
	"""
	Creates a screen when we click instructions screen. Contains Instructions related to the game
	"""

	global win, cursor
	
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

	
	while True:	
		win.fill((255,255,255))
		win.blit(screen_instruction1,(0,0))
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

def display_aboutbutton():
	"""
	Creates a screen a when we click About button
	"""
	global win, cursor
	
	main.speed = 60		# fps
	main.run = True
	
	
	# Home screen interface
	width, height = 800,600
	win = pygame.display.set_mode((width, height))	
	pygame.display.set_caption('About Button Interface')

	cursor = Cursor()

	clock = pygame.time.Clock()

	# Hide the original cursor
	pygame.mouse.set_visible(False)

	pop_sound_play = False

	#Music Variable
	Music_Background = pygame.mixer.music.load(os.path.join('Utils\Music\BGmusic_Level1.wav'))
	pygame.mixer.music.play(-1)

	while True:

		about_mode = check_mode_aboutbutton()
		if about_mode == 1:
			interface_module.display_homescreen()
			break 	# breaks interface loop

		mouse = pygame.mouse.get_pos()

		win.fill((255,0,0))
		win.blit(screen_aboutbutton_interface,(0,0))
		win.blit(button_home_small,(365,520))

		event_loop()

		if 365 <= mouse[0] <= 435 and 522 <= mouse[1] <= 587 :
			if right_click == 0:
				win.blit(button_home_enlarge, (360,515))
			if pop_sound_play == False:
				music_module.sound_button_enlarge.play()
			pop_sound_play = True
			
		cursor.draw()

		pygame.display.update()

	pygame.mouse.set_visible(False)

def check_index(queue_shared):
	#queue.get()
	if queue_shared.empty():
		#print("*")
		return False
	else:
		queue_shared.get()
		# print("----------------------------------------------------------------------------------------------------------------------------------------------------------------")
		return True
		
		
def display_no_hand_info(win):
	win.blit(index_finger_not_detected,(300,300))
	# pygame.display.update()
	#time.sleep(2)


