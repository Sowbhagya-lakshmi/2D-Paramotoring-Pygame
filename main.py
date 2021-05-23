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

from module import background_module
from module import bird_module
from module import coins_module
from module import display_module
from module import event_module
from module import effects_module
from module import foreground_module
from module import obstacles_module
from module import player_module

# Global variables
speed = 60		# fps
run = True
game_duration = 30 # in sec

pygame.init()

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
	coins_module.coin_board = coins_module.coin_board.convert_alpha()
	
	player_module.Player.imgs = [img.convert_alpha() for img in player_module.player.imgs]
	coins_module.Coin.resized_imgs = [img.convert_alpha() for img in coins_module.Coin.resized_imgs]

	obstacles_module.Tree.resized_imgs = [img.convert_alpha() for img in obstacles_module.Tree.resized_imgs]
	obstacles_module.Rock_n_Bush.resized_imgs = [img.convert_alpha() for img in obstacles_module.Rock_n_Bush.resized_imgs]	

	effects_module.Coin_spark_effects.imgs = [img.convert_alpha() for img in effects_module.Coin_spark_effects.imgs]

	display_module.heart = display_module.heart.convert_alpha()
	display_module.line = display_module.line.convert_alpha()
	display_module.start = display_module.start.convert_alpha()
	display_module.finish = display_module.finish.convert_alpha()
	
	bird_module.Bird.list_of_lists = [[img.convert_alpha() for img in lst] for lst in bird_module.Bird.list_of_lists]

def draw_all_objects():
	"""
	Draws the background, foreground, obstacles and coins.
	"""
	background_module.draw_bg(win)
	obstacles_module.draw_obstacles(win)
	coins_module.draw_coins(win)
	foreground_module.draw_fg(win)
	for spark_object in effects_module.Coin_spark_effects.effects_list:
		spark_object.draw(win)

	player_module.draw_player(win)
	bird_module.draw_bird(win)
	display_module.display_lives(win, num_of_lives)
	display_module.draw_progression_bar(win,frame_count)


# MAIN ALGORITHM
if __name__ == '__main__':

	change_img_pixel_format()

	clock = pygame.time.Clock()
	event_module.setting_up_events()
	frame_count = 0
	count = 0
	num_of_lives = 3

	'''
	frame_count = 0	# chk fps
	start_time = time.time()'''
	
	#Music Variable
	Music_Background = pygame.mixer.music.load(os.path.join('Utils\Music\BG1music.wav'))
	pygame.mixer.music.play(-1)

	# GAME LOOP
	while run:
		#frame_count += 1
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
		collision_with_bird = bird_module.collision_with_bird(player_module.player)

		if collision_occured or collision_with_bird:		# Dummy exit
			music_module.Sound_Collided.play()
			num_of_lives -= 1
			if num_of_lives == 0:
				time.sleep(1)
				break

		clock.tick(speed)
		pygame.display.update()
	
		'''if frame_count >= (game_duration-10)*speed:	# Last 10 seconds of game
			#print('ending')
			event_module.level_end(win, count)'''

		if frame_count >= game_duration*speed:
			print('Game Over')
			time.sleep(1)
			break
 
		
		'''now = time.time()	# chck fps
		if now-start_time >=5:
			start_time = time.time()
			print(frame_count//5)
			frame_count = 0
		frame_count += 1'''
		
