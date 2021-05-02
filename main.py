import pygame
from pygame.locals import *
import os
import sys
import math
import random
import time
import json

class Player(object):
	
	imgs = [pygame.image.load(os.path.join('pics', "player-"+ str(x) + '.png')) for x in range(1,10)]

	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height 
		self.runCount = 0
		
		# Border
		self.border_to_be_modified = read_json('player')
		self.border = set()

		for lst in self.border_to_be_modified:
			new_tup = (lst[0]+self.x, lst[1])
			self.border.add(new_tup)

	def draw (self, win):
		if self.runCount > 63:
			self.runCount = 0
		win.blit(self.imgs[self.runCount//9], (self.x,self.y))
		self.runCount += 1 

class Tree:
	tree_light = pygame.image.load('pics/tree_light.png')
	tree_dark = pygame.image.load('pics/tree_dark.png')
	cherry_tree = pygame.image.load('pics/cherry_tree.png')

	imgs = [tree_light, tree_dark, cherry_tree]
	resized_imgs = [pygame.transform.scale(img, (int(img.get_width()//1.5), int(img.get_height()//1.5))) for img in imgs]

	def __init__(self, x, y, tree_num):
		self.x = x
		self.y = y
		self.tree_num = tree_num
		self.border = read_json('tree')

	def draw(self,win):
		win.blit(self.resized_imgs[self.tree_num], (self.x, self.y)) 

def read_json(key):
	filename = 'contour_coordinates.json'
	with open(filename) as f:
		json_data = json.load(f)
	border_points = json_data[key]
	return border_points

def redrawWindow(bgX, bg_width, groundX, ground_width):
	# Drawing background
	win.blit(bg, (bgX, 0))
	win.blit(bg, (bg_width,0))

	# Background movement
	bgX -= 1.5
	bg_width -= 1.5
	
	# For repetition of background movement
	if bgX < bg.get_width() * -1:
		bgX = bg.get_width()
	if bg_width < bg.get_width() * -1:
		bg_width = bg.get_width()

	# Drawing obstacles
	for obstacle in obstacles:
		obstacle.draw(win)

	# Drawing ground
	win.blit(ground, (groundX, 0))
	win.blit(flipped_ground, (ground_width,0))	

	# Ground movement
	groundX -= foreground_speed
	ground_width -= foreground_speed
	
	# For repetition of ground movement
	if groundX < (ground.get_width()-5) * -1:
		groundX = (ground.get_width()-5)
	if ground_width < (flipped_ground.get_width()-5) * -1:
		ground_width = (flipped_ground.get_width()-5)

	return bgX, bg_width, groundX, ground_width

def create_obstacle(): 
	#Creates one obstacle
	random_num = random.randint(0,2)        # range over the number of obstacles
	random_x = random.randint(1550, 2000)   # range is defined such that the obstacle seems to be coming into the view smoothly
	if random_num == 0:
		obstacles.append(Tree(random_x,300,0))
	elif random_num == 1:
		obstacles.append(Tree(random_x,300,1))
	elif random_num == 2:
		obstacles.append(Tree(random_x,300,2))

def update_obstacle_position():
	for obstacle in obstacles:
		if obstacle.x < -400:
			obstacles.remove(obstacle)
		else:
			obstacle.x -= foreground_speed

def display_pointer(mx,my):
	font = pygame.font.Font('freesansbold.ttf', 32)
	text_x, text_y = 10, 10
	text = font.render(str(mx)+', '+str(my), True, (0,0,0))
	win.blit(text, (text_x, text_y))

def collision_message():
	font = pygame.font.Font('freesansbold.ttf', 100)
	text_x, text_y = 750, 100
	text = font.render('COLLISION', True, (0,0,0))
	win.blit(text, (text_x, text_y))

def collision():
	curr_player_border = set()
	for tup in player.border:
		new_tup = (tup[0], tup[1]+player.y)
		curr_player_border.add(new_tup)
	
	'''for point in curr_player_border:
		pygame.draw.circle(win, (255,0,0), point,3)
	pygame.display.update()'''

	for obstacle in obstacles:
		curr_obstacle_border = set()
		for lst in obstacle.border:
			new_tup = (lst[0]+obstacle.x, lst[1]+obstacle.y)
			curr_obstacle_border.add(new_tup)

		'''for point in curr_obstacle_border:
			pygame.draw.circle(win, (255,0,0), point,3)
		pygame.display.update()'''
		

		collision_points = curr_player_border.intersection(curr_obstacle_border)
		if len(collision_points) > 0:
			#print(collision_points)
			return True
	return False

# MAIN ALGORITHM

pygame.init()

# Game Window
W, H = 1550, 800
win = pygame.display.set_mode((W,H))
pygame.display.set_caption('Game Window')

# Background Image
bg = pygame.image.load(os.path.join('pics','bg.png')).convert()
bgX = 0
bg_width = bg.get_width()                             # to get width of the image

# Ground
ground = pygame.image.load(os.path.join('pics','ground.png'))
flipped_ground = pygame.transform.flip(ground, True, False)
groundX = 0
ground_width = ground.get_width() - 5

speed = 60		# fps
clock = pygame.time.Clock()
foreground_speed = 6

run = True
collision_occured = False
obstacles = []

player = Player(250, 313, 50, 50)	# Creating an instance of the class Player

# Setting a userevent once in every 8 seconds to generate obstacles
pygame.time.set_timer(pygame.USEREVENT+2, 8000)    

# GAME LOOP
while run:
	# Draws the stuff to be displayed in window
	bgX, bg_width, groundX, ground_width = redrawWindow(bgX, bg_width, groundX, ground_width)

	# Gets the mouse pointer coordinates
	(mx, my) = pygame.mouse.get_pos()

	# Displaying the mouse pointer coordinates for reference
	display_pointer(mx,my)
	   	
	# To limit the movable region
	if my < 560 :
		player.x, player.y = 250, my	# instead of loc
		player.draw(win)
	else:
		player.x, player.y = 250, 560
		player.draw(win)
	
	# Event loop
	for event in pygame.event.get():
		
		if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
			pygame.quit()
			sys.exit()
			run = False

		if event.type == pygame.USEREVENT+2:
			create_obstacle()
	
	update_obstacle_position()

	collision_occured = collision()	# Checks collision and returns boool 

	if collision_occured:		# Dummy exit
		collision_message()
		pygame.display.update()
		time.sleep(3)
		break

	clock.tick(speed)
	pygame.display.update()
	