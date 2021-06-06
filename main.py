import pygame
import time
import os

from module import background_module
from module import coins_module
from module import event_module
from module import foreground_module
from module import obstacles_module
from module import player_module
from module import music_module
from module import interface_module

# Global variables
speed = 60		# fps
run = True
collision_occured = False

pygame.init()

interface_module.display_buttons()

# Game Window
width, height = 1550,800
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Game Window')

def change_img_pixel_format():
	"""
	Creates a new copy of the Surface which will have the same pixel format as
	the display Surface. Necessary for blitting images to the screen faster.
	"""
	background_module.bg = background_module.bg.convert()
	foreground_module.ground = foreground_module.ground.convert_alpha()
	foreground_module.flipped_ground = foreground_module.flipped_ground.convert_alpha()
	coins_module.coin_board = coins_module.coin_board.convert_alpha()
	
	player_module.Player.imgs = [img.convert_alpha() for img in player_module.player.imgs]
	coins_module.Coin.resized_imgs = [img.convert_alpha() for img in coins_module.Coin.resized_imgs]

	obstacles_module.Tree.resized_imgs = [img.convert_alpha() for img in obstacles_module.Tree.resized_imgs]
	obstacles_module.Rock_n_Bush.resized_imgs = [img.convert_alpha() for img in obstacles_module.Rock_n_Bush.resized_imgs]	

def draw_all_objects():
	"""
	Draws the background, foreground, obstacles and coins.
	"""
	background_module.draw_bg(win)
	obstacles_module.draw_obstacles(win)
	coins_module.draw_coins(win)
	foreground_module.draw_fg(win)
	player_module.draw_player(win)

# MAIN ALGORITHM
if __name__ == '__main__':
	change_img_pixel_format()

	clock = pygame.time.Clock()
	event_module.setting_up_events()

	'''
	frame_count = 0	# chk fps
	start_time = time.time()'''
	
	#Music Variable
	Music_Background = pygame.mixer.music.load(os.path.join('Utils\Music\BGmusic_Level1.wav'))
	pygame.mixer.music.play(-1)

	# GAME LOOP
	while run:
		draw_all_objects()
		event_module.event_loop()

		# Coin collection
		collected = coins_module.coin_collection(player_module.player)	# Checks collision and returns bool 
		if collected:
			music_module.Sound_Coins.play()
			coins_module.Coin.num_coins_collected += 1
		coins_module.display_num_coins_collected(win)

		# Collision with Obstacles
		collision_occured = obstacles_module.collision_with_obstacle(player_module.player)	# Checks collision and returns bool 
		if collision_occured:		# Dummy exit
			music_module.Sound_Collided.play()
			time.sleep(1)
			break

		clock.tick(speed)
		pygame.display.update()

		'''
		now = time.time()	# chk fps
		if now-start_time >=5:
			start_time = time.time()
			print(frame_count//5)
			frame_count = 0
		frame_count += 1
		'''
