import os

import pygame

import global_config
from level_2.module import foreground_module

class Player:
	"""
	Descibes the player object.
	It has info such as the x positon, y position, width, height and a draw method to draw the
    player's images onto the screen hence creating the animation effect.
	"""

	path = r'level_2/Utils/Pics/Player/'
	img_name_lst = os.listdir(path)
	num_of_player_imgs = len(img_name_lst)

	# Loading player images
	imgs_big = [pygame.image.load(r'level_2/Utils/Pics/Player/'+img) for img in img_name_lst]
	imgs = [pygame.transform.scale(img, (int(img.get_width()/4), int(img.get_height()/4))) for img in imgs_big ] 

	def __init__(self):
		self.x = 0
		self.y = 0
		self.run_count = 0

	def draw(self, win):

		# Draw player
		self.frames_per_image = 7			# each player image is drawn for 7 consecutive frames
		if self.run_count >= self.frames_per_image*self.num_of_player_imgs :
			self.run_count = 0

		self.index = self.run_count//self.frames_per_image
		self.img = self.imgs[self.index]
		win.blit(self.img, (self.x,self.y))
		self.run_count += 1 

class Propeller:
	"""
	Descibes the propeller. Has a draw method which blits the propeller image to the screen.
	"""

	path = r'level_2/Utils/Pics/Propeller/'
	img_name_lst = os.listdir(path)
	num_of_propeller_imgs = len(img_name_lst)

	# Loading propeller images
	org_propeller_imgs = [pygame.image.load(r'level_2/Utils/Pics/Propeller/'+img) for img in img_name_lst]
	propeller_imgs = [pygame.transform.scale(img, (int(img.get_width()/4), int(img.get_height()/4))) for img in org_propeller_imgs ]
	frames_per_propeller_img = 2

	def __init__(self):
		self.run_count = 0
		self.propeller_count = 0
	
	def draw(self, win):
		# Draw propeller
		frames_per_propeller_img = int(self.frames_per_propeller_img)
		if self.propeller_count >= frames_per_propeller_img*self.num_of_propeller_imgs :
			self.propeller_count = 0
		
		self.index = self.propeller_count//frames_per_propeller_img
		self.propeller_img = self.propeller_imgs[self.index]
		win.blit(self.propeller_img, (player.x,player.y))
		self.propeller_count += 1 


player = Player()	
propeller = Propeller()	

def draw_player(win, player_won=False):
	(mx, my) = pygame.mouse.get_pos()
		
	# limit player's movable region
	if player_won:
		if player.x < global_config.window_width - player.img.get_width():
			player.x = player.x + 3
		player.y = my
	elif my < foreground_module.ground_y - 50:
		player.x, player.y = 250, my
	else:
		player.x, player.y = 250, foreground_module.ground_y - 50

	propeller.draw(win)
	player.draw(win)

	x_pos, y_pos = player.x, player.y 

	return x_pos, y_pos