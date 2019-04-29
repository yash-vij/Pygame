import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
	def __init__(self,screen,ai_setting):
		super(Ship, self).__init__()
		self.screen = screen
		self.ai_setting = ai_setting
		self.image = pygame.image.load('Ship.gif')
		self.rect = self.image.get_rect()
		self.screen_rect = self.screen.get_rect()
		self.rect.bottom=self.screen_rect.bottom
		self.rect.centerx=self.screen_rect.centerx
		self.move_right = False
		self.center = float(self.rect.centerx)
		self.move_left = False
	def update(self):
		if self.move_right and self.rect.right < self.screen_rect.right:
			self.center += self.ai_setting.ship_speed_factor
		if self.move_left and self.rect.left >0:
			self.center -= self.ai_setting.ship_speed_factor
		self.rect.centerx=self.center			
	def blitme(self):
		self.screen.blit(self.image,self.rect)
	def center_ship(self):
		self.center = self.screen_rect.centerx

