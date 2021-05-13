import math
import os
import pygame
import random
import sys
import time

pygame.init()

# Game Window
width, height = 1550,800
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Game Window')

# Background Image
bg = pygame.image.load(os.path.join('Utils/Pics/Background','bg.png')).convert()
bg_x = 0
bg_width = bg.get_width()  
background_speed = 2	# Background shifts by 2 pixels in each game loop

# Ground
ground = pygame.image.load(os.path.join('Utils/Pics/Foreground','ground.png')).convert_alpha()
flipped_ground = pygame.transform.flip(ground, True, False)
ground_x = 0
ground_width = ground.get_width() - 5	# To prevent glitches in background movement...yet to find an optimal solution
foreground_speed = 6 	# Foreground shifts by 6 pixels in each game loop

# Coin collection board
coin_board1 = pygame.image.load(os.path.join('Utils/Pics/Display','coin_display.png')).convert_alpha()
coin_board = pygame.transform.scale(coin_board1, (int(coin_board1.get_width()//1.5), int(coin_board1.get_height()//1.5)))
coins = []
num_coins_collected = 0

class Player:
	"""
	Descibes the player object.
	It has info such as the x positon, y position, width, height and a draw method to draw the player's images onto the screen hence creating the animation effect.
	"""
	# Loading player images
	num_of_player_imgs = 9
	imgs = [pygame.image.load(os.path.join('Utils/Pics/Player/', "player-"+ str(x) + '.png')).convert_alpha() for x in range(1, num_of_player_imgs+1)]

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
	Describes tree objects. Currently it contains 11 types of trees. It contains the x position, y position of tree.
	Also contains a draw method to draw trees onto the screen. The type of tree that is to be created can be determined using num variable.
	"""
	# Loading images 
	num_of_imgs = 11
	imgs = [pygame.image.load(os.path.join('Utils/Pics/Obstacles/', "tree"+ str(x) + '.png')).convert_alpha() for x in range(0, num_of_imgs)]
	resized_imgs = [pygame.transform.scale(img, (int(img.get_width()//1.5), int(img.get_height()//1.5))) for img in imgs]

	obstacles = []


	def __init__(self, x, y, num):
		self.x = x
		self.y = y
		self.num = num

		# Width and height of obstacle
		self.width = self.resized_imgs[self.num].get_width()
		self.width = self.resized_imgs[self.num].get_height()

	# Draws the obstacle onto the screen
	def draw(self,win):
		self.img = self.resized_imgs[self.num]
		win.blit(self.img, (self.x, self.y)) 

class Other_obstacles:
	"""
	Describes other obstacle objects. Contains rocks and shrubs. It contains the x position, y position. The various obstacles are created using num variable.
	Also contains a draw method to draw the tree onto the screen.
	"""
	# Loading images 
	num_of_imgs = 2
	imgs = [pygame.image.load(os.path.join('Utils/Pics/Obstacles/', "obstacle"+ str(x) + '.png')).convert_alpha() for x in range(0, num_of_imgs)]
	resized_imgs = [pygame.transform.scale(img, (int(img.get_width()*2), int(img.get_height()*2))) for img in imgs]

	obstacles = []

	def __init__(self, x, y, num):
		self.x = x
		self.y = y
		self.num = num

		# Width and height of obstacle
		self.width = self.resized_imgs[self.num].get_width()
		self.width = self.resized_imgs[self.num].get_height()

	# Draws the obstacle onto the screen
	def draw(self,win):
		self.img = self.resized_imgs[self.num]
		win.blit(self.img, (self.x, self.y))

class Coin:
	"""
	Describes coin object. Draw method draws the coin, and animates it.
	"""
	# Loading coin images
	num_of_imgs = 6
	imgs = [pygame.image.load(os.path.join('Utils/Pics/Coins/', "coin"+ str(x) + '.png')).convert_alpha() for x in range(1, num_of_imgs+1)]
	resized_imgs = [pygame.transform.scale(img, (int(img.get_width()//50), int(img.get_height()//50))) for img in imgs]

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.runCount = 0

	def draw(self, win):	
		self.frames_per_image = 3			# each coin image is drawn for 7 consecutive frames
		if self.runCount >= self.frames_per_image*self.num_of_imgs:
			self.runCount = 0
		self.index = self.runCount//self.frames_per_image
		self.runCount += 1

		# coin image
		self.img = self.resized_imgs[self.index]

		# Coins to rotate about it's central y axis
		self.centroid_x = self.img.get_width()//2
		win.blit(self.img, (self.x-self.centroid_x,self.y))

# HELPER FUNCTIONS

def draw_scene_and_obstacles():
	"""
	Draws the background, foreground, obstacles and coins.
	"""
	global bg_x, bg_width, ground_x, ground_width
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
	for obstacle in Other_obstacles.obstacles:
		obstacle.draw(win)
	for obstacle in Tree.obstacles:
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


def create_tree_obstacle():
	"""
	Creates a random tree obstacle.
	"""
	y_coordinate_obstacle = 310
	random_num = random.randrange(0,Tree.num_of_imgs)       	# range over the number of obstacles
	random_x = random.randint(bg.get_width(), bg.get_width()+500)   # random inital x position of obstacle
	# Add new obstacle to obstacles list
	Tree.obstacles.append(Tree(random_x,y_coordinate_obstacle,random_num))

def create_other_obstacle():
	"""
	Creates a random obstacle.
	"""
	y_coordinate_obstacle = 150
	random_num = random.randrange(0,Other_obstacles.num_of_imgs)       	# range over the number of obstacles
	random_x = random.randint(bg.get_width(), bg.get_width()+500)   # random inital x position of obstacle
	# Add new obstacle to obstacles list
	Other_obstacles.obstacles.append(Other_obstacles(random_x,y_coordinate_obstacle,random_num))

def update_obstacle_position():
	"""
	Creates the moving effect. If obstacle goes offscreen, removes it from obstacles list"
	"""
	for element in obstacle_classes:
		for obstacle in element.obstacles:
			if obstacle.x < -1*obstacle.width: 
				element.obstacles.remove(obstacle)
			else:
				obstacle.x -= foreground_speed

def collision_with_obstacle():
	"""
	Pixel perfect collision implemented using masks. Checks for collision of mask of player against other
	obstacles only if the obstacle is near to the player. Returns True if collision occurred, else False.
	"""
	player_mask = pygame.mask.from_surface(player.img)
	for element in obstacle_classes:
		for obstacle in element.obstacles:
			if obstacle.x < (player.x + player.img.get_width()+10):	# Checking for collision if near player
				obstacle_mask = pygame.mask.from_surface(obstacle.img)
				offset = obstacle.x - player.x, obstacle.y - player.y
				boolean = player_mask.overlap(obstacle_mask, offset)
				if boolean:
					return True
	return False


def find_free_zone_y():
	"""
	To determine free space inorder to place coins. To prevent coins being drawn over obstacles.
	"""
	y_coordinate_obstacle1 = 310
	y_coordinate_obstacle2 = 150
	free_zone_y = max_y_coord

	for obstacle in Tree.obstacles:
		if obstacle.x >(bg.get_width() - obstacle.width) and obstacle.x < bg.get_width():
			free_zone_y =  y_coordinate_obstacle1
	for rock in Other_obstacles.obstacles:
		if rock.x >(bg.get_width() - rock.width) and rock.x < bg.get_width():
			free_zone_y =  y_coordinate_obstacle2

	return free_zone_y

def create_coin():
	"""
	Creates a coin in the free space. 
	"""
	free_zone_y = find_free_zone_y()	# find free space in y axis
	x = random.randint(50,free_zone_y)	# choose random y value within free zone
	coins.append(Coin(bg.get_width(), x))

def update_coins_position():
	"""
	Updates the x coordinates of coins. If coin goes offscreen, remove it from the list.
	"""
	for coin in coins:
		coin_width = coin.imgs[0].get_width()
		if coin.x < -1*coin_width: # If coin goes offscreen, removing it from coins list 
			coins.remove(coin)
		else:
			coin.x -= foreground_speed

def coin_collection():
	"""
	Collision with coin is checked using Pixel perfect collision method. If collision occurs returns True, else False.
	Collision is check only if coin is near the player to save computation.
	"""
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
	"""
	To display the number of coins collected.
	"""
	win.blit(coin_board, (10,10))
	font = pygame.font.Font('freesansbold.ttf', 40)
	text_x, text_y = 80, 20
	text = font.render(str(num_coins_collected), True, (255,255,255))
	win.blit(text, (text_x, text_y))


def display_mouse_pointer_coordinates(mx,my):
	"""
	To display mouse pointer coordinates just for reference. Temporary function to be removed later.
	"""
	font = pygame.font.Font('freesansbold.ttf', 32)
	text_x, text_y = 1400, 10
	text = font.render(str(mx)+', '+str(my), True, (0,0,0))
	win.blit(text, (text_x, text_y))

def display_collision_message():
	"""
	Temporary function to communicate that collision had occured
	"""
	font = pygame.font.Font('freesansbold.ttf', 100)
	text_x, text_y = 750, 100
	text = font.render('COLLISION', True, (0,0,0))
	win.blit(text, (text_x, text_y))

# MAIN ALGORITHM

speed = 60		# fps
max_y_coord = 560	# player's y axis limit
run = True

obstacle_classes = [Tree, Other_obstacles]

collision_occured = False
rock_collision_occured = False

player = Player(250, 313)	# Creating an instance of the class Player

clock = pygame.time.Clock()

# Setting a userevent once in every 1.5 seconds to generate coin
pygame.time.set_timer(pygame.USEREVENT+1, 1500)
# Setting a userevent once in every 8 seconds to generate tree obstacles
pygame.time.set_timer(pygame.USEREVENT+2, 8000)
# Setting a userevent once in every 20 seconds to generate other obstacles
pygame.time.set_timer(pygame.USEREVENT+3, 20000)

pygame.event.set_blocked(None)
pygame.event.set_allowed([pygame.KEYDOWN, pygame.QUIT, pygame.USEREVENT+1, pygame.USEREVENT+2, pygame.USEREVENT+3])

'''
frame_count = 0	# chck fps
start_time = time.time()'''

# GAME LOOP
while run:
	# Draws stuff to be displayed in window
	draw_scene_and_obstacles()
	
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
	#pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])
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
			create_tree_obstacle()
		if event.type == pygame.USEREVENT+3:
			create_other_obstacle()
	
	update_obstacle_position()
	update_coins_position()

	# Coin collection
	collected = coin_collection()	# Checks collision and returns bool 
	if collected:
		num_coins_collected += 1
	display_num_coins_collected()

	# Collision with Obstacles
	collision_occured = collision_with_obstacle()	# Checks collision and returns bool 
	if collision_occured:		# Dummy exit
		display_collision_message()
		pygame.display.update()
		time.sleep(3)
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
