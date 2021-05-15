import os
import pygame
import random

import bg_module
import fg_module

class Tree:
	"""
	Describes tree objects. Currently it contains 11 types of trees. It contains the x position, y position of tree.
	Also contains a draw method to draw trees onto the screen. The type of tree that is to be created can be determined using num variable.
	"""
	# Loading images 
	num_of_imgs = 11
	imgs = [pygame.image.load(os.path.join('Utils/Pics/Obstacles/', "tree"+ str(x) + '.png')).convert_alpha() for x in range(num_of_imgs)]
	resized_imgs = [pygame.transform.scale(img, (int(img.get_width()//1.2), int(img.get_height()//1.2))) for img in imgs]

	obstacles = []


	def __init__(self, x, num):
		self.num = num
		self.img = self.resized_imgs[self.num]
		self.x = x
		self.y = fg_module.ground_y - self.img.get_height() + 230 # push the image slightly down
	
		# Width and height of obstacle
		self.width = self.img.get_width()
		self.height = self.img.get_height()

	# Draws the obstacle onto the screen
	def draw(self,win):
		win.blit(self.img, (self.x, self.y)) 

class Other_obstacles:
	"""
	Describes other obstacle objects. Contains rocks. It contains the x position, y position. The various obstacles are
	created using num variable. Also contains a draw method to draw the tree onto the screen.
	"""
	# Loading images 
	num_of_imgs = 4
	imgs = [pygame.image.load(os.path.join('Utils/Pics/Obstacles/', "obstacle"+ str(x) + '.png')).convert_alpha() for x in range(num_of_imgs)]
	resized_imgs = [pygame.transform.scale(img, (int(img.get_width()), int(img.get_height()))) for img in imgs]

	obstacles = []

	def __init__(self, x, num):
		self.num = num
		self.img = self.resized_imgs[self.num]
		self.x = x
		self.y = fg_module.ground_y - self.img.get_height() + 250 # push the image slightly down

		# Width and height of obstacle
		self.width = self.img.get_width()
		self.height = self.img.get_height()

	# Draws the obstacle onto the screen
	def draw(self,win):
		win.blit(self.img, (self.x, self.y))

obstacle_classes = [Tree, Other_obstacles]



def create_tree_obstacle():
	"""
	Creates a random tree obstacle.
	"""
	random_num = random.randrange(0,Tree.num_of_imgs)       	# range over the number of obstacles
	random_x = random.randint(bg_module.bg.get_width(), bg_module.bg.get_width()+500)   # random inital x position of obstacle	
	# Add new obstacle to obstacles list
	Tree.obstacles.append(Tree(random_x,random_num))

def create_other_obstacle():
	"""
	Creates a random obstacle.
	"""
	random_num = random.randrange(0,Other_obstacles.num_of_imgs)       	# range over the number of obstacles
	random_x = random.randint(bg_module.bg.get_width(), bg_module.bg.get_width()+500)   # random inital x position of obstacle
	# Add new obstacle to obstacles list
	Other_obstacles.obstacles.append(Other_obstacles(random_x,random_num))

def draw_obstacles(win):
	"""
	Draws the obstacles onto the screen and updates the obstacles position.
	"""
	for obstacle in Other_obstacles.obstacles:
		obstacle.draw(win)
	for obstacle in Tree.obstacles:
		obstacle.draw(win)
	update_obstacle_position()

def update_obstacle_position():
	"""
	Creates the moving effect. If obstacle goes offscreen, removes it from obstacles list"
	"""
	for element in obstacle_classes:
		for obstacle in element.obstacles:
			if obstacle.x < -1*obstacle.width:
				element.obstacles.remove(obstacle)
			else:
				obstacle.x -= fg_module.foreground_speed

def collision_with_obstacle(player):
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
