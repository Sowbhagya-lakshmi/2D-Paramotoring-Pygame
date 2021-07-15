import pygame
import sys
import time

from level_3.module import dragon_module
from level_3.module import ghost_module
from level_3.module import shark_module
from level_3.module import coins_module
from level_3.module import obstacles_module
from level_3.mp import process_object



right_click = False

def setting_up_events():
	# Generate coin once in every 1 seconds
	pygame.time.set_timer(pygame.USEREVENT+1, 1250)
	# Generate house obstacles once in every 8 seconds
	pygame.time.set_timer(pygame.USEREVENT+2, 6000)
	# Generate tree once in every 20 seconds
	pygame.time.set_timer(pygame.USEREVENT+3, 10000)
	# Generate dragon obstacle once in every 8 seconds
	pygame.time.set_timer(pygame.USEREVENT+4, 9500)
	# Generate ghost obstacle once in every 8 seconds
	pygame.time.set_timer(pygame.USEREVENT+5, 16000)
	# Generate shark obstacle once in every 8 seconds
	pygame.time.set_timer(pygame.USEREVENT+6, 12500)

	pygame.event.set_blocked(None)
	pygame.event.set_allowed([pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN,pygame.QUIT, pygame.USEREVENT+2, pygame.USEREVENT+3, pygame.USEREVENT+4, pygame.USEREVENT+5, pygame.USEREVENT+6])

def event_loop():
	global right_click

	right_click =  False

	for event in pygame.event.get():		
		if event.type == pygame.QUIT:
			if process_object.is_alive():
				process_object.terminate()
				time.sleep(1)
			pygame.quit()
			sys.exit()		
		elif event.type == pygame.KEYDOWN:
			if event.key == 27:		# press esc to quit
				if process_object.is_alive():
					process_object.terminate()
					time.sleep(1)
				pygame.quit()
				sys.exit()		
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				right_click = True

		if event.type == pygame.USEREVENT+1:
			coins_module.create_coin()
		if event.type == pygame.USEREVENT+2:
			obstacles_module.create_house_obstacle()
		if event.type == pygame.USEREVENT+3:
			obstacles_module.create_tree()
		if event.type == pygame.USEREVENT+4:
			dragon_module.create_dragon()
		if event.type == pygame.USEREVENT+5:
			ghost_module.create_ghost()
		if event.type == pygame.USEREVENT+6:
			shark_module.create_shark()

