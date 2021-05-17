
import pygame
import time


# Global variables
speed = 60		# fps
run = True
collision_occured = False

pygame.init()

#Sound Variables
CollisionSound = pygame.mixer.Sound('CollidedSound.wav')
BirdSound = pygame.mixer.Sound('BirdSound.wav')
CoinSound = pygame.mixer.Sound('CoinsSound.wav')

#Music Variable
Backgroundmusic = pygame.mixer.music.load('BG1music.wav')
pygame.mixer.music.play(-1) 

# Game Window
width, height = 1550,800
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Game Window')

def draw_all_objects():
	"""
	Draws the background, foreground, obstacles and coins.
	"""
	bg_module.draw_bg(win)
	obstacles_module.draw_obstacles(win)
	coins_module.draw_coins(win)
	fg_module.draw_fg(win)
	player_module.draw_player(win)

# MAIN ALGORITHM
if __name__ == '__main__':
	import player_module
	import bg_module
	import fg_module
	import coins_module
	import obstacles_module
	import event_module

	clock = pygame.time.Clock()
	event_module.setting_up_events()

	'''
	frame_count = 0	# chck fps
	start_time = time.time()'''

	# GAME LOOP
	while run:
		draw_all_objects()
		event_module.event_loop()

		# Coin collection
		collected = coins_module.coin_collection(player_module.player)	# Checks collision and returns bool 
		if collected:
			CoinSound.play()
			coins_module.Coin.num_coins_collected += 1
		coins_module.display_num_coins_collected(win)

		# Collision with Obstacles
		collision_occured = obstacles_module.collision_with_obstacle(player_module.player)	# Checks collision and returns bool 
		if collision_occured:		# Dummy exit
			CollisionSound.play()
			time.sleep(1)
			break

		clock.tick(speed)
		pygame.display.update()

		'''
		now = time.time()	# chck fps
		if now-start_time >=5:
			start_time = time.time()
			print(frame_count//5)
			frame_count = 0
		frame_count += 1
		'''
