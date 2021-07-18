import os
import pygame
import time

import global_config
from level_2.module import background_module
from level_2.module import bird_module
from level_2.module import coins_module
from level_2.module import display_module
from level_2.module import effects_module
# from level_2.module import ending_module
from level_2.module import event_module
from level_2.module import foreground_module
from level_2.module import interface_module

from level_2.module import interface_screens_module
from level_2.module import music_module
from level_2.module import obstacles_module
from level_2.module import player_module
from level_2.module import dynamic_obstacle_olaf
from level_2.module import dynamic_obstacle_santa
from level_2.module import dynamic_obstacle_giftbox

from level_2.mp import process_object
from level_2.module.interface_screens_module import check_index
from level_2.module.interface_screens_module import display_no_hand_info
from level_2.module.interface_screens_module import display_fail_msg
from level_2.module.interface_screens_module import display_success_msg

from level_2.mp import queue_shared
from level_2.module.player_movement_box import draw_control_screen_actual, draw_player_position

# Global variables
run = True

frame_count = 0
num_of_lives = 3
fuel_count = 0
ending_count = 0

won_bool = False
fuel_available = global_config.speed*60
start_fuel = False

display_pop_up = False
collected_map = False

lost_music_count = 0

win = None
game_window = None

def create_game_window():
	global win, game_window
	
	# Game Window
	game_window = pygame.display.set_mode((global_config.window_width, global_config.window_height), pygame.RESIZABLE)
	pygame.display.set_caption('Game Window')

	# Title and icon
	pygame.display.set_caption('Para Escapade')
	icon =  pygame.image.load(r'level_1\Utils\Pics\Display\icon.png')   # loading into code
	pygame.display.set_icon(icon)   # to display
	
	# Copy of game window which will be later resized according to the resolution, and blit onto the original game window.
	win = game_window.copy()

def change_img_pixel_format():
	"""
	Creates a new copy of the Surface which will have the same pixel format as
	the display Surface. Necessary for blitting images to the screen faster.
	"""
	background_module.bg = background_module.bg.convert()
	background_module.snow = background_module.snow.convert_alpha()

	foreground_module.ground = foreground_module.ground.convert_alpha()
	
	player_module.Player.imgs = [img.convert_alpha() for img in player_module.player.imgs]
	player_module.Propeller.propeller_imgs = [img.convert_alpha() for img in player_module.Propeller.propeller_imgs]

	coins_module.Coin.resized_imgs = [img.convert_alpha() for img in coins_module.Coin.resized_imgs]
	coins_module.coin_board = coins_module.coin_board.convert_alpha()

	obstacles_module.Tree.resized_imgs = [img.convert_alpha() for img in obstacles_module.Tree.imgs]
	obstacles_module.Rock_n_Bush.imgs = [img.convert_alpha() for img in obstacles_module.Rock_n_Bush.imgs]	

	effects_module.Coin_spark_effects.imgs = [img.convert_alpha() for img in effects_module.Coin_spark_effects.imgs]
	effects_module.Hit_effects.imgs = [img.convert_alpha() for img in effects_module.Hit_effects.imgs]

	display_module.heart = display_module.heart.convert_alpha()
	display_module.line = display_module.line.convert_alpha()
	display_module.start = display_module.start.convert_alpha()
	display_module.finish = display_module.finish.convert_alpha()
	display_module.fuel_bar.img_icon = display_module.fuel_bar.img_icon.convert_alpha()

	for fuel in display_module.Fuel.fuel_list:
		fuel.img = fuel.img.convert_alpha()
	for extra_life in display_module.Extra_life.extra_lives_list:
		extra_life.img = extra_life.img.convert_alpha()
	
	dynamic_obstacle_giftbox.Gift.imgs_list = [img.convert_alpha() for img in dynamic_obstacle_giftbox.Gift.imgs_list]
	dynamic_obstacle_santa.Santa.imgs_list = [img.convert_alpha() for img in dynamic_obstacle_santa.Santa.imgs_list]
	dynamic_obstacle_olaf.Olaf.imgs_list = [img.convert_alpha() for img in dynamic_obstacle_olaf.Olaf.imgs_list]
	bird_module.Bird.list_of_lists = [[img.convert_alpha() for img in lst] for lst in bird_module.Bird.list_of_lists]
	
def draw_all_objects():
	"""
	Draws the background, foreground, obstacles, coins, special effects, player, bird, lives, minimap.
	"""
	global fuel_available

	background_module.draw_bg(win)
	background_module.draw_snow(win)
	obstacles_module.draw_obstacles(win)
	coins_module.draw_coins(win)
	foreground_module.draw_fg(win)

	for spark_object in effects_module.Coin_spark_effects.coin_effects_list:
		spark_object.draw(win)
	for hit_effect_object in effects_module.Hit_effects.hit_effects_list:
		hit_effect_object.draw(win)

	if num_of_lives == 0:
		player_module.player.y += 1
		player_module.propeller.draw(win)
		player_module.player.draw(win)
	elif won_bool:
		player_module.draw_player(win, True)
	else:
		player_module.draw_player(win)
		
	bird_module.draw_bird(win)
	dynamic_obstacle_giftbox.draw_gift(win)
	dynamic_obstacle_olaf.draw_olaf(win)
	dynamic_obstacle_santa.draw_santa(win)
	display_module.display_lives(win, num_of_lives)
	display_module.draw_minimap(win,frame_count)

	if start_fuel:
		fuel_available -= 1
	fuel_available = display_module.fuel_bar.draw_fuel_bar(win, fuel_available, start_fuel)

	display_module.draw_fuel(win)
	cursor.draw(win)

