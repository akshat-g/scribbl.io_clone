"""
represents and stores information about chat
"""

from round import Round

class Chat(object):
    def __init__(self, round):
        self.content = []
        self.round = round
        
    def update_chat(self, msg):
        self.content.append(msg)
        
    def get_chat(self):
        return self.content
    
    def __len__(self):
        return len(self.content)
    
    def __str__(self):
        return " ".join(self.content)
    
    def __repr__(self):
        return str(self)
    