import os
import random

import pygame

from level_3.module import background_module
from level_3.module import foreground_module
from level_3.module import player_module

class Ghost():
	"""
	Describes ghost obstacles.
	"""
	# Loading ghost images
	num_of_imgs = 6
	list_of_lists = []

	path = r'level_3/Utils/Pics/Ghost/'
	colour_list = os.listdir(path)
	num_of_colours = len(colour_list)	
	
	for colour in colour_list:
		imgs = []
		for x in range(num_of_imgs):
			imgs.append(pygame.image.load(os.path.join(path, colour+"/"+ str(x) + '.png')))
		list_of_lists.append(imgs)

	ghosts_list = []
	collision_ghosts = []	# ghosts for which we have to check collision

	def __init__(self,x,y,colour_num):
		self.x = x
		self.y = y
		self.run_count = 0
		self.colour_num = colour_num

		random_num = random.uniform(6, 10)
		self.ghosts_list = [pygame.transform.scale(img, (int(img.get_width()/random_num), int(img.get_height()/random_num))) for img in self.list_of_lists[colour_num]]

		# Variables for sine wave trajectory calculation
		self.org_y = y									# initial y value where the ghost is spawned
		self.time = 0									# Taken for a reference
		self.frequency = random.uniform(0.005, 0.013)	# frequency of sine wave
		self.amplitude = random.randrange(30, 70)		# Amplitude of sine wave - defines range of ghost movement in y axis

	def draw(self, win):
		# Determining index of ghost image to be drawn
		self.frames_per_image = 7					# each ghost image is drawn for 7 consecutive frames
		if self.run_count >= self.frames_per_image*self.num_of_imgs:
			self.run_count = 0
		self.index = self.run_count//self.frames_per_image
		self.run_count += 1
		
		# Drawing ghost image
		self.img = self.ghosts_list[self.index]
		self.randomize_movement()
		win.blit(self.img, (self.x,self.y))
		

	def randomize_movement(self):
		# Sine wave trajectory for ghost
		self.y= self.org_y 
		self.time += 1

def create_ghost():
	"""
	Creates a dragon in the free space. 
	"""
	x = random.randint(50,400)	# choose random y value in upper half of window	(WIP)
	colour_num = random.randrange(Ghost.num_of_colours)
	new_ghost = Ghost(background_module.bg.get_width(), x, colour_num)
	Ghost.ghosts_list.append(new_ghost)
	Ghost.collision_ghosts.append(new_ghost)	#	To check collision

def draw_ghost(win):
	for ghost in Ghost.ghosts_list:
		ghost.draw(win)
	update_ghosts_position()
	
def update_ghosts_position():
	"""
	Updates the x coordinates of ghost. If ghost goes offscreen, remove it from the list.
	"""
	for ghost in Ghost.ghosts_list:
		ghost_width = ghost.imgs[0].get_width()
		if ghost.x < -1*ghost_width: # If ghost goes offscreen, removing it from ghost list 
			try:
				ghost.ghosts_list.remove(ghost)
			except: pass
		else:
			ghost.x -= (foreground_module.foreground_speed + 4)

def collision_with_ghost():
	"""
	Collision with ghost is checked using Pixel perfect collision method. If collision occurs returns True, else False.
	Collision is checked only if ghost is near the player to save computation.
	"""
	player = player_module.player
	propeller = player_module.propeller

	if len(Ghost.collision_ghosts)!=0:
		for ghost in Ghost.collision_ghosts:
			if ghost.x < (player.x + player.img.get_width()) and (ghost.x + ghost.img.get_width()) > player.x:
				if ghost.y < (player.y + player.img.get_height()) and (ghost.y + ghost.img.get_height()) > player.y:	# Checking for collision if near player
					player_mask = pygame.mask.from_surface(player.img)
					propeller_mask = pygame.mask.from_surface(propeller.propeller_img)
					ghost_mask = pygame.mask.from_surface(ghost.img)
					offset = int(ghost.x - player.x), int(ghost.y - player.y)
					collision_point_with_player = player_mask.overlap(ghost_mask, offset)
					collision_point_with_propeller = propeller_mask.overlap(ghost_mask, offset)	# Checking collision with player

					if collision_point_with_player or collision_point_with_propeller:
						Ghost.collision_ghosts.remove(ghost)
						return True
	return False