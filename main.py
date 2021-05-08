import json
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

	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height 
		self.runCount = 0
		
		# Border (contour coordinates)
		self.border_to_be_modified = read_json('player')
		self.border = set()
		for lst in self.border_to_be_modified:
			new_tup = (lst[0]+self.x, lst[1])
			self.border.add(new_tup)

	def draw(self, win):
		self.frames_per_image = 7			# each player image is drawn for 7 consecutive frames
		if self.runCount > self.frames_per_image*self.num_of_player_imgs :
			self.runCount = 0
		win.blit(self.imgs[self.runCount//self.num_of_player_imgs], (self.x,self.y))
		self.runCount += 1 

class Tree:
	"""
	Describes tree objects. Currently it contains 3 types of trees. It contains the x position, y position, contour coordinates of tree.
	Also contains a draw method to draw the tree onto the screen. The type of tree that is to be created can be determined using tree_num variable.
	"""
	# Loading images 
	tree_light = pygame.image.load('Utils/Pics/Obstacles/tree_light.png')
	tree_dark = pygame.image.load('Utils/Pics/Obstacles/tree_dark.png')
	cherry_tree = pygame.image.load('Utils/Pics/Obstacles/cherry_tree.png')

	imgs = [tree_light, tree_dark, cherry_tree]
	resized_imgs = [pygame.transform.scale(img, (int(img.get_width()//1.5), int(img.get_height()//1.5))) for img in imgs]

	def __init__(self, x, y, tree_num):
		self.x = x
		self.y = y
		self.tree_num = tree_num
		self.border = read_json('tree')

	# Draws the obstacle onto the screen
	def draw(self,win):
		win.blit(self.resized_imgs[self.tree_num], (self.x, self.y)) 

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
		
		# Border (contour coordinates)
		self.borders = read_json('coins')

	def draw(self, win):	
		self.frames_per_image = 3			# each coin image is drawn for 7 consecutive frames
		if self.runCount >= self.frames_per_image*self.num_of_coin_imgs:
			self.runCount = 0
		self.index = self.runCount//self.frames_per_image
		self.img = self.resized_imgs[self.index]
		self.centroid_x = self.img.get_width()//2
		win.blit(self.img, (self.x-self.centroid_x,self.y))
		self.runCount += 1
		self.border = self.borders[self.index]

# HELPER FUNCTIONS

# Returns a nested list of contour coordinates of the argument, required for collision detection
def read_json(key):
	filename = 'contour_coordinates.json'
	with open(filename) as f:
		json_data = json.load(f)
	border_points = json_data[key]
	return border_points

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
	total_num_of_obstacles = 3
	y_coordinate_obstacle = 300
	random_num = random.randrange(0,total_num_of_obstacles)       	# range over the number of obstacles
	random_x = random.randint(bg.get_width(), bg.get_width()+500)   						# random inital x position of obstacle
	if random_num == 0:
		obstacles.append(Tree(random_x,y_coordinate_obstacle,0))	# tree_light obstacle
	elif random_num == 1:
		obstacles.append(Tree(random_x,y_coordinate_obstacle,1))	# tree_dark obstacle
	elif random_num == 2:
		obstacles.append(Tree(random_x,y_coordinate_obstacle,2))	# cherry_tree obstacle

def create_coin():
	x = random.randint(-250,250)
	coins.append(Coin(bg.get_width(), 300 + x))

def update_coins_position():
	for coin in coins:
		coin_width = coin.imgs[0].get_width()
		if coin.x < -1*coin_width: # If coin goes offscreen, removing it from coins list 
			coins.remove(coin)
		else:
			coin.x -= foreground_speed


def update_obstacle_position():
	for obstacle in obstacles:
		obstacle_width = obstacle.resized_imgs[obstacle.tree_num].get_width()
		if obstacle.x < -1*obstacle_width: # If obstacle goes offscreen, removing it from obstacles list 
			obstacles.remove(obstacle)
		else:
			obstacle.x -= foreground_speed

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

def collision_with_obstacle():
	player.curr_border = set()
	for tup in player.border:
		new_tup = (tup[0], tup[1]+player.y)
		player.curr_border.add(new_tup)
	
	'''for point in player.curr_border:
		pygame.draw.circle(win, (255,0,0), point,3)
	pygame.display.update()'''

	for obstacle in obstacles:
		curr_obstacle_border = set()
		for lst in obstacle.border:
			new_tup = (lst[0]+obstacle.x, lst[1]+obstacle.y)
			curr_obstacle_border.add(new_tup)

		'''for point in curr_obstacle_border:
			pygame.draw.circle(win, (255,0,0), point,3)
		pygame.display.update()'''
		

		collision_points = player.curr_border.intersection(curr_obstacle_border)
		if len(collision_points) > 0:
			return True
	return False

def coin_collection():
	for coin in coins:
		coin.curr_border = set()
		try:
			for lst in coin.border:
				new_tup = (lst[0]+coin.x-coin.centroid_x, lst[1]+coin.y)
				coin.curr_border.add(new_tup)
			
			collision_points = player.curr_border.intersection(coin.curr_border)
			if len(collision_points) > 0:
				coins.remove(coin)
				return True
		except: break
	return False

def display_num_coins_collected():
	win.blit(coin_board, (10,10))
	font = pygame.font.Font('freesansbold.ttf', 30)
	text_x, text_y = 60, 20
	text = font.render(str(num_coins_collected), True, (255,255,255))
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

# Ground
ground = pygame.image.load(os.path.join('Utils/Pics/Foreground','ground.png'))
flipped_ground = pygame.transform.flip(ground, True, False)
ground_x = 0
ground_width = ground.get_width() - 5	# To prevent glitches in background movement...yet to find an optimal solution

# Coin collection board
coin_board = pygame.image.load(os.path.join('Utils/Pics/Display','coin_display.png'))

speed = 60		# fps
clock = pygame.time.Clock()
foreground_speed = 6 	# Foreground shifts by 6 pixels in each game loop
background_speed = 2	# Background shifts by 2 pixels in each game loop
run = True
collision_occured = False
obstacles = []
coins = []
num_coins_collected = 0

player = Player(250, 313, 50, 50)	# Creating an instance of the class Player

# Setting a userevent once in every 8 seconds to generate obstacles
pygame.time.set_timer(pygame.USEREVENT+2, 8000)

# Setting a userevent once in every 3 seconds to generate coin
pygame.time.set_timer(pygame.USEREVENT+1, 2000)


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
		player.x, player.y = 250, 560
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

		if event.type == pygame.USEREVENT+2:
			create_random_obstacle()
		
		if event.type == pygame.USEREVENT+1:
			create_coin()
	
	update_obstacle_position()
	update_coins_position()

	collision_occured = collision_with_obstacle()	# Checks collision and returns bool 

	if collision_occured:		# Dummy exit
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
