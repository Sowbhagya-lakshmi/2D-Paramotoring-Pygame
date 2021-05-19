import pygame
import os

pygame.init()

#Sound Variables
Sound_Bird = pygame.mixer.Sound(os.path.join('Utils\Music\BirdSound.wav'))
Sound_Coins = pygame.mixer.Sound(os.path.join('Utils\Music\CoinsSound.wav'))
Sound_Collided = pygame.mixer.Sound(os.path.join('Utils\Music\CollidedSound.wav'))
