__author__ = 'antoine'
"""
    Class containing all modules connected to the manager
"""
import os.path


class ClientList():
    c_list = []
    filename = 'client.db'

    def add_client(self, client):
        self.c_list.append(client)

    def rm_client(self, idx):
        self.c_list.pop(idx)

    def search_client(self, client):
        return self.c_list.index(client)

    def save_list(self):
        f = open(self.filename, 'bw')
        for i in range(0, len(self.c_list) - 1):
            f.write(self.c_list[i])
        f.close()
        self.c_list.clear()

    def load_list(self):
        if os.path.isfile(self.filename):
            f = open(self.filename, 'br')
            obj = f.readline()
            while obj != '':
                self.c_list.append(obj)
                obj = f.read(len(Client))
            f.close()


class Client():
    token = None
    name = None
    last_ip = ''
    last_activity = ''

    def __init__(self, token, name):
        self.token = token
        self.name = name

    def __str__(self):
        return "Client "+self.name+": TK="+self.token+" last_ip="\
               +self.last_ip+" last_activity="+self.last_activity

if __name__ == '__main__':
    c = Client(12345, "TestName")
    cl = ClientList()
    cl.add_client(c)
    cl.save_list()
    cl.load_list()
    print(cl.c_list)