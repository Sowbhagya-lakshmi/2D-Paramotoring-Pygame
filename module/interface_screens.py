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

screen_home =  pygame.image.load(os.path.join('Utils/Pics/Interface','Para Escapade.png'))

button_mode_gesture =  pygame.image.load(os.path.join('Utils/Pics/Interface/ModeOfGame','Mode_HandGesture.png'))
button_mode_mouse =  pygame.image.load(os.path.join('Utils/Pics/Interface/ModeOfGame','Button_Mouse.png'))

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
	width, height = 400,400
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

    while True:

        event_loop()

        win.fill((255,255,255))
        win.blit(screen_home,(0,0))
        win.blit(button_mode_gesture, (320,100))
        win.blit(button_mode_mouse, (320,200))
        
       
		mouse = pygame.mouse.get_pos()

        cursor.draw()   # should be at last, to avoid overlapping

        pygame.display.update()

		
	
	# Bring back the original cursor
    pygame.mouse.set_visible(True)


