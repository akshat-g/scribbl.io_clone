"""
represents a full game and handles operations related to games and connections/interations
between player, chat, board, round
"""

import random
from player import Player
from board import Board
from round import Round

class Game(object):
    def __init__(self, id, players):
        """
        init the game once player threshold is met
        :param id: int
        :param players Player[]
        """
        self.id = id
        self.players = players
        self.words_used = []
        self.round = None
        self.board = Board()
        self.player_draw_ind = 0
        self.round_count = 1
        self._start_new_round()
        self._create_board()
        
    def _start_new_round(self):
        """
        starts a new round with a new word
        """
        round_word = self.get_word()
        self.words_used.append(round_word)
        self.round = Round(round_word, self.players[self.player_draw_ind], self.players, self)
        self.player_draw_ind += 1
        self.round_count += 1
        
        if self.player_draw_ind >= len(self.players):
            self.round.end_round()
            self.end_game()
        
        
    def player_guess(self, player, guessed_word):
        """
        makes the player guess the word
        """
        return self.round.guess(player, guessed_word)
    
    def player_disconnected(self, player):
        """
        call to clean up objects once player disconnects
        :param player Player
        :raises Exception()
        """
        if player in self.players:
            player_index = self.players.index(player)
            if player_index > self.player_draw_ind:
                self.player_draw_ind -= 1
            
            self.players.remove(player)
            self.round.player_left(player)
            
        else:
            raise Exception("Player not in game")
        
        if len(self.players) <= 3:
            self.end_game()
    
    def skip(self):
        """
        increments the round skips; if the skips are greater than threshold, a new
        round is started
        :raises Exception()
        :return None
        """
        if self.round:
            new_round = self.round.skip()
            if new_round:
                self.round_ended()
        else:
            raise Exception("No round is available to skip")
        
    def round_ended(self):
        self._start_new_round()
        self.board.clear()
    
    def update_board(self, x, y, color):
        """
        calls update method on board
        """
        if not self.board:
            raise Exception("No Board is created")
        self.board.update(x, y, color)
    
    def end_game(self):
        """
        ends the game
        """
        for player in self.players:
            self.round.player_left(player)
        pass
    
    def get_word(self):
        """
        returns a word that has not yet been used in the current game
        :return str
        """
        with open("words.txt", "r") as f:
            words = []
            
            for line in f:
                single_word = line.strip()
                if single_word not in self.words_used:
                    words.append(single_word)
            r = random.randint(0, len(words)-1)
            return words[r].strip()
        
    def get_player_scores(self):
        """
        returns a dictionary of player scores
        :return dict
        """
        scores = {player:player.get_score() for player in self.players}
        return scores