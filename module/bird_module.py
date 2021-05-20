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
			imgs.append(pygame.transform.scale(img, (int(img.get_width()//4), int(img.get_height()//4))))
		list_of_lists.append(imgs)

	birds_list = []
	collision_birds = []	# Birds for which we have to check collision

	def __init__(self,x,y,colour_num):
		self.x = x
		self.y = y
		self.runCount = 0
		self.colour_num = colour_num

	def draw(self, win):	
		self.frames_per_image = 7	# each bird image is drawn for 7 consecutive frames
		if self.runCount >= self.frames_per_image*self.num_of_imgs:
			self.runCount = 0
		self.index = self.runCount//self.frames_per_image
		self.runCount += 1

		# Bird image
		self.img = self.list_of_lists[self.colour_num][self.index]

		win.blit(self.img, (self.x,self.y))

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
			bird.x -= (foreground_module.foreground_speed + 2)

def collision_with_bird(player):
	"""
	Collision with bird is checked using Pixel perfect collision method. If collision occurs returns True, else False.
	Collision is check only if bird is near the player to save computation.
	"""
	player_mask = pygame.mask.from_surface(player.img)
	for bird in Bird.collision_birds:
		try:
			if bird.x < (player.x + player.img.get_width()+10):	# Checking for collision if near player
				bird_mask = pygame.mask.from_surface(bird.img)
				offset = bird.x - player.x, bird.y - player.y
				boolean = player_mask.overlap(bird_mask, offset)
				if boolean:
					Bird.collision_birds.remove(bird)
					return True
		except: pass
	return False