import sys
import pygame
from button import Button
from ship import Ship
from alian import Alian
from settings import Setting
import game_function as gf
from pygame.sprite import Group
from game_stats import GameStats
from scoreboard import Scoreboard
def game():
    pygame.init()
    ai_setting = Setting()
    screen=pygame.display.set_mode((ai_setting.screen_width,ai_setting.screen_height))
    pygame.display.set_caption('Alien invasion')
    play_button = Button(ai_setting, screen, "Play")
    stats = GameStats(ai_setting)
    sb = Scoreboard(ai_setting, screen, stats)
    bg_color = (220,220,220)
    alian = Alian(ai_setting, screen)
    ship = Ship(screen,ai_setting)
    bullets = Group()
    alians = Group()
    gf.create_fleet(ai_setting,screen,ship,alians)
    while True:
        gf.check_event(ai_setting, screen, stats,sb, play_button, ship, alians, bullets)
        gf.screen(ai_setting,screen,stats,sb,ship,bullets,alians,play_button)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_setting,screen, stats, sb, ship, alians, bullets)
            gf.update_alians(ai_setting, screen, stats, sb, ship, alians,bullets)
        pygame.display.flip()
        gf.screen(ai_setting,screen,stats,sb,ship,bullets,alians,play_button)
game()
