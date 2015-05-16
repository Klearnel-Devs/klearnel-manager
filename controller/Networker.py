__author__ = 'antoine'
"""
    Class to send actions to execute to the klearnel module
"""
import socket

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
        ip_addr = socket.gethostbyname(host)
        if ip_addr is None:
            raise Exception("Unable to find "+host)

        self.s.connect((ip_addr, port))

    def send_val(self, value):
        self.s.send(bytes(value, 'UTF-8'))
        ack = self.s.recv(2).decode('UTF-8')
        if ack != self.SOCK_ACK:
            raise Exception("The operation couldn't be executed on the device, error: "+ack)
        print(ack)

    def get_multiple_data(self, buf_size=20):
        result = []
        while True:
            new_v = self.s.recv(buf_size).decode('UTF-8')
            self.s.send(bytes(self.SOCK_ACK, 'UTF-8'))
            if new_v == 'EOF':
                break
            result.append(new_v)
        return result

if __name__ == '__main__':
    net = Networker()
    net.connect_to("antoine-laptop")
    net.send_val("IT WORSKKK")
    result = net.get_multiple_data()
    print(result)