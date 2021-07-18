import os
import random

import pygame

from level_3.module import background_module
from level_3.module import effects_module
from level_3.module import foreground_module
from level_3.module import obstacles_module

free_zone_y = 0

class Coin:
	"""
	Describes coin object. Draw method draws the coin, and animates it.
	"""
	# Loading coin images
	num_of_imgs = 8
	list_of_lists = []

	path = r'level_3/Utils/Pics/Coins/'
	colour_list = os.listdir(path)
	num_of_colours = len(colour_list)

	for colour in colour_list:
		if colour == 'Effects': continue
		imgs = []
		for x in range(num_of_imgs):
			img = pygame.image.load(os.path.join(path, colour +"/"+ str(x) + '.png'))
			resized_img = pygame.transform.scale(img, (int(img.get_width()*1.5), int(img.get_height()*1.5)))
			imgs.append(resized_img)
		list_of_lists.append(imgs)

	# imgs = [pygame.image.load(os.path.join(r'level_3/Utils/Pics/Coins/', str(x) + '.png')) for x in range(num_of_imgs)]
	# resized_imgs = [pygame.transform.scale(img, (int(img.get_width()*1.5), int(img.get_height()*1.5))) for img in imgs]

	del imgs
	coins_list = []
	num_coins_collected = 0

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.run_count = 0
		self.colour_num = random.randrange(0, len(self.list_of_lists))
		# print('self.num_of_colours-1: ',self.num_of_colours-1)

	def draw(self, win):	
		self.frames_per_image = 3			# each coin image is drawn for 7 consecutive frames
		if self.run_count >= self.frames_per_image*self.num_of_imgs:
			self.run_count = 0
		self.index = self.run_count//self.frames_per_image
		self.run_count += 1

		# coin image
		# print(self.colour_num)
		self.img = self.list_of_lists[self.colour_num][self.index]

		# Coins to rotate about it's central y axis
		self.centroid_x = self.img.get_width()//2
		win.blit(self.img, (self.x-self.centroid_x,self.y))


# Coin collection board
coin_board1 = pygame.image.load(os.path.join(r'level_3/Utils/Pics/Display','coin_display.png'))
coin_board = pygame.transform.scale(coin_board1, (int(coin_board1.get_width()/1.7), int(coin_board1.get_height()/1.7)))

def find_free_zone_y():
	"""
	To determine free space inorder to place coins. To prevent coins being drawn over obstacles.
	"""
	global free_zone_y
	free_zone_y = foreground_module.ground_y

	for obstacle in obstacles_module.Tree.obstacles:
		if obstacle.x >(background_module.bg.get_width() - obstacle.width) and obstacle.x < background_module.bg.get_width():
			free_zone_y =  obstacle.y
	for obstacle in obstacles_module.House.obstacles:
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
		coin_width = coin.list_of_lists[0][0].get_width()
		if coin.x < -1*coin_width: # If coin goes offscreen, removing it from coins list 
			Coin.coins_list.remove(coin)
		else:
			coin.x -= foreground_module.foreground_speed

def coin_collection(player):
	"""
	Collision with coin is checked using Pixel perfect collision method. If collision occurs returns True, else False.
	Collision is checked only if coin is near the player to save computation.
	"""
	player_mask = pygame.mask.from_surface(player.img)
	for coin in Coin.coins_list:
		try:
			if coin.x < (player.x + player.img.get_width()) and (coin.x + coin.img.get_width()) > player.x:			# Check x range
				if coin.y < (player.y + player.img.get_height()) and (coin.y + coin.img.get_height()) > player.y:	# Check y range
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
	win.blit(coin_board, (10,5))
	font_size = 40
	font = pygame.font.Font(r'level_1\Utils\Font\FreeSansBold.ttf', font_size)
	text_x_pos, text_y_pos = 80, 10
	text = font.render(str(Coin.num_coins_collected), True, (0,0,0))
	win.blit(text, (text_x_pos, text_y_pos))