__author__ = 'antoine'
"""
    Class containing all modules connected to the manager
"""
import os.path
import pickle


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
        pickle.dump(len(self.c_list), f)
        for i in range(0, len(self.c_list)):
            pickle.dump(self.c_list[i], f)
        f.close()
        self.c_list.clear()

    def load_list(self):
        if os.path.isfile(self.filename):
            f = open(self.filename, 'br')
            len = pickle.load(f)
            for i in range(0, len):
                obj = pickle.load(f)
                self.c_list.append(obj)
            f.close()

    def __str__(self):
        total = None
        for i in range(0, len(self.c_list)):
            total += self.c_list[i].__str__()+"\n"
        return total


class Client():
    token = None
    password = None
    name = None
    last_ip = ''
    last_activity = ''

    def __init__(self, token, name, encrypt_pwd):
        self.token = token
        self.name = name
        self.password = encrypt_pwd

    def set_ip(self, ip_addr):
        self.last_ip = ip_addr

    def set_last_activity(self, last_activity):
        self.last_activity = last_activity

    def __str__(self):
        return "Client "+self.name+": TK="+self.token+" last_ip="+\
               self.last_ip+" last_activity="+self.last_activity

if __name__ == '__main__':
    c = Client("12345", "TestName", "pkpfpkp234")
    cl = ClientList()
    cl.add_client(c)
    cl.save_list()
    cl.load_list()
    print(cl.c_list[0])