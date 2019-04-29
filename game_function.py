import sys
from alian import Alian
import pygame
from game_stats import GameStats
from button import Button
from time import sleep
from bullet import Bullet
def check_keydown_events(event,ai_setting,screen,ship,bullets):
    if event.key == pygame.K_RIGHT:
        ship.move_right = True
    elif event.key == pygame.K_LEFT:
        ship.move_left = True
    elif event.key == pygame.K_SPACE:
        if len(bullets) < ai_setting.bullet_allowed:
            new_bullet = Bullet(ai_setting,screen,ship)
            bullets.add(new_bullet)
    elif event.key == pygame.K_q:
        sys.exit()
def check_keyup_events(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.move_right = False
    elif event.key == pygame.K_LEFT:
        ship.move_left = False
def check_event(ai_setting, screen, stats,sb, play_button, ship, alians, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_setting, screen, stats,sb, play_button, ship,alians, bullets, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_setting,screen,ship,bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
def screen(ai_setting,screen,stats,sb,ship,bullets,alians,play_button):
    screen.fill(ai_setting.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    alians.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()
def update_bullets(ai_setting,screen,stats,sb,ship,alians,bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_setting, screen, stats, sb, ship, alians, bullets)
def check_bullet_alien_collisions(ai_setting, screen,stats,sb, ship, alians, bullets):
    collisions = pygame.sprite.groupcollide(bullets,alians,True,True)
    if collisions:
        for alians in collisions.values():
            stats.score += ai_setting.alien_points * len(alians)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(alians) == 0:
        bullets.empty()
        ai_setting.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_setting, screen, ship, alians)
def create_fleet(ai_setting, screen,ship,alians):
    alian = Alian(ai_setting, screen)
    number_alian_x = get_number_alians_x(ai_setting, alian.rect.width)
    number_rows = get_number_rows(ai_setting,ship.rect.height,alian.rect.height)
    for row_number in range(number_rows):
        for alian_number in range(number_alian_x):
            create_alian(ai_setting, screen, alians, alian_number,row_number)
def get_number_alians_x(ai_setting, alian_width):
    available_space_x = ai_setting.screen_width - 2 * alian_width
    number_alian_x = int(available_space_x / (2 * alian_width))
    return number_alian_x
def create_alian(ai_setting, screen, alians, alian_number,row_number):
    alian = Alian(ai_setting, screen)
    alian_width = alian.rect.width
    alian.x = alian_width + 2 * alian_width * alian_number
    alian.rect.x = alian.x
    alian.rect.y = alian.rect.height + 2 * alian.rect.height * row_number
    alians.add(alian)
def get_number_rows(ai_setting, ship_height, alian_height):
    available_space_y = (ai_setting.screen_height-(3 * alian_height) - ship_height)
    number_rows = int(available_space_y / (2 * alian_height))
    return number_rows
def check_fleet_edges(ai_setting, alians):
    for alian in alians.sprites():
        if alian.check_edges():
            change_fleet_direction(ai_setting, alians)
            break
def change_fleet_direction(ai_setting, alians):
    for alian in alians.sprites():
        alian.rect.y += ai_setting.fleet_drop_speed
    ai_setting.fleet_direction *= -1
def update_alians(ai_setting,screen,stats,sb,ship,alians,bullets):
    check_fleet_edges(ai_setting, alians)
    alians.update()
    if pygame.sprite.spritecollideany(ship, alians):
        ship_hit(ai_setting, screen,stats,sb, ship, alians, bullets)
        print("Ship hit!!!")
    check_alians_bottom(ai_setting,screen,stats,sb, ship, alians, bullets)
def ship_hit(ai_setting, screen, stats, sb, ship, alians, bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()
        alians.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, alians)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
def check_alians_bottom(ai_setting, screen, stats, sb, ship, alians, bullets):
    screen_rect = screen.get_rect()
    for alian in alians.sprites():
        if alian.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_setting, stats, screen, ship, alians, bullets)
            break
def check_play_button(ai_setting, screen, stats, sb,play_button, ship, alians,bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_setting.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        alians.empty()
        bullets.empty()
        create_fleet(ai_setting, screen, ship, alians)
        ship.center_ship()
def check_high_score(stats,sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()










