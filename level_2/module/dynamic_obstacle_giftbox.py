import os
import pygame
import random

from level_2.module import background_module
from level_2.module import foreground_module
from level_2.module import player_module
from level_2.module import music_module


class Gift():
	"""
	Describes dynamic obstacle santa.
	"""
	# Loading bird images
	num_of_imgs = 24

	path = r'level_2/Utils/Pics/Santa/gift/'
	
	imgs_list = []
	for x in range(num_of_imgs):
		imgs_list.append(pygame.image.load(os.path.join(path, "gift" + str(x) + '.png')))

	gifts_list = []
	collision_gift = []	# Birds for which we have to check collision

	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.run_count = 0
		#self.colour_num = colour_num

		self.gift_list = [pygame.transform.scale(img, (int(img.get_width()*1), int(img.get_height()*1))) for img in self.imgs_list]

		self.org_y = y									# initial y value where the bird is spawned
		self.time = 0								

	def draw(self, win):
		# Determining index of bird image to be drawn
		self.frames_per_image = 7					# each bird image is drawn for 7 consecutive frames
		if self.run_count >= self.frames_per_image*self.num_of_imgs:
			self.run_count = 0
		self.index = self.run_count//self.frames_per_image
		self.run_count += 1
		
		# Drawing bird image
		self.img = self.gift_list[self.index]
		win.blit(self.img, (self.x,self.y))
		

def create_gift():
	"""
	Creates a bird in the free space. 
	"""
	#y_coordnate = random.uniform(100,380)
	new_gift = Gift(background_module.bg.get_width(), 250)
	Gift.gifts_list.append(new_gift)
	Gift.collision_gift.append(new_gift)	#	To check collision

def draw_gift(win):
	for olaf in Gift.gifts_list:
		olaf.draw(win)
		# music_module.sound_bird.play()
	update_gift_position()
	
def update_gift_position():
	"""
	Updates the x coordinates of bird. If bird goes offscreen, remove it from the list.
	"""
	for bird in Gift.gifts_list:
		bird_width = bird.img.get_width()
		if bird.x < -1*bird_width: # If bird goes offscreen, removing it from bird list 
			Gift.gifts_list.remove(bird)
		else:
			bird.x -= (foreground_module.foreground_speed + 4)

def collision_with_gift():
	"""
	Collision with bird is checked using Pixel perfect collision method. If collision occurs returns True, else False.
	Collision is checked only if bird is near the player to save computation.
	"""
	player = player_module.player
	propeller = player_module.propeller
	player_mask = pygame.mask.from_surface(player.img)
	propeller_mask = pygame.mask.from_surface(propeller.propeller_img)

	if len(Gift.collision_gift)!=0:
		for bird in Gift.collision_gift:
			if bird.x < (player.x + player.img.get_width()) and (bird.x + bird.img.get_width()) > player.x:
				if bird.y < (player.y + player.img.get_height()) and (bird.y + bird.img.get_height()) > player.y:	# Checking for collision if near player
					bird_mask = pygame.mask.from_surface(bird.img)
					offset = int(bird.x - player.x), int(bird.y - player.y)
					collision_point_with_player = player_mask.overlap(bird_mask, offset)
					collision_point_with_propeller = propeller_mask.overlap(bird_mask, offset)	# Checking collision with player

					if collision_point_with_player or collision_point_with_propeller:
						Gift.collision_gift.remove(bird)
						return True
	return False