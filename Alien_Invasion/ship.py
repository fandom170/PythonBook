import pygame


class Ship():

    def __init__(self, ai_settings, screen):
        """Initializes ship and set his start position"""
        self.screen = screen
        self.ai_settings = ai_settings

        # Loading of ship image and receiving of rectangle
        self.image = pygame.image.load('images/alien_ship1.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Every new ship appears near bottom edge of screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #Saving of coordinate of ship center
        self.center = float(self.rect.centerx)

        # flag of moving
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update ship position counting flags"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # Update rect based on self.center
        self.rect.centerx = self.center


    def blitme(self):
        """Drawing a ship in current position."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Put ship to the center of bottom side"""
        self.center = self.screen_rect.centerx