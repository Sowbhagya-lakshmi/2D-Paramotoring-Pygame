import math
import os
import pygame
import random
import sys
import time

class Player:
	"""
	Descibes the player object.
	It has info such as the x positon, y position, width, height, contour coordinates and
	a draw method to draw the player's images onto the screen hence creating the animation effect.
	"""
	# Loading player images
	num_of_player_imgs = 9
	imgs = [pygame.image.load(os.path.join('Utils/Pics/Player/', "player-"+ str(x) + '.png')) for x in range(1, num_of_player_imgs+1)]

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.runCount = 0

	def draw(self, win):
		self.frames_per_image = 7			# each player image is drawn for 7 consecutive frames
		if self.runCount > self.frames_per_image*self.num_of_player_imgs :
			self.runCount = 0
		self.img = self.imgs[self.runCount//self.num_of_player_imgs]
		win.blit(self.img, (self.x,self.y))
		self.runCount += 1 

class Tree:
	"""
	Describes tree objects. Currently it contains 3 types of trees. It contains the x position, y position, contour coordinates of tree.
	Also contains a draw method to draw the tree onto the screen. The type of tree that is to be created can be determined using tree_num variable.
	"""
	# Loading images 
	num_of_tree_imgs = 11
	imgs = [pygame.image.load(os.path.join('Utils/Pics/Obstacles/', "tree"+ str(x) + '.png')) for x in range(0, num_of_tree_imgs)]
	resized_imgs = [pygame.transform.scale(img, (int(img.get_width()//1.5), int(img.get_height()//1.5))) for img in imgs]

	def __init__(self, x, y, tree_num):
		self.x = x
		self.y = y
		self.tree_num = tree_num

		# Width and height of obstacle
		self.width = self.resized_imgs[self.tree_num].get_width()
		self.width = self.resized_imgs[self.tree_num].get_height()

	# Draws the obstacle onto the screen
	def draw(self,win):
		self.img = self.resized_imgs[self.tree_num]
		win.blit(self.img, (self.x, self.y)) 

class Rock:
	"""
	Describes rock objects. It contains the x position, y position, contour coordinates of rocks.
	Also contains a draw method to draw the tree onto the screen.
	"""
	# Loading images 
	num_of_rock_imgs = 2
	imgs = [pygame.image.load(os.path.join('Utils/Pics/Obstacles/', "rock"+ str(x) + '.png')) for x in range(0, num_of_rock_imgs)]
	resized_imgs = [pygame.transform.scale(img, (int(img.get_width()*2), int(img.get_height()*2))) for img in imgs]

	def __init__(self, x, y, rock_num):
		self.x = x
		self.y = y
		self.rock_num = rock_num

		# Width and height of obstacle
		self.width = self.resized_imgs[self.rock_num].get_width()
		self.width = self.resized_imgs[self.rock_num].get_height()

	# Draws the obstacle onto the screen
	def draw(self,win):
		self.img = self.resized_imgs[self.rock_num]
		win.blit(self.img, (self.x, self.y))


class Coin:
	"""
	Describes coin object.
	"""
	# Loading coin images
	num_of_coin_imgs = 6
	imgs = [pygame.image.load(os.path.join('Utils/Pics/Coins/', "coin"+ str(x) + '.png')) for x in range(1, num_of_coin_imgs+1)]
	resized_imgs = [pygame.transform.scale(img, (int(img.get_width()//50), int(img.get_height()//50))) for img in imgs]

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.runCount = 0

	def draw(self, win):	
		self.frames_per_image = 3			# each coin image is drawn for 7 consecutive frames
		if self.runCount >= self.frames_per_image*self.num_of_coin_imgs:
			self.runCount = 0
		self.index = self.runCount//self.frames_per_image
		self.runCount += 1

		# coin image
		self.img = self.resized_imgs[self.index]

		# Coins to rotate about it's central y axis
		self.centroid_x = self.img.get_width()//2
		win.blit(self.img, (self.x-self.centroid_x,self.y))

# HELPER FUNCTIONS

# Draws the background, foreground and obstacles
def draw_scene_and_obstacles(bg_x, bg_width, ground_x, ground_width):
	# Drawing background
	win.blit(bg, (bg_x, 0))
	win.blit(bg, (bg_width,0))

	# Background movement
	bg_x -= background_speed
	bg_width -= background_speed
	
	# For repetition of background movement
	if bg_x < bg.get_width() * -1:
		bg_x = bg.get_width()
	if bg_width < bg.get_width() * -1:
		bg_width = bg.get_width()

	# Drawing obstacles
	for rock in rocks:
		rock.draw(win)
	for obstacle in obstacles:
		obstacle.draw(win)

	# Draw coins
	for coin in coins:
		coin.draw(win)

	# Drawing ground
	win.blit(ground, (ground_x, 0))
	win.blit(flipped_ground, (ground_width,0))	

	# Ground movement
	ground_x -= foreground_speed
	ground_width -= foreground_speed
	
	# For repetition of ground movement
	if ground_x < (ground.get_width()-5) * -1:
		ground_x = (ground.get_width()-5)
	if ground_width < (flipped_ground.get_width()-5) * -1:
		ground_width = (flipped_ground.get_width()-5)

	return bg_x, bg_width, ground_x, ground_width

# Creates a random obstacle from the available list of obstacles
def create_random_obstacle():
	y_coordinate_obstacle = 300
	random_num = random.randrange(0,Tree.num_of_tree_imgs)       	# range over the number of obstacles
	random_x = random.randint(bg.get_width(), bg.get_width()+500)   # random inital x position of obstacle
	# Add new obstacle to obstacles list
	obstacles.append(Tree(random_x,y_coordinate_obstacle,random_num))

def update_obstacle_position():
	for obstacle in obstacles:
		if obstacle.x < -1*obstacle.width: # If obstacle goes offscreen, removing it from obstacles list 
			obstacles.remove(obstacle)
		else:
			obstacle.x -= foreground_speed

def collision_with_obstacle():
	player_mask = pygame.mask.from_surface(player.img)
	for obstacle in obstacles:
		if obstacle.x < (player.x + player.img.get_width()+10):	# Checking for collision if near player
			obstacle_mask = pygame.mask.from_surface(obstacle.img)
			offset = obstacle.x - player.x, obstacle.y - player.y
			boolean = player_mask.overlap(obstacle_mask, offset)
			if boolean:
				print(boolean)
				return True
	return False

def create_rock_obstacle():
	y_coordinate_obstacle = 150
	random_num = random.randrange(0,Rock.num_of_rock_imgs)       	# range over the number of obstacles
	random_x = random.randint(bg.get_width(), bg.get_width()+500)   # random inital x position of obstacle
	# Add new obstacle to obstacles list
	rocks.append(Rock(random_x,y_coordinate_obstacle,random_num))

def update_rock_position():
	for rock in rocks:
		if rock.x < -1*rock.width: # If obstacle goes offscreen, removing it from obstacles list 
			rocks.remove(rock)
		else:
			rock.x -= foreground_speed

def collision_with_rock():
	player_mask = pygame.mask.from_surface(player.img)
	for rock in rocks:
		if rock.x < (player.x + player.img.get_width()+10):	# Checking for collision if near player
			rock_mask = pygame.mask.from_surface(rock.img)
			offset = rock.x - player.x, rock.y - player.y
			boolean = player_mask.overlap(rock_mask, offset)
			if boolean:
				return True
	return False

def find_free_zone_y():
	y_coordinate_obstacle = 300
	rock_y_coordinate_obstacle = 100
	free_zone_y = max_y_coord

	for obstacle in obstacles:
		if obstacle.x >(bg.get_width() - obstacle.width) and obstacle.x < bg.get_width():
			free_zone_y =  y_coordinate_obstacle
	for rock in obstacles:
		if rock.x >(bg.get_width() - rock.width) and rock.x < bg.get_width():
			free_zone_y =  rock_y_coordinate_obstacle

	return free_zone_y

def create_coin():
	free_zone_y = find_free_zone_y()	# find free space in y axis
	#print(free_zone_y)
	x = random.randint(50,free_zone_y)	# choose random y value within free zone
	coins.append(Coin(bg.get_width(), x))

def update_coins_position():
	for coin in coins:
		coin_width = coin.imgs[0].get_width()
		if coin.x < -1*coin_width: # If coin goes offscreen, removing it from coins list 
			coins.remove(coin)
		else:
			coin.x -= foreground_speed

def coin_collection():
	player_mask = pygame.mask.from_surface(player.img)
	for coin in coins:
		try:
			if coin.x < (player.x + player.img.get_width()+10):	# Checking for collision if near player
				coin_mask = pygame.mask.from_surface(coin.img)
				offset = coin.x - player.x, coin.y - player.y
				boolean = player_mask.overlap(coin_mask, offset)
				if boolean:
					coins.remove(coin)
					return True
		except: pass
	return False

def display_num_coins_collected():
	win.blit(coin_board, (10,10))
	font = pygame.font.Font('freesansbold.ttf', 40)
	text_x, text_y = 80, 20
	text = font.render(str(num_coins_collected), True, (255,255,255))
	win.blit(text, (text_x, text_y))


def display_mouse_pointer_coordinates(mx,my):
	font = pygame.font.Font('freesansbold.ttf', 32)
	text_x, text_y = 1400, 10
	text = font.render(str(mx)+', '+str(my), True, (0,0,0))
	win.blit(text, (text_x, text_y))

def display_collision_message():
	font = pygame.font.Font('freesansbold.ttf', 100)
	text_x, text_y = 750, 100
	text = font.render('COLLISION', True, (0,0,0))
	win.blit(text, (text_x, text_y))




# MAIN ALGORITHM

pygame.init()

# Game Window
width, height = 1550, 800
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Game Window')

# Background Image
bg = pygame.image.load(os.path.join('Utils/Pics/Background','bg.png')).convert()
bg_x = 0
bg_width = bg.get_width()  
background_speed = 2	# Background shifts by 2 pixels in each game loop

# Ground
ground = pygame.image.load(os.path.join('Utils/Pics/Foreground','ground.png'))
flipped_ground = pygame.transform.flip(ground, True, False)
ground_x = 0
ground_width = ground.get_width() - 5	# To prevent glitches in background movement...yet to find an optimal solution
foreground_speed = 6 	# Foreground shifts by 6 pixels in each game loop

# Coin collection board
coin_board1 = pygame.image.load(os.path.join('Utils/Pics/Display','coin_display.png'))
coin_board = pygame.transform.scale(coin_board1, (int(coin_board1.get_width()//1.5), int(coin_board1.get_height()//1.5)))
coins = []
num_coins_collected = 0

speed = 60			# fps
max_y_coord = 560	# player's y axis limit
run = True

collision_occured = False
rock_collision_occured = False
obstacles = []
rocks = []

player = Player(250, 313)	# Creating an instance of the class Player

clock = pygame.time.Clock()

# Setting a userevent once in every 3 seconds to generate coin
pygame.time.set_timer(pygame.USEREVENT+1, 2000)

# Setting a userevent once in every 8 seconds to generate tree obstacles
pygame.time.set_timer(pygame.USEREVENT+2, 8000)

# Setting a userevent once in every 20 seconds to generate rock obstacles
pygame.time.set_timer(pygame.USEREVENT+3, 10000)

'''
frame_count = 0
start_time = time.time()'''

# GAME LOOP
while run:
	# Draws stuff to be displayed in window
	bg_x, bg_width, ground_x, ground_width = draw_scene_and_obstacles(bg_x, bg_width, ground_x, ground_width)
	
	# Get mouse pointer coordinates
	(mx, my) = pygame.mouse.get_pos()

	# Display mouse pointer coordinates for reference
	display_mouse_pointer_coordinates(mx,my)
	   	
	# limit player's movable region
	if my < 560 :
		player.x, player.y = 250, my
		player.draw(win)
	else:
		player.x, player.y = 250, max_y_coord
		player.draw(win)
	
	# Event loop
	for event in pygame.event.get():
		
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
			run = False
		
		if event.type == pygame.KEYDOWN:
			if event.key == 27:		# press esc to quit
				pygame.quit()
				sys.exit()
				run = False
		
		if event.type == pygame.USEREVENT+1:
			create_coin()
		if event.type == pygame.USEREVENT+2:
			create_random_obstacle()
		if event.type == pygame.USEREVENT+3:
			create_rock_obstacle()
	
	update_obstacle_position()
	update_coins_position()
	collision_occured = collision_with_obstacle()	# Checks collision and returns bool 

	update_rock_position()
	rock_collision_occured = collision_with_rock()

	if collision_occured or rock_collision_occured:		# Dummy exit
		display_collision_message()
		pygame.display.update()
		time.sleep(3)
		break

	collected = coin_collection()	# Checks collision and returns bool 

	if collected:
		num_coins_collected += 1

	display_num_coins_collected()

	clock.tick(speed)
	pygame.display.update()

	'''now = time.time()
	if now-start_time >=1:
		start_time = time.time()
		print(frame_count)
		frame_count = 0
	frame_count += 1'''

