import pygame
import sys
import time

import global_config
from level_2.module import bird_module
from level_2.module import display_module
from level_2.module import dynamic_obstacle_olaf
from level_2.module import dynamic_obstacle_santa
from level_2.module import dynamic_obstacle_giftbox
from level_2.module import coins_module
from level_2.module import obstacles_module
from level_2.mp import process_object



right_click = False
total_number_of_frames = global_config.fps*global_config.game_duration

def setting_up_events():

	pygame.event.set_blocked(None)
	pygame.event.set_allowed([pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN,pygame.QUIT])

def event_loop(frame_count, win):
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
		
	if frame_count > 4*global_config.fps and frame_count < (total_number_of_frames - 8*global_config.fps):
		custom_event_loop(frame_count)
	
	if frame_count < 4*global_config.fps:
			display_module.countdown.draw(win)

def custom_event_loop(frame_count):
	"""
	Generates coins, trees, bushes, rocks and birds
	"""
	# Event 1 - Generate coin once in every 0.75 seconds
	if (frame_count/global_config.fps)%0.75 == 0:
		coins_module.create_coin()

	# Event 2 - Generate tree obstacles once in every 6 seconds
	if (frame_count/global_config.fps)%6 == 0:
		obstacles_module.create_tree_obstacle()

	# Event 3 - Generate rock and bush obstacles once in every 7 seconds
	if (frame_count/global_config.fps)%7 == 0:
		obstacles_module.create_rock_n_bush()

	# Event 4 - Generate bird obstacle once in every 8 seconds
	if (frame_count/global_config.fps)%8 == 0:
		bird_module.create_bird()
	
	# Event 5 - Generate Reindeer obstacles once in every 20 seconds
	if (frame_count/global_config.fps)%20 == 0:
		dynamic_obstacle_olaf.create_olaf()

	# Event 6 - Generate Santa Claus once in every 28 seconds
	if (frame_count/global_config.fps)%28 == 0:
		dynamic_obstacle_santa.create_santa()

	# Event 7 - Generate Gift box obstacle once in every 40 seconds
	if (frame_count/global_config.fps)%40 == 0:
		dynamic_obstacle_giftbox.create_gift()
		

