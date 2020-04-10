"""
Represents the state of the board
"""

class Board(object):
    ROWS = COL = 720
    
    def __init__(self):
        self.data = self._create_empty_board()
        
    def update(self, x, y, color):
        self.data[y][x] = color
    
    def _create_empty_board(self):
        return [[(255, 255, 255) for _ in range(self.COL)] for _ in range(self.ROWS)]  
    
    def clear(self):
        self.data = self._create_empty_board()
        
    def fill(self, x, y):
        pass
    
    def get_board(self):
        return self.data