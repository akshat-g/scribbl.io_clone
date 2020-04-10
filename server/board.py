"""
Represents the state of the board
"""

class Board(object):
    ROWS = COL = 720
    
    def __init__(self):
        """
        init the board 
        """
        self.data = self._create_empty_board()
        
    def update(self, x, y, color):
        """
        updates a single pixel of the board
        """
        self.data[y][x] = color
    
    def _create_empty_board(self):
        return [[(255, 255, 255) for _ in range(self.COL)] for _ in range(self.ROWS)]  
    
    def clear(self):
        """
        clears board to full white
        """
        self.data = self._create_empty_board()
        
    def fill(self, x, y):
        pass
    
    def get_board(self):
        """
        returns the data of the board
        """
        return self.data