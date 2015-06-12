__author__ = 'antoine'
"""
    Class to send actions to execute to the klearnel module
"""
import socket, re

from controller.Crypter import Crypter
from model.Exceptions import *

class Networker:
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
        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", host):
            ip_addr = host
        else:
            try:
                ip_addr = socket.gethostbyname(host)
            except:
                raise NoConnectivity("Unable to find "+host)
        try:
            self.s.connect((ip_addr, port))
        except:
            raise NoConnectivity("Unable to find "+host)

    def send_val(self, value):
        if type(value) is str:
            self.s.send(bytes(value, 'UTF-8'))
        elif type(value) is bytes:
            self.s.send(value)
        else:
            self.s.send(bytes(value))
        ack = self.s.recv(1).decode('UTF-8')
        if ack != self.SOCK_ACK:
            raise ConnectionError("The operation couldn't be executed on the device, error: "+ack)

    def get_ack(self):
        return self.s.recv(1).decode('UTF-8')

    def get_multiple_data(self, buf_size=20):
        result = []
        while True:
            new_v = self.s.recv(buf_size).decode('UTF-8')
            self.s.send(bytes(self.SOCK_ACK, 'UTF-8'))
            if new_v == 'EOF':
                break
            result.append(new_v)
        return result

    def get_data(self, buf_size):
        b_result = bytes()
        end = False
        for i in range(0, buf_size):
            char = self.s.recv(1)
            if not end:
                if char not in [b'\x00', b'\xff']:
                    b_result += char
                else:
                    for j in range(i, buf_size):
                        b_result += b'\x00'
                    end = True
        result = b_result.decode('UTF-8')
        return result.split('\x00')[0]

    def send_ack(self, value):
        self.s.send(bytes(value, 'UTF-8'))

if __name__ == '__main__':
    net = Networker()
    net.connect_to("antoine-laptop")
    net.send_val("KL19267280729489")
    if net.get_ack() != net.SOCK_ACK:
        print("Error on token negociation")
        exit("End of program")
    digest = Crypter.encrypt("PASSWORD")
    net.send_val(digest)

    if net.get_ack() != net.SOCK_ACK:
        print("Error on root password negociation")
    net.s.close()
