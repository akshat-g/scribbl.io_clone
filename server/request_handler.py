"""
MAIN THREAD
Handles all the connections, creating new games and requests from the clients
"""

import socket
from _thread import *
import time
import threading
from player import Player
from game import Game
from queue import Queue
import json



class Server(object):
    PLAYERS = 3
    def __init__(self):
        self.connection_queue = []
        self.game_id = 0


    def player_thread(self, conn, player):
        while True:
            try:
                # receive request
                data = conn.recv(1024)
                data = json.loads(data)
                
                keys = [key for key in data.keys()]
                send_msg = {key:[] for key in keys}
                
                for key in keys:
                    if key == -1: # get game, returns a list of players playing a game
                        if player.game:
                            send_msg[-1] = player.game.players
                            
                        else:
                            send_msg[-1] = []
                    
                    if player.game:
                        if key == 0: # guess
                            correct = player.game.player_guess(player, data[0][0])
                            send_msg[0] = correct
                            
                        elif key == 1: # skip
                            skip = player.game.skip()
                            send_msg[1] = skip
                            
                        elif key == 2: # get chat
                            content = player.game.round.chat.get_chat()
                            send_msg[2] = content
                            
                        elif key == 3: # get board
                            brd = player.game.board.get_board()
                            send_msg[3] = brd
                            
                        elif key == 4: # get score
                            score = player.game.get_player_scores()
                            send_msg[4] = scores
                            
                        elif key == 5: # get round
                            rnd = player.game.round_count
                            send_msg[5] = rnd
                            
                        elif key == 6: # get word
                            wrd = player.game.round.word
                            send_msg[6] = wrd
                            
                        elif key == 7: # get skips
                            skips = player.game.round.skips
                            send_msg[7] = skips
                            
                        elif key == 8: # update board
                            x, y, color = data[8][:3]
                            player.game.update_board(x, y, color)
                            
                        elif key == 9: # get round time
                            t = player.game.round.time
                            send_msg[9] = t
                        else:
                            raise Exception("Not a valid key")    
                
                conn.sendall(json.dumps(send_msg))
            except Exception as e:
                print ("[EXCEPTION]:" + player.get_name() +  "disconnected!! ", e)
                conn.close()
                # todo: call player disconnect method
                
    
    def handle_queue(self, player):
        """
        adds player to the queue and starts game if enough players are there
        """
        self.connection_queue.append(player)
        
        if len(self.connection_queue) > self.PLAYERS:
            game = Game(self.connection_queue[:], self.game_id)
            
            for p in self.connection_queue:
                p.set_game(game)
             
            self.game_id += 1   
            self.connection_queue = []

    def authentication(self, conn, addr):
        """
        try to do some basic authentication
        """
        try:
            data = conn.recv(512)
            name = str(data.decode())
            if not name:
                raise Exception("No Name received")
            
            conn.sendall("1".encode())
            player = Player(addr, name)
            
            self.handle_queue(player)
            thread = threading.Thread(target=self.player_thread, args=(conn, player))
            thread.start()
        except Exception as e:
            print ("[EXCEPTION]: ", e)
            conn.close()
        

    def connection_thread(self):
        server = "localhost"
        port = 5555
    
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        try:
            s.bind((server, port))
        except socket.error as e:
            str(e)
        
        s.listen()
        print ("waiting for the connections; Server started")
    
        while True:
            conn, addr = s.accept()
        
            print ("[CONNECT] New Connection!!!")
            
            self.authentication(conn, addr)
        
        
if __name__ == "__main__":
    s = Server()
    thread = threading.Thread(target=s.connection_thread)
    thread.start()
    




