import os
import pygame

from module import foreground_module

class Player:
	"""
	Descibes the player object.
	It has info such as the x positon, y position, width, height and a draw method to draw the
    player's images onto the screen hence creating the animation effect.
	"""
	# Loading player images
	num_of_player_imgs = 9
	imgs = [pygame.image.load(os.path.join('Utils/Pics/Player/', "player-"+ str(x) + '.png')) for x in range(1, num_of_player_imgs+1)]

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.runCount = 0

	def draw(self, win):
		self.frames_per_image = 7			# each player image is drawn for 7 consecutive frames
		if self.runCount > self.frames_per_image*self.num_of_player_imgs :
			self.runCount = 0
		self.img = self.imgs[self.runCount//self.num_of_player_imgs]
		win.blit(self.img, (self.x,self.y))
		self.runCount += 1 

player = Player(250, 313)	# Creating an instance of the class Player

def draw_player(win):
	(mx, my) = pygame.mouse.get_pos()

	# Display mouse pointer coordinates for reference
	display_mouse_pointer_coordinates(mx,my, win)
		
	# limit player's movable region
	if my < foreground_module.ground_y :
		player.x, player.y = 250, my
		player.draw(win)
	else:
		player.x, player.y = 250, foreground_module.ground_y
		player.draw(win)

def display_mouse_pointer_coordinates(mx,my, win):
	"""
	To display mouse pointer coordinates just for reference. Temporary function to be removed later.
	"""
	font_size = 32
	font = pygame.font.Font('freesansbold.ttf', font_size)
	text_x_pos, text_y_pos = 1400, 10
	text = font.render(str(mx)+', '+str(my), True, (0,0,0))
	win.blit(text, (text_x_pos, text_y_pos))