def lost():
	"""
	The player falls if all three lives are lost
	"""
	foreground_module.foreground_speed = 0
	background_module.background_speed = 0
	display_fail_msg(win)

	if player_module.player.y > foreground_module.ground_y:
		try:
			process_object.terminate()
		except: pass
		interface_module.display_endscreen()
		return True
	return False

def won():
	"""
	If the player 
	"""
	display_success_msg(win)
	foreground_module.foreground_speed = 0
	background_module.background_speed = 0
	
# MAIN ALGORITHM
def main(volume_button_on_status):
	global bool_val
	global collected_map
	global cursor
	global frame_count
	global lost_music_count
	global num_of_lives
	global start_fuel
	global won_bool

	pygame.init()

	interface_screens_module.display_playbutton()

	# Game window
	create_game_window()

	change_img_pixel_format()

	clock = pygame.time.Clock()
	pygame.event.clear()
	event_module.setting_up_events()
	cursor = interface_module.Cursor()
	pygame.mouse.set_visible(False)
	
	#Music Variable
	pygame.mixer.music.load(os.path.join(r'level_2\Utils\Music\BGmusic_Level2.wav'))
	if volume_button_on_status:
		pygame.mixer.music.play(-1)

	total_num_of_frames = global_config.speed*global_config.game_duration

	# GAME LOOP
	while run:
		frame_count += 1
		
		draw_all_objects()
		
		if frame_count == 4*global_config.speed:
			start_fuel = True
		
		event_module.event_loop(frame_count, win)

		# Coin collection
		collected = coins_module.coin_collection(player_module.player)	# Returns bool 
		if collected:
			if volume_button_on_status:
				music_module.sound_coins.play()
			coins_module.Coin.num_coins_collected += 1
		coins_module.display_num_coins_collected(win)

		# Extra life
		num_of_coins_inexchange_for_life = 50
		if coins_module.Coin.num_coins_collected%num_of_coins_inexchange_for_life == 0 and num_of_lives!=3:
			display_module.create_extra_life()

		# Extra life collection
		elif coins_module.Coin.num_coins_collected > num_of_coins_inexchange_for_life:
			for extra_life in display_module.Extra_life.extra_lives_list:
				extra_life.draw(win)	
				bool = extra_life.check_collision()
				if bool:
					num_of_lives += 1
					display_module.Extra_life.extra_lives_list.remove(extra_life)
					coins_module.Coin.num_coins_collected -= num_of_coins_inexchange_for_life
		
		# Display black reference screen only if hand gesture mode is selected
		if process_object.is_alive():
			draw_control_screen_actual(win)
			draw_player_position(win)		     

		try:
			# Check if index finger is detected
			bool_val = check_index(queue_shared)
			if bool_val and num_of_lives > 0:
				display_pop_up = True
				start_loop = 0

			# If not detected display pop up
			if display_pop_up:
				start_loop += 1
				display_no_hand_info(win)

				# Display the no hand info for 0.5 seconds
				if start_loop >= global_config.speed//2:	
					display_pop_up = False
		except:
			pass

		# Collision with Obstacles
		collision_with_obstacle = obstacles_module.collision_with_obstacle()	# Checks collision and Returns bool 
		collision_with_bird = bird_module.collision_with_bird()
		collision_with_olaf = dynamic_obstacle_olaf.collision_with_olaf()
		collision_with_santa = dynamic_obstacle_santa.collision_with_santa()
		collision_with_gift = dynamic_obstacle_giftbox.collision_with_gift()


		if collision_with_obstacle or collision_with_bird or collision_with_olaf or collision_with_santa or collision_with_gift:		# Dummy exit
			if volume_button_on_status:
				music_module.sound_collided.play()
			num_of_lives -= 1
			if num_of_lives <= 0:
				num_of_lives = 0
		
		# Player loses if he runs out of lives or fuel
		if num_of_lives == 0 or fuel_available <= 0:

			lost_music_count += 1
			if lost_music_count == 1:

				if volume_button_on_status:
					pygame.mixer.music.stop()
					music_module.sound_aftercollided.play()
									
			game_end = lost()
			player_module.propeller.frames_per_propeller_img += 0.01	# propeller slows down

			# If the player has fallen to the ground
			if game_end:
				break

		if frame_count > total_num_of_frames - 10*global_config.speed:	#last 10 seconds
			collected_map = display_module.display_map(win)

		if frame_count > total_num_of_frames - 5*global_config.speed:	#last 5 seconds
			won()
			won_bool = True

		# Resize and blit the copy of game window onto main game window
		game_window.blit(pygame.transform.scale(win, game_window.get_rect().size), (0,0))

		clock.tick(global_config.speed)
		pygame.display.update()

		# Dummy exit
		if collected_map:
			pygame.mixer.music.fadeout(2000)	# Fades out the background music
			time.sleep(2)
			try:
				process_object.terminate()
			except: pass

			return_bool = interface_module.display_winscreen()
			if return_bool:
				break

	pygame.quit()	
			

			