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
button_instructions_click =  pygame.image.load(os.path.join('Utils/Pics/Interface/Buttons','Button_Instructions_click.png'))

button_home =  pygame.image.load(os.path.join('Utils/Pics/Interface','Button_Home.png'))
button_home_small = pygame.transform.scale(button_home, (int(button_home.get_width()*0.7),int(button_home.get_height()*0.7)))
button_home_click =  pygame.image.load(os.path.join('Utils/Pics/Interface','Button_Home_click.png'))

button_mode_gesture =  pygame.image.load(os.path.join('Utils/Pics/Interface/ModeOfGame','Mode_HandGesture.png'))
button_mode_gesture_enlarge = pygame.transform.scale(button_mode_gesture, (int(button_mode_gesture.get_width()*1.1),int(button_mode_gesture.get_height()*1.1)))
button_mode_gesture_click =  pygame.image.load(os.path.join('Utils/Pics/Interface/ModeOfGame','Mode_HandGesture_click.png'))

button_mode_mouse =  pygame.image.load(os.path.join('Utils/Pics/Interface/ModeOfGame','Mode_Mouse.png'))
button_mode_mouse_enlarge = pygame.transform.scale(button_mode_mouse, (int(button_mode_mouse.get_width()*1.1),int(button_mode_mouse.get_height()*1.1)))
button_mode_mouse_click =  pygame.image.load(os.path.join('Utils/Pics/Interface/ModeOfGame','Mode_Mouse_click.png'))

def check_mode(screen):
	global value, right_click
	i=0
	mouse = pygame.mouse.get_pos()
	
	if 50 <= mouse[0] <= 170 and 150 <= mouse[1] <= 310:
		if right_click:
			while i<50:
				screen.blit(button_mode_gesture_click, (50,150))
				i +=1
			mode = 1
	if 320 <= mouse[1] <= 440 and 150 <= mouse[1] <= 310:
		if right_click:
			while i<50:
				screen.blit(button_mode_mouse_click, (330,150))
				i +=1
			mode = 2
	elif 215 <= mouse[0] <= 285 and 355 <= mouse[1] <= 425 :
			if right_click:
				while z<10:
					win.blit(button_home_click,(210,350))
					z = z+1
				mode = 3
		
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

		mode = check_mode(win)
		if mode == 3: 
			interface_module.display_buttons()
			break 	# breaks interface loop
	

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
				win.blit(button_home, (200,340))
			if pop_sound_play == False:
				music_module.sound_button_enlarge.play()
			pop_sound_play = True
			
		i=i+1
		cursor.draw()

		pygame.display.update()

	pygame.mouse.set_visible(False)
    


