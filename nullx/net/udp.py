import socket

class UDPDatagram():
    def __init__(self, buffer_size=1024):
        self.buffer_size = buffer_size
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def send(self, target, port, data):
        sent = self.socket.sendto(data, (target, port))
        data, server = self.socket.recvfrom(self.buffer_size)
        return data
