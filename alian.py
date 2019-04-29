import pygame
from pygame.sprite import Sprite
class Alian(Sprite):
    def __init__(self,ai_setting,screen):
        super(Alian, self).__init__()
        self.screen=screen
        self.ai_setting=ai_setting
        self.image=pygame.image.load('Alian.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
    def blitme(self):
        self.screen.blit(self.image, self.rect)
    def update(self):
        self.x += self.ai_setting.alian_speed_factor
        self.rect.x = self.x
        self.x += (self.ai_setting.alian_speed_factor * self.ai_setting.fleet_direction)
    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
         return False
