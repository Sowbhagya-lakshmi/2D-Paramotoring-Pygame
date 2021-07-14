import math
import os
import pygame
import random

from module import background_module
from module import foreground_module
from module import player_module
from module import music_module


class Shark():
	"""
	Describes shark obstacles.
	"""
	# Loading shark images
	num_of_imgs = 2
	list_of_lists = []

	path = 'Utils/Pics/Shark/'
	colour_list = os.listdir(path)
	num_of_colours = len(colour_list)	
	
	for colour in colour_list:
		imgs = []
		for x in range(num_of_imgs):
			imgs.append(pygame.image.load(os.path.join(path, colour +"/shark"+ str(x) + '.png')))
		list_of_lists.append(imgs)

	sharks_list = []
	collision_sharks = []	# sharks for which we have to check collision

	def __init__(self,x,y,colour_num):
		self.x = x
		self.y = y
		self.run_count = 0
		self.colour_num = colour_num

		random_num = random.uniform(4, 8)
		self.shark_list = [pygame.transform.scale(img, (int(img.get_width()/random_num), int(img.get_height()/random_num))) for img in self.list_of_lists[colour_num]]

		# Variables for sine wave trajectory calculation
		self.org_y = y									# initial y value where the shark is spawned
		self.time = 0									# Taken for a reference
		self.frequency = random.uniform(0.0015, 0.017)	# frequency of sine wave
		self.amplitude = random.randrange(30, 70)		# Amplitude of sine wave - defines range of shark movement in y axis

	def draw(self, win):
		# Determining index of shark image to be drawn
		self.frames_per_image = 7					# each shark image is drawn for 7 consecutive frames
		if self.run_count >= self.frames_per_image*self.num_of_imgs:
			self.run_count = 0
		self.index = self.run_count//self.frames_per_image
		self.run_count += 1
		
		# Drawing shark image
		self.img = self.shark_list[self.index]
		self.randomize_movement()
		win.blit(self.img, (self.x,self.y))
		

	def randomize_movement(self):
		# Sine wave trajectory for shark
		self.y= self.org_y + self.amplitude*math.sin(2*math.pi*self.frequency*self.time)
		self.time += 1


def create_shark():
	"""
	Creates a shark in the free space. 
	"""
	x = random.randint(50,400)	# choose random y value in upper half of window	(WIP)
	colour_num = random.randrange(Shark.num_of_colours)
	new_shark = Shark(background_module.bg.get_width(), x, colour_num)
	Shark.sharks_list.append(new_shark)
	Shark.collision_sharks.append(new_shark)	#	To check collision

def draw_shark(win):
	for shark in Shark.sharks_list:
		shark.draw(win)
		# music_module.sound_shark.play()
	update_sharks_position()
	
def update_sharks_position():
	"""
	Updates the x coordinates of shark. If shark goes offscreen, remove it from the list.
	"""
	for shark in Shark.sharks_list:
		shark_width = shark.imgs[0].get_width()
		if shark.x < -1*shark_width: # If shark goes offscreen, removing it from shark list 
			Shark.sharks_list.remove(shark)
		else:
			shark.x -= (foreground_module.foreground_speed + 4)

def collision_with_shark():
	"""
	Collision with shark is checked using Pixel perfect collision method. If collision occurs returns True, else False.
	Collision is checked only if shark is near the player to save computation.
	"""
	player = player_module.player
	propeller = player_module.propeller
	player_mask = pygame.mask.from_surface(player.img)
	propeller_mask = pygame.mask.from_surface(propeller.propeller_img)

	if len(Shark.collision_sharks)!=0:
		for shark in Shark.collision_sharks:
			if shark.x < (player.x + player.img.get_width()) and (shark.x + shark.img.get_width()) > player.x:
				if shark.y < (player.y + player.img.get_height()) and (shark.y + shark.img.get_height()) > player.y:	# Checking for collision if near player
					shark_mask = pygame.mask.from_surface(shark.img)
					offset = int(shark.x - player.x), int(shark.y - player.y)
					collision_point_with_player = player_mask.overlap(shark_mask, offset)
					collision_point_with_propeller = propeller_mask.overlap(shark_mask, offset)	# Checking collision with player

					if collision_point_with_player or collision_point_with_propeller:
						Shark.collision_sharks.remove(shark)
						return True
	return False