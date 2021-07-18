import os

import pygame

from level_1.module import foreground_module
from level_1.module import player_module

class Coin_spark_effects():
	"""
	Describes a visual effect when the player collects a coin. Draw method which draws the effect onto the screen.
	"""
	path = r'level_1/Utils/Pics/Coins/Effects/'
	list_of_imgs = os.listdir(path)	# ist of all images in the path
	num_of_imgs = len(list_of_imgs)

	imgs_big = [pygame.image.load(r'level_1/Utils/Pics/Coins/Effects/'+img) for img in list_of_imgs]
	imgs = [pygame.transform.scale(img, (int(img.get_width()/6), int(img.get_height()/6))) for img in imgs_big]

	coin_effects_list = []       # contains spark objects

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.run_count = 0
	
	def draw(self, win):
		self.x -= foreground_module.foreground_speed
		self.frames_per_image = 2			# Each image is drawn for 2 consecutive frames

		if self.run_count >= self.frames_per_image*self.num_of_imgs :
			self.coin_effects_list.remove(self)
			self.run_count = 0
			return None
		
		self.index = self.run_count//self.frames_per_image
		self.img = self.imgs[self.index]
		win.blit(self.img, (self.x - self.img.get_width()//3,self.y- self.img.get_height()//3))
		self.run_count += 1 

class Hit_effects:
	"""
	Describes a visual effect when the player hits an obstacle like a tree, rock, or bush. Draw method which draws the effect onto the screen.
	"""
	path = r'level_1/Utils/Pics/Obstacles/Effects/'
	list_of_imgs = os.listdir(path)
	num_of_imgs = len(list_of_imgs)

	imgs = [pygame.image.load(r'level_1/Utils/Pics/Obstacles/Effects/'+img) for img in list_of_imgs]
	imgs = [pygame.transform.scale(img, (img.get_width()*2, img.get_height()*2)) for img in imgs]

	hit_effects_list = []   

	def __init__(self):
		self.run_count = 0
		self.x = player_module.player.x + player_module.player.img.get_width() - self.imgs[0].get_width()//2	# adjusting the position
		self.y = player_module.player.y + player_module.player.img.get_height()//2	- self.imgs[0].get_height()//2
	
	def draw(self, win):
		self.x -= foreground_module.foreground_speed

		self.frames_per_image = 2			# each image is drawn for 3 consecutive frames
		if self.run_count > self.frames_per_image*self.num_of_imgs :
			self.hit_effects_list.remove(self)

		self.index = self.run_count//self.num_of_imgs
		self.img = self.imgs[self.index]
		win.blit(self.img, (self.x, self.y))
		self.run_count += 1	
