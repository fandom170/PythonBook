import pygame

from pygame.sprite import Sprite

class Alien(Sprite):
    """Class which descriped one alien invader"""

    def __init__(self, ai_settings, screen):
        """Initializes alien and set his stert position"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # loading of image and setting of rect attribute
        self.image = pygame.image.load('images/invader_ship.bmp')
        self.rect = self.image.get_rect()

        # Every new alien appears in top left corner of screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Saving of accurate alien position
        self.x = float(self.rect.x)

    def blitme(self):
        """Show alien invader ship  in particular position"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Move alien right or left"""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """Returns True if alien position is near the edge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

