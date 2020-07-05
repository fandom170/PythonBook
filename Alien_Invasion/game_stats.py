

class GameStats():
    """Monitoring of statistic for Alien Invasion game"""
    def __init__(self, air_settings):
        """Initializes statistic"""
        self.ai_settings = air_settings
        self.reset_stats()
        self.game_active = False

    def reset_stats(self):
        """Initializes statistic, which changes during the game"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0

