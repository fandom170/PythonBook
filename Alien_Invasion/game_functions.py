import sys
from time import sleep

import pygame

from Alien_Invasion.bullet import Bullet
from Alien_Invasion.alien import Alien


def check_keydown_events(event, ai_settings, screen, stats, ship, aliens, bullets):
    """reaction for pressing of keys"""
    if event.key == pygame.K_RIGHT:
        # move ship right
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # move ship left
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_p:
        start_game(ai_settings, screen, stats, ship, aliens, bullets)


def start_game(ai_settings, screen, stats, ship, aliens, bullets):
    if not stats.game_active:
        stats.reset_stats()
        stats.game_active = True
        # Clearing of bullets list and alien list
        aliens.empty()
        bullets.empty()
        # Create new flit and put ship to the center
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def check_keyup_events(event, ship):
    """Reacts on freeng of key"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets):
    # Monitoring actions on keyboard and mouse
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, ship, aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Run new game after click on play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Mouse coursor becomes hidden
        pygame.mouse.set_visible(False)
        # reset game settings
        ai_settings.initialize_dynamic_settings()
        if play_button.rect.collidepoint(mouse_x, mouse_y):
            start_game(ai_settings, screen, stats, ship, aliens, bullets)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    # every loop run screen refreshes
    screen.fill(ai_settings.bg_color)
    #all bullets are displayed after image of ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # Displaying of score
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()


def update_bullets(ai_settings, screen, ship, aliens, bullets):
    """Update bullets positions and destroys old bullets"""
    # Bullet position update
    bullets.update()
    # deleting of bullets beyond screen border
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
    """Handling of collisions of bullets with aliens"""
    # If alien is hit, destroys bullet
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0:
        # Clearing existing bullets and creating of new fleet
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)


def fire_bullet(ai_settings, screen, ship, bullets):
    """shot a bullet if max still not reached"""
    # Creation of new bullet and adding it to bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

    # displaying of last drown screen
    pygame.display.flip()


def create_fleet(ai_settings, screen, ship, aliens):
    """Create alien invader fleet"""
    # Create alien and calculation of alien number in the row
    # Interval between aliens is equal to width of alien
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # Creation of first row of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # Creation of alien and put it to row
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_number_aliens_x (ai_settings, alien_width):
    """Calcualate amount of aliens in the row"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x/(2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create alien and put him in the row"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def get_number_rows(ai_settings, ship_height, alien_height):
    """Calculate number of rows which fits screen"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """"Check if alien fleet reached edge of screen
    after that updates positions of all aliens in the fleet"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Check Alien-Ship collisions
    if pygame.sprite.spritecollide(ship, aliens, True):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

    # checking of aliens which reached the bottom border of screen
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)


def check_fleet_edges(ai_settings, aliens):
    """React on reaching of alien to edge of screen"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Move down whole fleet and revert direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed

    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """Handles collsiion Ship with Aliens"""
    # Decresing ships_left
    if stats.ships_left > 0:
        stats.ships_left -= 1
        # Clearing aliens list and bullets list
        aliens.empty()
        bullets.empty()
        # Creating of new fleet and put ship to the center
        create_fleet(ai_settings, screen, ship, aliens)
        # Pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """Check reaching of aliien ship to bottom border of screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Same actions as for ship colliding
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break




