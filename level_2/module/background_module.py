import os

import pygame

# Background Image
bg = pygame.image.load(os.path.join(r'level_2/Utils/Pics/Background','bg.png'))
bg_x = 0
bg_width = bg.get_width() - 3 
background_speed = 2	# Background shifts by 2 pixels in each game loop

def draw_bg(win):
	global bg_x, bg_width
	win.blit(bg, (bg_x + 3, 0))
	win.blit(bg, (bg_width + 3,0))

	# Background movement
	bg_x -= background_speed
	bg_width -= background_speed
	
	# For repetition of background movement
	if bg_x < (bg.get_width()-3) * -1:
		bg_x = (bg.get_width()-3)
	if bg_width < (bg.get_width()-3) * -1:
		bg_width = (bg.get_width()-3)
		
	# Background Image
snow = pygame.image.load(os.path.join(r'level_2/Utils/Pics/Background','bg2.png'))
bg_y = 0
bg_height = snow.get_height()  
snow_speed = 2	# Background shifts by 2 pixels in each game loop

def draw_snow(win):
	global bg_y, bg_height
	win.blit(snow, (0, bg_y))
	win.blit(snow, (0,bg_height))

	# Background movement
	bg_y += snow_speed
	bg_height += snow_speed
	
	# For repetition of background movement
	if bg_y > snow.get_height()*1:
		bg_y = snow.get_height()*-1
	if bg_height > snow.get_height() * 1:
		bg_height =snow.get_height()*-1
