import sys
from nullx.net.tcp import TCP, TrafficRecorder
from nullx.net.udp import UDPDatagram

class connect:
    def __init__(self, target, port, buffer_size=1024):
        self.target = target
        self.port = port
        self.buffer_size = buffer_size
    
    def __enter__(self):
        self.conn = TCP(buffer_size=self.buffer_size)
        self.conn.connect(self.target, self.port)
        return self.conn
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

class listen:
    def __init__(self, port, host="", buffer_size=1024, backlog=5):
        self.port = port
        self.host = host
        self.buffer_size = buffer_size
        self.backlog = backlog
    
    def __enter__(self):
        self.server = TCP(buffer_size=self.buffer_size)
        self.server.listen(self.port, host=self.host, backlog=self.backlog)
        return self.server
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.server.close()
