import multiprocessing
import os
from sys import base_prefix
import pygame
import random

import global_config
from module import coins_module
from module import event_module
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

	fuel_list = []

	def __init__(self):
		self.x = global_config.window_width
		free_zone_y = coins_module.find_free_zone_y()
		self.y = random.randint(0,free_zone_y)	
		self.img = pygame.image.load(os.path.join('Utils/Pics/Display/','fuel2.png'))

	def draw(self, win):
		# print('drawing')
		for fuel in self.fuel_list:
			if fuel.x > -1*fuel.img.get_width():
				# print('blitting')
				win.blit(fuel.img, (fuel.x, fuel.y))
				# print(fuel.x, fuel.y)
				fuel.x -= foreground_module.foreground_speed
			else:
				self.fuel_list.remove(fuel)

		self.fuel_collection()

	def check_collision(self):
		for fuel in self.fuel_list:
			player = player_module.player
			propeller = player_module.propeller
			player_mask = pygame.mask.from_surface(player.img)
			propeller_mask = pygame.mask.from_surface(propeller.propeller_img)

			fuel_mask = pygame.mask.from_surface(fuel.img)

			offset = fuel.x - player.x, fuel.y - player.y
			collision_point_with_player = player_mask.overlap(fuel_mask, offset)	# Checking collision with player
			collision_point_with_propeller = propeller_mask.overlap(fuel_mask, offset)	# Checking collision with player
			if collision_point_with_player or collision_point_with_propeller:
				return True
		return False

	def fuel_collection(self):
		global fuel_bar
		bool = self.check_collision()
		if bool:
			for fuel in self.fuel_list:
				self.fuel_list.remove(fuel)
				del fuel_bar
				fuel_bar = Fuel_bar()
				# fuel_bar.fuel_available = fuel_bar.max_fuel


def draw_fuel(win):
		for fuel in Fuel.fuel_list:
			fuel.draw(win)	

class Fuel_bar:
	img = pygame.image.load(os.path.join('Utils/Pics/Display/', 'fuel2.png'))
	img_icon = pygame.transform.scale(img, (img.get_width()//2, img.get_height()//2))

	bar_pos      = (50, 145)
	bar_size     = (120, 20)
	border_color = (0,0,0)
	red = 255
	green = 255
	bar_color = (red, green, 0)
	max_fuel = global_config.speed * 60  # 60 seconds
	fuel_available = max_fuel

	bool_check = True

	def draw_fuel_bar(self, win, fuel_available, bool):
		if self.bar_color == (255,255, 0):
			self.fuel_available = self.max_fuel
		else:
			self.fuel_available = fuel_available
		win.blit(self.img_icon, (10, 140))

		if bool:
			# self.red += 255/self.max_fuel
			self.green -= 255/self.max_fuel

			if self.red >= 255:
				self.red == 255
			if self.green <0:
				self.green = 0

		self.bar_color = (int(self.red), int(self.green), 0)
		progress = self.fuel_available/self.max_fuel
		# print(progress)

		if self.bool_check:
			if progress <= 0.25:
				# print('inside')
				self.bool_check = False
				fuel = Fuel()
				Fuel.fuel_list.append(fuel)
	
		pygame.draw.rect(win, self.border_color, (*self.bar_pos, *self.bar_size), 3)
		innerPos  = (self.bar_pos[0]+3, self.bar_pos[1]+3)
		innerSize = ((self.bar_size[0]-6) * progress, self.bar_size[1]-6)
		pygame.draw.rect(win, self.bar_color, (*innerPos, *innerSize))

		return self.fuel_available

fuel_bar = Fuel_bar()

class Pause_button:
	"""
	Defines the mute button
	"""
	def __init__(self):
		self.centroid_x = 0
		self.centroid_y = 0

		self.img_original = pygame.image.load(os.path.join('Utils/Pics/Display', 'pause.png')).convert_alpha()
		self.img_small = pygame.transform.scale(self.img_original,(int(self.img_original.get_width()), int(self.img_original.get_height())))
		self.img_big = pygame.transform.scale(self.img_original,(int(self.img_original.get_width()*1.1), int(self.img_original.get_height()*1.1)))

		self.img = self.img_small
	
class Play_button:
	"""
	Defines the unmute button
	"""
	def __init__(self):
		self.centroid_x = 0
		self.centroid_y = 0

		self.img_original = pygame.image.load(os.path.join('Utils/Pics/Display', 'play.png')).convert_alpha()		
		self.img_small = pygame.transform.scale(self.img_original,(int(self.img_original.get_width()), int(self.img_original.get_height())))
		self.img_big = pygame.transform.scale(self.img_original,(int(self.img_original.get_width()*1.1), int(self.img_original.get_height()*1.1)))

		self.img = self.img_small

class Pause_play_button:
	"""
	For pausing the game.
	"""
	x = 760
	y = 40

	button_flag = False
	
	def __init__(self):
		# self.buttons_list = [unmute_button, mute_button]
		self.img = self.buttons_list[0].img
	
	def check_status(self, button, pop_sound_play):
		"""
		Checks whether the cursor is over the button. And if it is clicked inverts the status of the button i.e mute to unmute or vice versa.
		"""
		collision_with_button = cursor_over_button(cursor, button)

		# If the cursor is over button, button enlarges
		if collision_with_button:
			button.img = button.img_big		

			# If clicked, button is changed
			if event_module.right_click:
				button = self.buttons_list[not(self.buttons_list.index(button))]
				# Sound effect
				if pop_sound_play == False:
					music_module.sound_button_enlarge.play()
					pop_sound_play = True
				else:
					pop_sound_play = False
		else:
			button.img = button.img_small		

		self.draw(button)		
		self.functionality(button)

		return button, pop_sound_play

	def functionality(self, volume_button):
		
		if self.buttons_list.index(volume_button) == 1:
			pygame.mixer.music.stop()
			self.button_flag = True
		elif self.buttons_list.index(volume_button) == 0 and self.button_flag:
			pygame.mixer.music.play(-1)
			self.button_flag = False

	def draw(self, button):
		button.centroid_x = Volume_control.x - button.img.get_width()//2
		button.centroid_y = Volume_control.y - button.img.get_height()//2

		win.blit(button.img, (button.centroid_x, button.centroid_y))