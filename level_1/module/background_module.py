import os
import pygame

# Background Image
bg = pygame.image.load(os.path.join(r'level_1/Utils/Pics/Background','bg.png'))
bg_x = 0
bg_width = bg.get_width() - 3 	# Consequent background images overlap by 3 pixels
background_speed = 2			# Background shifts by 2 pixels in each game loop

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