import os
import pygame

from module import foreground_module

class Coin_spark_effects():
	num_of_imgs = 9
	imgs_small = [pygame.image.load(os.path.join('Utils/Pics/Coins/Effects/',str(x)+'.png')) for x in range(num_of_imgs)]
	imgs = [pygame.transform.scale(img, (img.get_width()*2, img.get_height()*2)) for img in imgs_small]

	effects_list = []       # number of spark effects

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.runCount = 0
	
	def draw(self, win):
		self.x -= foreground_module.foreground_speed
		self.frames_per_image = 5			# each player image is drawn for 7 consecutive frames
		if self.runCount > self.frames_per_image*self.num_of_imgs :
			self.effects_list.remove(self)
		self.img = self.imgs[self.runCount//self.num_of_imgs]
		win.blit(self.img, (self.x - self.img.get_width()//3,self.y- self.img.get_height()//3))
		self.runCount += 1 
