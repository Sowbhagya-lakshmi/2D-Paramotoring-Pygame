import os
import pygame

import global_config

# Ground
ground = pygame.image.load(os.path.join(r'level_2/Utils/Pics/Foreground','ground.png'))
ground_x = 0
ground_y = global_config.window_height-ground.get_height() 
ground_width = ground.get_width() - 5	# To prevent glitches in background movement...WIP
foreground_speed = 6 	# Foreground shifts by 6 pixels in each game loop

def draw_fg(win):
	global ground_x, ground_width
	# Drawing ground
	win.blit(ground, (ground_x, ground_y))
	win.blit(ground, (ground_width,ground_y))	

	# Ground movement
	ground_x -= foreground_speed
	ground_width -= foreground_speed
	
	# For repetition of ground movement
	if ground_x < (ground.get_width()-5) * -1:
		ground_x = (ground.get_width()-5)
	if ground_width < (ground.get_width()-5) * -1:
		ground_width = (ground.get_width()-5)