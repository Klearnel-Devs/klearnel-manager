__author__ = 'antoine'
"""
    Class to send actions to execute to the klearnel module
"""
import socket



class Networker(socket):
    """Class Networker to make interaction with Klearnel module"""
    s = None
    SOCK_ACK = "1"
    SOCK_NACK = "2"
    SOCK_DENIED = "3"
    SOCK_UNK = "4"
    SOCK_ABORTED = "8"
    SOCK_RETRY = "9"

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to(self, host, port=42225):
        ip_addr = self.gethostbyname(host)
        if ip_addr is None:
            raise Exception("Unable to find %s", host)

        if self.s.connect(ip_addr, port) is None:
            raise Exception("Unable to connect to %s", host)

    def send_val(self, value):
        self.s.send(value)
        return self.s.recv(2)

    def send_val(self, value, buf_size):
        self.s.send(value)
        return self.s.recv(buf_size)