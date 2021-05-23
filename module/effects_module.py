import os
import pygame

from module import foreground_module
from module import player_module

class Coin_spark_effects():
	"""
	Describes a visual effect when the player collects a coin. Has a draw method which draws the effect onto the screen.
	"""
	num_of_imgs = 9
	imgs_small = [pygame.image.load(os.path.join('Utils/Pics/Coins/Effects/',str(x)+'.png')) for x in range(num_of_imgs)]
	imgs = [pygame.transform.scale(img, (img.get_width()*2, img.get_height()*2)) for img in imgs_small]

	coin_effects_list = []       # number of spark effects

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.runCount = 0
	
	def draw(self, win):
		self.x -= foreground_module.foreground_speed
		self.frames_per_image = 5			# each image is drawn for 5 consecutive frames
		if self.runCount > self.frames_per_image*self.num_of_imgs :
			self.coin_effects_list.remove(self)
		self.img = self.imgs[self.runCount//self.num_of_imgs]
		win.blit(self.img, (self.x - self.img.get_width()//3,self.y- self.img.get_height()//3))
		self.runCount += 1 

class Hit_effects:
	"""
	Describes a visual effect when the player hits an obstacle like tree, rock or bush. Has a draw method which draws the effect onto the screen.
	"""
	num_of_imgs = 10
	imgs = [pygame.image.load(os.path.join('Utils/Pics/Obstacles/Effects/',str(x)+'.png')) for x in range(num_of_imgs)]
	imgs = [pygame.transform.scale(img, (img.get_width()*2, img.get_height()*2)) for img in imgs]

	hit_effects_list = []   

	def __init__(self):
		self.runCount = 0
		self.x = player_module.player.x - 70	# adjusting the position
		self.y = player_module.player.y - 70
	
	def draw(self, win):
		self.x -= foreground_module.foreground_speed
		self.frames_per_image = 3			# each image is drawn for 3 consecutive frames
		if self.runCount > self.frames_per_image*self.num_of_imgs :
			self.hit_effects_list.remove(self)
		self.img = self.imgs[self.runCount//self.num_of_imgs]
		win.blit(self.img, (self.x, self.y))
		self.runCount += 1	
