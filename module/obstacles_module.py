import os
import pygame
import random

import main
from module import background_module
from module import effects_module
from module import foreground_module
from module import player_module

class Tree:
	"""
	Describes tree objects. Currently it contains 11 types of trees. It contains the x position, y position of tree.
	Also contains a draw method to draw trees onto the screen. The type of tree that is to be created can be determined using num variable.
	"""
	# Loading images 
	num_of_imgs = 11
	imgs = [pygame.image.load(os.path.join('Utils/Pics/Obstacles/', "tree"+ str(x) + '.png')) for x in range(num_of_imgs)]

	obstacles = []
	collision_obstacles = []

	def __init__(self, x, num):
		self.num = num

		# Randomizing the size of imgs
		self.random_size = random.uniform(1.15, 1.25)	
		self.org_img = self.imgs[self.num]
		self.img = pygame.transform.scale(self.org_img, ((int(self.org_img.get_width()//self.random_size), int(self.org_img.get_height()//self.random_size))))
		
		self.x = x
		self.y = foreground_module.ground_y - self.img.get_height() + 230 # push the image slightly down
	
		# Width and height of obstacle
		self.width = self.img.get_width()
		self.height = self.img.get_height()

	# Draws the obstacle onto the screen
	def draw(self,win):
		win.blit(self.img, (self.x, self.y)) 

class Rock_n_Bush:
	"""
	Describes other obstacle objects. Contains rocks. It contains the x position, y position. The various obstacles are
	created using num variable. Also contains a draw method to draw the tree onto the screen.
	"""
	# Loading images 
	num_of_imgs = 4
	imgs = [pygame.image.load(os.path.join('Utils/Pics/Obstacles/', "obstacle"+ str(x) + '.png')) for x in range(num_of_imgs)]
	resized_imgs = [pygame.transform.scale(img, (int(img.get_width()*1.3), int(img.get_height()*1.3))) for img in imgs]

	obstacles = []
	collision_obstacles = []

	def __init__(self, x, num):
		self.num = num
		self.img = self.resized_imgs[self.num]
		self.x = x
		self.y = foreground_module.ground_y - self.img.get_height() + 250 # push the image slightly down

		# Width and height of obstacle
		self.width = self.img.get_width()
		self.height = self.img.get_height()

	# Draws the obstacle onto the screen
	def draw(self,win):
		win.blit(self.img, (self.x, self.y))

obstacle_classes = [Rock_n_Bush, Tree]

def create_tree_obstacle():
	"""
	Creates a random tree obstacle.
	"""
	random_num = random.randrange(0,Tree.num_of_imgs)       	# range over the number of obstacles
	random_x = random.randint(background_module.bg.get_width(), background_module.bg.get_width()+1500)   # random inital x position of obstacle	
	# Add new obstacle to obstacles list
	new_tree = Tree(random_x,random_num)
	Tree.obstacles.append(new_tree)
	Tree.collision_obstacles.append(new_tree)	# To check collision

def create_rock_n_bush():
	"""
	Creates a random obstacle either a rock or bush.
	"""
	random_num = random.randrange(0,Rock_n_Bush.num_of_imgs)       	# range over the number of obstacles
	random_x = random.randint(background_module.bg.get_width(), background_module.bg.get_width()+1500)   # random inital x position of obstacle
	# Add new obstacle to obstacles list
	new_obstacle = Rock_n_Bush(random_x,random_num)
	Rock_n_Bush.obstacles.append(new_obstacle)
	Rock_n_Bush.collision_obstacles.append(new_obstacle)

def draw_obstacles(win):
	"""
	Draws the obstacles onto the screen and updates the obstacles position.
	"""
	for element in obstacle_classes:
		for obstacle in element.obstacles:
			if obstacle.x <= main.width:	# draw only if the obsatcle is on-screen
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
				obstacle.x -= foreground_module.foreground_speed

def collision_with_obstacle():
	"""
	Pixel perfect collision implemented using masks. Checks for collision of mask of player against other
	obstacles only if the obstacle is near to the player. Returns True if collision occurred, else False.
	"""
	player = player_module.player
	propeller = player_module.propeller
	player_mask = pygame.mask.from_surface(player.img)
	propeller_mask = pygame.mask.from_surface(propeller.propeller_img)
	
	for element in obstacle_classes:
		for obstacle in element.collision_obstacles:
			if obstacle.x < (player.x + player.img.get_width()+10):	# Checking for collision if near player
				obstacle_mask = pygame.mask.from_surface(obstacle.img)
				offset = obstacle.x - player.x, obstacle.y - player.y

				collision_point_with_player = player_mask.overlap(obstacle_mask, offset)	# Checking collision with player
				collision_point_with_propeller = propeller_mask.overlap(obstacle_mask, offset)	# Checking collision with propeller

				if collision_point_with_player or collision_point_with_propeller:
					element.collision_obstacles.remove(obstacle)
					effects_module.Hit_effects.hit_effects_list.append(effects_module.Hit_effects())
					return True
	return False