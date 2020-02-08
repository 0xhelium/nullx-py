import sys
import time
import socket
import select

class DataPacket:
    IN = 0
    OUT = 1
    def __init__(self, data, direction):
        self.timestamp = time.time()
        self.data = data
        self.direction = direction

class TrafficRecorder:
    IN = DataPacket.IN
    OUT = DataPacket.OUT
    def __init__(self):
        self.packets = []
    
    def bytedata(self, direction_filter=None):
        data = bytearray()
        for p in self.packets:
            if direction_filter is not None:
                if p.direction == direction_filter:
                    data += p.data
            else:
                data += p.data
        return data
    
    def record(self, data, direction):
        self.packets.append(DataPacket(data, direction))
    
    def reset(self):
        self.packets.clear()

class TCPSocket:
    def __init__(self, soc, buffer_size=1024, addr=None):
        self.socket = soc
        self.buffer_size = buffer_size
        self.traffic_recorder = None
        self.addr = addr
    
    def recv(self, buffer_size=None):
        data = self.socket.recv(self.buffer_size if buffer_size is None else buffer_size)
        if self.traffic_recorder is not None:
            self.traffic_recorder.record(data, DataPacket.IN)
        return data
    
    def recvall(self, timeout=1.0):
        data = bytes()
        while True:
            r, w, e = select.select([self.socket], [], [], timeout)
            if r:
                data += self.recv()
            else:
                return data
    
    def receive_while(self, test, buffer_size=None):
        data = self.recv(buffer_size=buffer_size)
        collected = data
        while test(data):
            data = self.recv()
            collected += data
        return collected

    def receive_until_key(self, key):
        class Test:
            def __init__(self):
                self.lastByte = 0
                self.firstByte = True
                self.streak = 0
            def test(self, d):
                if self.firstByte:
                    self.firstByte = False
                else:
                    if key[self.streak] == d[0]:
                        self.streak += 1
                    else:
                        self.streak = 0
                    if self.streak >= len(key):
                        return False
                self.lastByte = d[0]
                return True
        test = Test()
        return self.receive_while(test.test, buffer_size=1)

    def send(self, data, encoding="utf-8"):
        if isinstance(data, str):
            data = data.encode(encoding)
        self.socket.send(data)
        if self.traffic_recorder is not None:
            self.traffic_recorder.record(data, DataPacket.OUT)

    def close(self):
        self.socket.close()

    @staticmethod
    def encode(data, encoding="utf-8"):
        return data.encode(encoding)
    
    @staticmethod
    def decode(data, encoding="utf-8"):
        return data.decode(encoding)

class TCP(TCPSocket):
    def __init__(self, buffer_size=1024):
        super().__init__(socket.socket(socket.AF_INET, socket.SOCK_STREAM), buffer_size=buffer_size)
    
    def reset(self):
        self.socket.shutdown()
    
    def accept(self):
        conn, addr = self.socket.accept()
        return TCPSocket(conn, addr=addr)

    def listen(self, port, host="", backlog=5):
        self.socket.bind((host, port))
        self.socket.listen(backlog)
    
    def connect(self, target, port):
        self.socket.connect((target, port))
