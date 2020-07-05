import pygame

from pygame.sprite import Group

from Alien_Invasion.settings import Settings
from Alien_Invasion.ship import Ship
from Alien_Invasion.game_stats import GameStats
from Alien_Invasion.button import Button
from Alien_Invasion.scoreboard import Scoreboard

import Alien_Invasion.game_functions as gf


def run_game():
    # Initialize game and creates screen object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    # Creating of 'Play' button
    play_button = Button(ai_settings, screen, "Play")
    # Create instance for storing of game statistic
    stats = GameStats(ai_settings)
    # Creation of ship
    ship = Ship(ai_settings, screen)
    # Creation of group for bullets storing
    bullets = Group()
    # Creation of group for alien fleet storing
    aliens = Group()
    # Creation of instances of scoreboard
    sb = Scoreboard(ai_settings, screen, stats)

    # Creation of fleet
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Run of main game cycle
    while True:
        gf.check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)




run_game()

