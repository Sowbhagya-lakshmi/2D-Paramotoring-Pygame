import pygame
import os

pygame.init()

#Sound Variables
sound_bird = pygame.mixer.Sound(os.path.join('Utils\Music\BirdSound.wav'))
sound_coins = pygame.mixer.Sound(os.path.join('Utils\Music\CoinsSound.wav'))
sound_collided = pygame.mixer.Sound(os.path.join('Utils\Music\CollidedSound.wav'))
