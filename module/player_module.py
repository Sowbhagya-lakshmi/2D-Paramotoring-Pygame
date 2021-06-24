import os
import pygame

from module import foreground_module

class Player:
	"""
	Descibes the player object.
	It has info such as the x positon, y position, width, height and a draw method to draw the
    player's images onto the screen hence creating the animation effect.
	"""

	path = 'Utils/Pics/Player/'
	img_name_lst = os.listdir(path)
	num_of_player_imgs = len(img_name_lst)

	# Loading player images
	imgs_big = [pygame.image.load('Utils/Pics/Player/'+img) for img in img_name_lst]
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

	path = 'Utils/Pics/Propeller/'
	img_name_lst = os.listdir(path)
	num_of_propeller_imgs = len(img_name_lst)

	# Loading propeller images
	org_propeller_imgs = [pygame.image.load('Utils/Pics/Propeller/'+img) for img in img_name_lst]
	propeller_imgs = [pygame.transform.scale(img, (int(img.get_width()/4), int(img.get_height()/4))) for img in org_propeller_imgs ]

	def __init__(self):
		self.run_count = 0
		self.propeller_count = 0
	
	def draw(self, win):
		# Draw propeller
		self.frames_per_propeller_img = 2
		if self.propeller_count >= self.frames_per_propeller_img*self.num_of_propeller_imgs :
			self.propeller_count = 0
		
		self.index = self.propeller_count//self.frames_per_propeller_img
		self.propeller_img = self.propeller_imgs[self.index]
		win.blit(self.propeller_img, (player.x,player.y))
		self.propeller_count += 1 


player = Player()	
propeller = Propeller()	

def draw_player(win):
	(mx, my) = pygame.mouse.get_pos()
		
	# limit player's movable region
	if my < foreground_module.ground_y :
		player.x, player.y = 250, my
	else:
		player.x, player.y = 250, foreground_module.ground_y

	propeller.draw(win)
	player.draw(win)