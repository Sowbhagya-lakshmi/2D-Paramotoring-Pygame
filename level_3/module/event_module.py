import sys
import time

import pygame

import global_config
from level_3.module import coins_module
from level_3.module import display_module
from level_3.module import dragon_module
from level_3.module import ghost_module
from level_3.module import obstacles_module
from level_3.module import shark_module
from level_3.mp import process_object

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
	
	# Spawn objects after countdown and 8 seconds before level completion
	if frame_count > 4*global_config.fps and frame_count < (total_number_of_frames - 8*global_config.fps):
		custom_event_loop(frame_count)
	
	# Countdown
	if frame_count < 4*global_config.fps:
			display_module.countdown.draw(win)

def custom_event_loop(frame_count):
	"""
	Generates coins and obstacles
	"""
	# Event 1 - Generate coin once in every 0.5 seconds
	if (frame_count/global_config.fps) % 0.5 == 0:
		coins_module.create_coin()

	# Event 2 - Generate house obstacles once in every 6 seconds
	if (frame_count/global_config.fps) % 5 == 0:
		obstacles_module.create_house_obstacle()
	
	# Event 3 - Generate tree once in every 10 seconds
	if (frame_count/global_config.fps) % 9 == 0:
		obstacles_module.create_tree()

	# Event 4 - Generate dragon obstacle once in every 9.5 seconds
	if (frame_count/global_config.fps) % 9.5 == 0:
		dragon_module.create_dragon()

	# Event 5 - Generate ghost obstacle once in every 16 seconds
	if (frame_count/global_config.fps) % 14 == 0:
		ghost_module.create_ghost()

	# Event 6 - Generate shark obstacle once in every 12.5 seconds
	if (frame_count/global_config.fps) % 11.5 == 0:
		shark_module.create_shark()

