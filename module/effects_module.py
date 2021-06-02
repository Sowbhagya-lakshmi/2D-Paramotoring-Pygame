import os
import pygame

from module import foreground_module
from module import player_module

class Coin_spark_effects():
	"""
	Describes a visual effect when the player collects a coin. Has a draw method which draws the effect onto the screen.
	"""
	path = 'Utils/Pics/Coins/Effects/'
	img_name_lst = os.listdir(path)
	num_of_imgs = len(img_name_lst)

	imgs_big = [pygame.image.load('Utils/Pics/Coins/Effects/'+img) for img in img_name_lst]
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
	Describes a visual effect when the player hits an obstacle like tree, rock or bush. Has a draw method which draws the effect onto the screen.
	"""
	path = 'Utils/Pics/Obstacles/Effects/'
	img_name_lst = os.listdir(path)
	num_of_imgs = len(img_name_lst)

	imgs = [pygame.image.load('Utils/Pics/Obstacles/Effects/'+img) for img in img_name_lst]
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
