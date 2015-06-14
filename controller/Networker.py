## @package controller
#   Handles communication between Klearnel & Klearnel Manager
#
# @author Antoine Ceyssens <a.ceyssens@nukama.be> & Derek Van Hove <d.vanhove@nukama.be>
import socket, re

from controller.Crypter import Crypter
from model.Exceptions import *

## Class that sends/receives information between Klearnel & Klearnel Manager
class Networker:
    s = None
    SOCK_ACK = "1"
    SOCK_NACK = "2"
    SOCK_DENIED = "3"
    SOCK_UNK = "4"
    SOCK_ABORTED = "8"
    SOCK_RETRY = "9"

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ## Method that initiations connection between Klearnel & Klearnel Manager
    # @param host The host as an IP address or hostname
    # @param port The port on which to connect
    # @throws NoConnectivity
    def connect_to(self, client, port=42225):
        try:
            if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", client.ip):
                ip_addr = client.ip
            else:
                ip_addr = socket.gethostbyname(client.name)
            self.s.connect((ip_addr, port))
        except:
            raise NoConnectivity("Unable to find "+client.name)

    ## Method that formats and sends data through the open socket
    # @param value The value to send
    # @throws ConnectionError Raised if ack not positive
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

    ##  Returns an ACK decoded in UTF8
    def get_ack(self):
        return self.s.recv(1).decode('UTF-8')

    ## Receives data that must be appended to a variable
    # @param buf_size The size of the packets to receive, defaults to 20
    # @return Returns the decoded data
    def get_multiple_data(self, buf_size=20):
        result = []
        while True:
            new_v = self.s.recv(buf_size).decode('UTF-8')
            self.s.send(bytes(self.SOCK_ACK, 'UTF-8'))
            if new_v == 'EOF':
                break
            result.append(new_v)
        return result

    ## Retrives and decodes socket data
    # @param buf_size The size of the packets to receive
    # @return Returns the decoded data
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

    ## Sends an ACK in UTF8
    # @param value The value to send
    def send_ack(self, value):
        self.s.send(bytes(value, 'UTF-8'))

