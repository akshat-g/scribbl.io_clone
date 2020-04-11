import socket
import json
import time

class Network(object):
    def __init__(self, name):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.name = name
        self._connect()
        
    
    def _connect(self):
        try:
            self.client.connect(self.addr)
            self.client.sendall(self.name.encode())
            
            return json.loads(self.client.recv(1024))
        
        except Exception as e:
            self._disconnect(e)
            
    def _disconnect(self, msg):
        print("[EXCEPTION] Disconnected from server:", msg)
        self.client.close()
        

if __name__ == "__main__":        
    n = Network("akshat_g")