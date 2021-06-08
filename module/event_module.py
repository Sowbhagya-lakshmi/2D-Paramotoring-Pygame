import pygame
import sys

from module import bird_module
from module import coins_module
from module import obstacles_module


def setting_up_events():
	# Generate coin once in every 1 seconds
	pygame.time.set_timer(pygame.USEREVENT+1, 1000)
	# Generate tree obstacles once in every 8 seconds
	pygame.time.set_timer(pygame.USEREVENT+2, 6000)
	# Generate rock and bush obstacles once in every 20 seconds
	pygame.time.set_timer(pygame.USEREVENT+3, 10000)
    # Generate bird obstacle once in every 8 seconds
	pygame.time.set_timer(pygame.USEREVENT+4, 8000)

	pygame.event.set_blocked(None)
	pygame.event.set_allowed([pygame.KEYDOWN, pygame.QUIT, pygame.USEREVENT+1,
                             pygame.USEREVENT+2, pygame.USEREVENT+3, pygame.USEREVENT+4])

def  event_loop():
    for event in pygame.event.get():		
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()		
        if event.type == pygame.KEYDOWN:
            if event.key == 27:		# press esc to quit
                pygame.quit()
                sys.exit()		
        if event.type == pygame.USEREVENT+1:
            coins_module.create_coin()
        if event.type == pygame.USEREVENT+2:
            obstacles_module.create_tree_obstacle()
        if event.type == pygame.USEREVENT+3:
            obstacles_module.create_rock_n_bush()
        if event.type == pygame.USEREVENT+4:
            bird_module.create_bird()


