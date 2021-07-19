import math
import os
import pygame
import random

from level_3.module import background_module
from level_3.module import foreground_module
from level_3.module import player_module

class Dragon():
	"""
	Describes dragon obstacles.
	"""
	# Loading dragon images
	num_of_imgs = 7
	list_of_lists = []

	path = r'level_3/Utils/Pics/Dragon/'
	colour_list = os.listdir(path)
	num_of_colours = len(colour_list)	
	
	for colour in colour_list:
		imgs = []
		for x in range(num_of_imgs):
			imgs.append(pygame.image.load(os.path.join(path, colour +"/dragon"+ str(x) + '.png')))
		list_of_lists.append(imgs)

	dragons_list = []
	collision_dragons = []	# dragons for which we have to check collision

	def __init__(self,x,y,colour_num):
		self.x = x
		self.y = y
		self.run_count = 0
		self.colour_num = colour_num

		random_num = random.uniform(4, 8)
		self.dragon_list = [pygame.transform.scale(img, (int(img.get_width()/random_num), int(img.get_height()/random_num))) for img in self.list_of_lists[colour_num]]

		# Variables for sine wave trajectory calculation
		self.org_y = y									# initial y value where the dragon is spawned
		self.time = 0									# Taken for a reference
		self.frequency = random.uniform(0.005, 0.012)	# frequency of sine wave
		self.amplitude = random.randrange(30, 70)		# Amplitude of sine wave - defines range of dragon movement in y axis

	def draw(self, win):
		# Determining index of dragon image to be drawn
		self.frames_per_image = 7					# each dragon image is drawn for 7 consecutive frames
		if self.run_count >= self.frames_per_image*self.num_of_imgs:
			self.run_count = 0
		self.index = self.run_count//self.frames_per_image
		self.run_count += 1
		
		# Drawing dragon image
		self.img = self.dragon_list[self.index]
		self.randomize_movement()
		win.blit(self.img, (self.x,self.y))
		

	def randomize_movement(self):
		# Sine wave trajectory for dragon
		self.y= self.org_y + self.amplitude*math.sin(2*math.pi*self.frequency*self.time)
		self.time += 1


def create_dragon():
	"""
	Creates a dragon in the free space. 
	"""
	x = random.randint(50,400)	# choose random y value in upper half of window	(WIP)
	colour_num = random.randrange(Dragon.num_of_colours)
	new_dragon = Dragon(background_module.bg.get_width(), x, colour_num)
	Dragon.dragons_list.append(new_dragon)
	Dragon.collision_dragons.append(new_dragon)	#	To check collision

def draw_dragon(win):
	for dragon in Dragon.dragons_list:
		dragon.draw(win)
	update_dragons_position()
	
def update_dragons_position():
	"""
	Updates the x coordinates of dragon. If dragon goes offscreen, remove it from the list.
	"""
	for dragon in Dragon.dragons_list:
		dragon_width = dragon.imgs[0].get_width()
		if dragon.x < -1*dragon_width: # If dragon goes offscreen, removing it from dragon list 
			Dragon.dragons_list.remove(dragon)
		else:
			dragon.x -= (foreground_module.foreground_speed + 4)

def collision_with_dragon():
	"""
	Collision with dragon is checked using Pixel perfect collision method. If collision occurs returns True, else False.
	Collision is checked only if dragon is near the player to save computation.
	"""
	player = player_module.player
	propeller = player_module.propeller

	if len(Dragon.collision_dragons)!=0:
		for dragon in Dragon.collision_dragons:
			if dragon.x < (player.x + player.img.get_width()) and (dragon.x + dragon.img.get_width()) > player.x:
				if dragon.y < (player.y + player.img.get_height()) and (dragon.y + dragon.img.get_height()) > player.y:	# Checking for collision if near player
					player_mask = pygame.mask.from_surface(player.img)
					propeller_mask = pygame.mask.from_surface(propeller.propeller_img)
					dragon_mask = pygame.mask.from_surface(dragon.img)
					
					offset = int(dragon.x - player.x), int(dragon.y - player.y)
					collision_point_with_player = player_mask.overlap(dragon_mask, offset)
					collision_point_with_propeller = propeller_mask.overlap(dragon_mask, offset)	# Checking collision with player

					if collision_point_with_player or collision_point_with_propeller:
						Dragon.collision_dragons.remove(dragon)
						return True
	return False