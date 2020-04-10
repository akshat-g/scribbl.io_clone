"""
represents a full game and handles operations related to games and connections/interations
between player, chat, board, round
"""

from player import Player
from board import Board
from round import Round
from mimetypes import guess

class Game(object):
    def __init__(self, id, players, thread):
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
        self.connected_thread = thread
        self.player_draw_ind = 0
        self._start_new_round()
        self._create_board()
        
    def _start_new_round(self):
        """
        starts a new round with a new word
        """
        self.round = Round(self.get_word(), self.players[self.player_draw_ind], self.players, self)
        self.player_draw_ind += 1
        
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
        pass
    
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
        # todo: implement the end gme
        pass
    
    def get_word(self):
        """
        returns a word that has not yet been used in the current game
        :return str
        """
        # TODO: get a list of words from somewhere
        pass