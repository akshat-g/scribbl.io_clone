"""
represents a single round of the game
"""
import time as timer
from _thread import *

from chat import Chat

class Round(object):
    def __init__(self, word, player_drawing, players, game):
        """
        init object
        :param word: str
        :param player_dawing: Player
        :param players: Player[]
        """
        self.word = word
        self.player_drawing = player_drawing
        self.player_guessed = []
        self.skips = 0
        self.game = game
        self.players = players
        self.player_scores = {player: 0 for player in players}
        self.time = 75
        self.chat = Chat(self)
        start_new_thread(self.time_thread, ())
        
    def time_thread(self):
        """
        runs in thread to keep track of the time of the round
        :return None
        """
        while self.time > 0:
            timer.sleep(1)
            self.time -= 1
            
        self.end_round("Time is up")
        
    def skip(self):
        """
        returns true if skip threshold is met
        """
        self.skips += 1
        if self.skips > (len(self.players) - 2):
            return True
        
        return False
    
    def get_score(self, player):
        """
        returns a specific player's score
        """
        if player in self.player_scores:
            return self.player_scores[player]
        
        else:
            raise Exception("Player not in score list")
        
    def guess(self, player, guessed_word):
        """
        :returns bool if player guessed the word correctly
        :param player: Player
        :param guessed_word: str
        :return bool
        """
        correct = (guessed_word == self.word)
        if correct:
            self.player_guessed.append(player)
            return True
        
        return False
    
    def player_left(self, player):
        """
        removes player that left the game from scores
        :param player: Player
        :return None
        """
        if player in self.player_scores:
            del self.player_scores[player]
            
        if player in self.player_guessed:
            self.player_guessed.remove(player)
            
        if player == self.player_drawing:
            self.end_round("Player drawing quit the game")
            
    def end_round(self, msg):
        for player in self.players:
            player.update_score(self.player_scores[player])
        self.game.round_ended()
        
        