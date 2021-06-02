import math
import os
import pygame
import random

from module import background_module
from module import foreground_module
from module import coins_module

class Bird():
	"""
	Describes bird obstacles.
	"""
	# Loading bird images
	num_of_imgs = 6
	list_of_lists = []

	path = 'Utils/Pics/Bird/'
	colour_list = os.listdir(path)
	num_of_colours = len(colour_list)	
	
	for colour in colour_list:
		imgs = []
		for x in range(num_of_imgs):
			img = pygame.image.load(os.path.join(path, colour +"/bird"+ str(x) + '.png'))
			imgs.append(pygame.transform.scale(img, (int(img.get_width()//6), int(img.get_height()//6))))
		list_of_lists.append(imgs)

	birds_list = []
	collision_birds = []	# Birds for which we have to check collision

	def __init__(self,x,y,colour_num):
		self.x = x
		self.y = y
		self.runCount = 0
		self.colour_num = colour_num

		# Variables for trajectory calculation
		self.org_y = y		# initial y value
		self.time = 0
		self.frequency = random.uniform(0.005, 0.013)
		self.amplitude = random.randrange(30, 70)
		print(self.amplitude)

	def draw(self, win):
		# Determining index of bird image to be drawn
		self.frames_per_image = 7					# each bird image is drawn for 7 consecutive frames
		if self.runCount >= self.frames_per_image*self.num_of_imgs:
			self.runCount = 0
		self.index = self.runCount//self.frames_per_image
		self.runCount += 1
		
		# Drawing bird image
		self.img = self.list_of_lists[self.colour_num][self.index]
		self.randomize_movement()
		win.blit(self.img, (self.x,self.y))
		

	def randomize_movement(self):
		# Sine wave trajectory for bird
		self.y= self.org_y + self.amplitude*math.sin(2*math.pi*self.frequency*self.time)
		self.time += 1


def create_bird():
	"""
	Creates a bird in the free space. 
	"""
	free_zone_y = coins_module.free_zone_y	# find free space in y axis
	x = random.randint(50,free_zone_y)	# choose random y value within free zone
	colour_num = random.randrange(Bird.num_of_colours)
	new_bird = Bird(background_module.bg.get_width(), x, colour_num)
	Bird.birds_list.append(new_bird)
	Bird.collision_birds.append(new_bird)	#	To check collision

def draw_bird(win):
	for bird in Bird.birds_list:
		bird.draw(win)
	update_birds_position()
	
def update_birds_position():
	"""
	Updates the x coordinates of bird. If bird goes offscreen, remove it from the list.
	"""
	for bird in Bird.birds_list:
		bird_width = bird.imgs[0].get_width()
		if bird.x < -1*bird_width: # If bird goes offscreen, removing it from bird list 
			Bird.birds_list.remove(bird)
		else:
			bird.x -= (foreground_module.foreground_speed + 4)

def collision_with_bird(player):
	"""
	Collision with bird is checked using Pixel perfect collision method. If collision occurs returns True, else False.
	Collision is check only if bird is near the player to save computation.
	"""
	player_mask = pygame.mask.from_surface(player.img)
	propeller_mask = pygame.mask.from_surface(player.propeller_img)
	if len(Bird.collision_birds)!=0:
		for bird in Bird.collision_birds:
			if bird.x < (player.x + player.img.get_width()+10):	# Checking for collision if near player
				bird_mask = pygame.mask.from_surface(bird.img)
				offset = int(bird.x - player.x), int(bird.y - player.y)
				collision_point_with_player = player_mask.overlap(bird_mask, offset)
				collision_point_with_propeller = propeller_mask.overlap(bird_mask, offset)	# Checking collision with player

				if collision_point_with_player or collision_point_with_propeller:
					Bird.collision_birds.remove(bird)
					return True
	return False