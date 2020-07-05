import pygame

from pygame.sprite import Sprite

class Bullet(Sprite):
    """Class for control of bullet which were sent by ship"""
    def __init__(self, ai_settings, screen, ship):
        super(Bullet, self).__init__()
        self.screen = screen

        # Creation of bullet in 0, 0 and set of correct position
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Position of bullet is stored in real format
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """Moves bullet to top of screen"""
        # update bullet podsition in real format
        self.y -= self.speed_factor
        # update of rectangle position
        self.rect.y = self.y

    def draw_bullet(self):
        """Displaying of bullet on the screen"""
        pygame.draw.rect(self.screen,self.color, self.rect)


