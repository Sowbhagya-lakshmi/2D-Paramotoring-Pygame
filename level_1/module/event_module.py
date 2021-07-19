import sys
import pygame
import time

import global_config
from level_1.module import bird_module
from level_1.module import coins_module
from level_1.module import display_module
from level_1.module import obstacles_module
from level_1.multiprocessing_module import process_object

right_click = False
total_number_of_frames = global_config.fps*global_config.game_duration

def setting_up_events():
	pygame.event.set_blocked(None)
	pygame.event.set_allowed([pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN,pygame.QUIT])

def event_loop(frame_count, win, lost_music_count):
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
	
	# Spawn objects after countdown and 8 seconds before level completion
	if frame_count > 4*global_config.fps and frame_count < (total_number_of_frames - 8*global_config.fps) and lost_music_count == 0:
		custom_event_loop(frame_count)
	
	# Countdown
	if frame_count < 4*global_config.fps:
			display_module.countdown.draw(win)
		
def custom_event_loop(frame_count):
	"""
	Generates coins, trees, bushes, rocks and birds
	"""
	# Event 1 - Generate coin once in every 0.5 seconds
	if (frame_count/global_config.fps)%0.5 == 0:
		coins_module.create_coin()

	# Event 2 - Generate tree obstacles once in every 4 seconds
	if (frame_count/global_config.fps)%4 == 0:
		obstacles_module.create_tree_obstacle()

	# Event 3 - Generate rock and bush obstacles once in every 8 seconds
	if (frame_count/global_config.fps)%8 == 0:
		obstacles_module.create_rock_n_bush()

	# Event 4 - Generate bird obstacle once in every 8 seconds
	if (frame_count/global_config.fps)%7 == 0:
		bird_module.create_bird()


