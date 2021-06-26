import pygame
import os

pygame.init()

#Sound Variables
sound_bird = pygame.mixer.Sound(os.path.join('Utils\Music\BirdSound.wav'))
sound_coins = pygame.mixer.Sound(os.path.join('Utils\Music\CoinsSound.wav'))
sound_collided = pygame.mixer.Sound(os.path.join('Utils\Music\CollidedSound.wav'))
sound_aftercollided = pygame.mixer.Sound(os.path.join('Utils\Music\AfterCollidedSound.wav'))


sound_button_click = pygame.mixer.Sound(os.path.join(r'Utils\Music\button_click_soundeffect.wav'))
sound_button_enlarge = pygame.mixer.Sound(os.path.join(r'Utils\Music\button_enlarge_soundeffect.wav'))