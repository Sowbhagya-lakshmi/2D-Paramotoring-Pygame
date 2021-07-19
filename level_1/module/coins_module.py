import os
import pygame
import random

from level_1.module import background_module
from level_1.module import effects_module
from level_1.module import foreground_module
from level_1.module import obstacles_module

free_zone_y = 0

class Coin:
	"""
	Describes coin object. Draw method draws the coin, and animates it.
	"""
	# Loading coin images
	num_of_imgs = 6
	resized_imgs = [pygame.image.load(os.path.join(r'level_1/Utils/Pics/Coins/', "coin"+ str(x) + '.png')) for x in range(1, num_of_imgs+1)]

	coins_list = []
	num_coins_collected = 0

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.run_count = 0

	def draw(self, win):	
		self.frames_per_image = 3			# each coin image is drawn for 7 consecutive frames
		if self.run_count >= self.frames_per_image*self.num_of_imgs:
			self.run_count = 0
		self.index = self.run_count//self.frames_per_image
		self.run_count += 1

		# coin image
		self.img = self.resized_imgs[self.index]

		# Coins to rotate about it's central y axis
		self.centroid_x = self.img.get_width()//2
		win.blit(self.img, (self.x-self.centroid_x,self.y))


# Coin collection board
coin_board1 = pygame.image.load(os.path.join(r'level_1/Utils/Pics/Display','coin_display.png'))
coin_board = pygame.transform.scale(coin_board1, (int(coin_board1.get_width()//1.5), int(coin_board1.get_height()//1.5)))

def find_free_zone_y():
	"""
	To determine free space inorder to place coins. To prevent coins being drawn over obstacles.
	"""
	global free_zone_y
	free_zone_y = foreground_module.ground_y

	for obstacle in obstacles_module.Rock_n_Bush.obstacles:
		if obstacle.x >(background_module.bg.get_width() - obstacle.width) and obstacle.x < background_module.bg.get_width():
			free_zone_y =  obstacle.y
	for obstacle in obstacles_module.Tree.obstacles:
		if obstacle.x >(background_module.bg.get_width() - obstacle.width) and obstacle.x < background_module.bg.get_width():
			free_zone_y =  obstacle.y

	return free_zone_y
def create_coin():
	"""
	Creates a coin in the free space. 
	"""
	free_zone_y = find_free_zone_y()	# find free space in y axis
	x = random.randint(50,free_zone_y)	# choose random y value within free zone
	Coin.coins_list.append(Coin(background_module.bg.get_width(), x))

def draw_coins(win):
	for coin in Coin.coins_list:
		coin.draw(win)
	update_coins_position()
	
def update_coins_position():
	"""
	Updates the x coordinates of coins. If coin goes offscreen, remove it from the list.
	"""
	for coin in Coin.coins_list:
		coin_width = coin.resized_imgs[0].get_width()
		if coin.x < -1*coin_width: # If coin goes offscreen, removing it from coins list 
			Coin.coins_list.remove(coin)
		else:
			coin.x -= foreground_module.foreground_speed

def coin_collection(player):
	"""
	Collision with coin is checked using Pixel perfect collision method. If collision occurs returns True, else False.
	Collision is checked only if coin is near the player to save computation.
	"""
	for coin in Coin.coins_list:
		try:
			if coin.x < (player.x + player.img.get_width()) and (coin.x + coin.img.get_width()) > player.x:			# Check x range
				if coin.y < (player.y + player.img.get_height()) and (coin.y + coin.img.get_height()) > player.y:	# Check y range
					player_mask = pygame.mask.from_surface(player.img)
					coin_mask = pygame.mask.from_surface(coin.img)
					offset = coin.x - player.x, coin.y - player.y
					collision_point = player_mask.overlap(coin_mask, offset)		# returns collision point else returns None
					if collision_point:
						Coin.coins_list.remove(coin)	# Stop drawing
						effects_module.Coin_spark_effects.coin_effects_list.append(effects_module.Coin_spark_effects(coin.x, coin.y))	# create a spark object
						return True
		except: pass
	return False

def display_num_coins_collected(win):
	"""
	To display the number of coins collected.
	"""
	win.blit(coin_board, (10,10))
	font_size = 40
	font = pygame.font.Font(r'level_1\Utils\Font\FreeSansBold.ttf', font_size)
	text_x_pos, text_y_pos = 80, 10
	text = font.render(str(Coin.num_coins_collected), True, (255,255,255))
	win.blit(text, (text_x_pos, text_y_pos))