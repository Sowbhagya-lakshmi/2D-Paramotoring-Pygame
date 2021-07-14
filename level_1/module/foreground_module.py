import os
import pygame

import global_config

# Ground
ground = pygame.image.load(os.path.join(r'level_1/Utils/Pics/Foreground','ground.png'))
ground_x = 0
ground_y = global_config.window_height-ground.get_height() 
ground_width = ground.get_width() - 10	# Treating the image to be shorter in width by 10 pixels to prevent glitches
foreground_speed = 6 	# Foreground shifts by 6 pixels in each game loop

def draw_fg(win):
	"""
	Draws the foreground onto the screen. The scalar 10 is used to treat the image to be shorter in width by 10 pixels to prevent glitches.
	"""
	global ground_x, ground_width
	# Drawing ground
	win.blit(ground, (ground_x+10, ground_y))
	win.blit(ground, (ground_width+10,ground_y))	

	# Ground movement
	ground_x -= foreground_speed
	ground_width -= foreground_speed
	
	# For repetition of ground movement
	if ground_x < (ground.get_width() - 10) * -1:
		ground_x = (ground.get_width() - 10)
	if ground_width < (ground.get_width() - 10) * -1:
		ground_width = (ground.get_width() - 10)