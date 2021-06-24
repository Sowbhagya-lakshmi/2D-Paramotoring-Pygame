import os
import pygame
import random

import global_config
from module import coins_module
from module import foreground_module
from module import player_module

# LIVES
heart = pygame.image.load(os.path.join('Utils/Pics/Display/', 'life.png'))

def display_lives(win, num_of_lives):
	"""
	Displays the lives of the player.
	"""
	x_pos = 20
	for _ in range(num_of_lives):
		win.blit(heart, (x_pos,75))
		x_pos += heart.get_width() + 3

class Extra_life:
	def __init__(self):
		self.x = global_config.window_width + heart.get_width()
		free_zone_y = coins_module.find_free_zone_y()
		self.y = random.randint(0,free_zone_y)	
		self.img = pygame.image.load(os.path.join('Utils/Pics/Display/', 'extra_life.png'))
	
	def draw(self,win):
		if self.x > -1*self.img.get_width():
			win.blit(self.img, (self.x, self.y))
			self.x -= foreground_module.foreground_speed
		else:
			del self
	def check_collision(self):
		player = player_module.player
		propeller = player_module.propeller
		player_mask = pygame.mask.from_surface(player.img)
		propeller_mask = pygame.mask.from_surface(propeller.propeller_img)

		heart_mask = pygame.mask.from_surface(self.img)

		offset = self.x - player.x, self.y - player.y
		collision_point_with_player = player_mask.overlap(heart_mask, offset)	# Checking collision with player
		collision_point_with_propeller = propeller_mask.overlap(heart_mask, offset)	# Checking collision with player
		if collision_point_with_player or collision_point_with_propeller:
			return True
		return False

# MINIMAP
line = pygame.image.load(os.path.join('Utils/Pics/Display/','line.png'))
line = pygame.transform.scale(line, (line.get_width()//2, line.get_height()//5))

icon_big = pygame.image.load(os.path.join('Utils/Pics/Display/','player_location.png'))
player_icon = pygame.transform.scale(icon_big, (icon_big.get_width()//5, icon_big.get_height()//5)) 

start = pygame.image.load(os.path.join('Utils/Pics/Display/','start.png'))
start = pygame.transform.scale(start, (start.get_width()//10, start.get_height()//10))

finish = pygame.image.load(os.path.join('Utils/Pics/Display/','finish.png'))
finish = pygame.transform.scale(finish, (finish.get_width()//10, finish.get_height()//10))

line_pos_x = 1140
line_pos_y = 770

def draw_minimap(win,progress):
	"""
	Minimap shows the position of the player relative to the full distance in a miniature size.
	"""
	max_progress = global_config.game_duration*global_config.speed
	current_progress = progress/max_progress        # Value btn 0 and 1

	# Line
	win.blit(line, (line_pos_x, line_pos_y))
	# Start point
	win.blit(start, (line_pos_x-25,line_pos_y-45))
	# End point
	win.blit(finish, (line_pos_x+320,line_pos_y-45))

	# Adding the player location icon
	x_pos = line_pos_x + line.get_width()*current_progress
	centroid_x_pos = x_pos - player_icon.get_width()//2   
	y_pos = line_pos_y - player_icon.get_height()
	win.blit(player_icon, (centroid_x_pos, y_pos))

class Countdown:
	num_of_imgs = 3
	imgs_big = [pygame.image.load(os.path.join('Utils/Pics/Countdown/',str(x) + '.png')) for x in range(num_of_imgs, 0, -1)]
	imgs = [pygame.transform.scale(img, (img.get_width()//2, img.get_height()//2)) for img in imgs_big]
	imgs.append(pygame.image.load(os.path.join('Utils/Pics/Countdown/','go.png')))
	num_of_imgs = 4

	def __init__(self):
		self.x, self.y = global_config.window_width//2, global_config.window_height//2
		self.run_count = 0
		self.frames_per_image = global_config.speed

	def draw(self, win):
		if self.run_count < self.frames_per_image*self.num_of_imgs :		
			self.index = self.run_count//self.frames_per_image
			self.img = self.imgs[self.index]
			win.blit(self.img, (self.x - self.img.get_width()//2,self.y- self.img.get_height()//2))
			self.run_count += 1 
			return True
		else:
			return False

countdown = Countdown()

class Fuel:
	img = pygame.image.load(os.path.join('Utils/Pics/Display/', 'fuel2.png'))
	img_icon = pygame.transform.scale(img, (img.get_width()//2, img.get_height()//2))
	# Fuel bar
	bar_pos      = (50, 145)
	bar_size     = (120, 20)
	border_color = (0,0,0)
	red = 255
	green = 255
	bar_color = (red, green, 0)
	max_fuel = global_config.speed * 10  # 60 seconds

	def __init__(self):
		self.x = global_config.window_width
		free_zone_y = coins_module.find_free_zone_y()
		self.y = random.randint(0,free_zone_y)	

	def draw(self, win):
		if self.x > -1*self.img.get_width():
			win.blit(self.img, (self.x, self.y))
			self.x -= foreground_module.foreground_speed
		else:
			del self

	def check_collision(self):
		player = player_module.player
		propeller = player_module.propeller
		player_mask = pygame.mask.from_surface(player.img)
		propeller_mask = pygame.mask.from_surface(propeller.propeller_img)

		fuel_mask = pygame.mask.from_surface(self.img)

		offset = self.x - player.x, self.y - player.y
		collision_point_with_player = player_mask.overlap(fuel_mask, offset)	# Checking collision with player
		collision_point_with_propeller = propeller_mask.overlap(fuel_mask, offset)	# Checking collision with player
		if collision_point_with_player or collision_point_with_propeller:
			return True
		return False
	
	def calculate_fuel(self):
		pass

	def draw_fuel_bar(self, win, fuel_available):
		win.blit(self.img_icon, (10, 140))
		self.bar_color = (self.red, self.green, 0)
		progress = fuel_available/self.max_fuel
	
		pygame.draw.rect(win, self.border_color, (*self.bar_pos, *self.bar_size), 3)
		innerPos  = (self.bar_pos[0]+3, self.bar_pos[1]+3)
		innerSize = ((self.bar_size[0]-6) * progress, self.bar_size[1]-6)
		pygame.draw.rect(win, self.bar_color, (*innerPos, *innerSize))

fuel = Fuel()
