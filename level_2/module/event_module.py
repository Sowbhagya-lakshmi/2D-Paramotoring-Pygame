import pygame
import sys
import time

from level_2.module import bird_module
from level_2.module import dynamic_obstacle_olaf
from level_2.module import dynamic_obstacle_santa
from level_2.module import dynamic_obstacle_giftbox
from level_2.module import coins_module
from level_2.module import obstacles_module
from level_2.mp import process_object



right_click = False

def setting_up_events():
	# Generate coin once in every 1 seconds
	pygame.time.set_timer(pygame.USEREVENT+1, 800)
	# Generate tree obstacles once in every 8 seconds
	pygame.time.set_timer(pygame.USEREVENT+2, 6000)
	# Generate rock and bush obstacles once in every 20 seconds
	pygame.time.set_timer(pygame.USEREVENT+3, 8000)
	# Generate bird obstacle once in every 8 seconds
	pygame.time.set_timer(pygame.USEREVENT+4, 8000)
	#generate reindeer obstacles
	pygame.time.set_timer(pygame.USEREVENT+5, 20000)
	#generate santa obstacles
	pygame.time.set_timer(pygame.USEREVENT+6, 28000)
	#generate giftbox obstacles
	pygame.time.set_timer(pygame.USEREVENT+7, 40000)

	pygame.event.set_blocked(None)
	pygame.event.set_allowed([pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN,pygame.QUIT, pygame.USEREVENT+2, pygame.USEREVENT+3, pygame.USEREVENT+4,  pygame.USEREVENT+5, pygame.USEREVENT+6])

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
			obstacles_module.create_tree_obstacle()
		if event.type == pygame.USEREVENT+3:
			obstacles_module.create_rock_n_bush()
		if event.type == pygame.USEREVENT+4:
			bird_module.create_bird()
		if event.type == pygame.USEREVENT+5:
			dynamic_obstacle_olaf.create_olaf()
		if event.type == pygame.USEREVENT+6:
			dynamic_obstacle_santa.create_santa()
		if event.type == pygame.USEREVENT+7:
			dynamic_obstacle_giftbox.create_gift()
		

