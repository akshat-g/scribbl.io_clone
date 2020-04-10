"""
Player class represents a player object on the server side
Each player will represent one connection; hence ip is the property of the player
"""

from constants import INITIAL_PLAYER_SCORE
from game import Game

class Player(object):
    def __init__(self, ip, name):
        """
        init the player object
        """
        self.game = None
        self.ip = ip
        self.name = name
        self.score = INITIAL_PLAYER_SCORE
        
    
    def set_game(self, game):
        """
        sets the game for the player
        """
        self.game = game
        
    def update_score(self, points):
        self.score += points
        
    def guess(self, guessed_string):
        """
        makes a player guess
        """
        return self.game.player_guess(self, guessed_string)
    
    def disconnect(self):
        """
        disconnects the player from the game
        """
        pass
    
    def get_score(self):
        return self.score
    
    def get_name(self):
        """
        returns a player's name
        """
        return self.name
    
    def get_ip(self):
        """
        return player's ip address
        """
        return self.ip
    


