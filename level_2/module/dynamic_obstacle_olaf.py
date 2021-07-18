import os
import random

import pygame

from level_2.module import background_module
from level_2.module import foreground_module
from level_2.module import player_module


class Olaf():
	"""
	Describes bird obstacles.
	"""
	# Loading bird images
	num_of_imgs = 9

	path = r'level_2/Utils/Pics/Obstacles/OlafAndReindeer/'
	
	imgs_list = []
	for x in range(num_of_imgs):
		imgs_list.append(pygame.image.load(os.path.join(path, "olaf"+ str(x) + '.png')))

	olafs_list = []
	collision_olaf = []	# Birds for which we have to check collision

	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.run_count = 0

		num_list = [1,0.7,0.75,0.65,0.85,0.95,0.8,0.9]
		random_num = random.choice(num_list)
		self.olaf_list = [pygame.transform.scale(img, (int(img.get_width()*random_num), int(img.get_height()*random_num))) for img in self.imgs_list]

		self.org_y = y									# initial y value where the bird is spawned
		self.time = 0								

	def draw(self, win):
		# Determining index of bird image to be drawn
		self.frames_per_image = 3				# each bird image is drawn for 7 consecutive frames
		if self.run_count >= self.frames_per_image*self.num_of_imgs:
			self.run_count = 0
		self.index = self.run_count//self.frames_per_image
		self.run_count += 1
		
		# Drawing bird image
		self.img = self.olaf_list[self.index]
		win.blit(self.img, (self.x,self.y))
		

def create_olaf():
	"""
	Creates a bird in the free space. 
	"""
	y_coordnate = random.uniform(50,300)
	new_olaf = Olaf(background_module.bg.get_width(), y_coordnate)
	Olaf.olafs_list.append(new_olaf)
	Olaf.collision_olaf.append(new_olaf)	#	To check collision

def draw_olaf(win):
	for olaf in Olaf.olafs_list:
		olaf.draw(win)
	update_olaf_position()
	
def update_olaf_position():
	"""
	Updates the x coordinates of bird. If bird goes offscreen, remove it from the list.
	"""
	for bird in Olaf.olafs_list:
		bird_width = bird.img.get_width()
		if bird.x < -1*bird_width: # If bird goes offscreen, removing it from bird list 
			Olaf.olafs_list.remove(bird)
		else:
			bird.x -= (foreground_module.foreground_speed + 4)

def collision_with_olaf():
	"""
	Collision with bird is checked using Pixel perfect collision method. If collision occurs returns True, else False.
	Collision is checked only if bird is near the player to save computation.
	"""
	player = player_module.player
	propeller = player_module.propeller
	player_mask = pygame.mask.from_surface(player.img)
	propeller_mask = pygame.mask.from_surface(propeller.propeller_img)

	if len(Olaf.collision_olaf)!=0:
		for bird in Olaf.collision_olaf:
			if bird.x < (player.x + player.img.get_width()) and (bird.x + bird.img.get_width()) > player.x:
				if bird.y < (player.y + player.img.get_height()) and (bird.y + bird.img.get_height()) > player.y:	# Checking for collision if near player
					bird_mask = pygame.mask.from_surface(bird.img)
					offset = int(bird.x - player.x), int(bird.y - player.y)
					collision_point_with_player = player_mask.overlap(bird_mask, offset)
					collision_point_with_propeller = propeller_mask.overlap(bird_mask, offset)	# Checking collision with player

					if collision_point_with_player or collision_point_with_propeller:
						Olaf.collision_olaf.remove(bird)
						return True
	return False