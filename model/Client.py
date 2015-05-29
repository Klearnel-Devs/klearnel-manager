__author__ = 'antoine'
"""
    Class containing all modules connected to the manager
"""
import os.path
import pickle

class ClientList:
    c_list = []
    filename = '../client.db'

    def add_client(self, client):
        self.c_list.append(client)
        self.save_list()

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
        self.load_list()

    def load_list(self):

        if os.path.isfile(self.filename):
            f = open(self.filename, 'br')
            length = pickle.load(f)
            for i in range(0, length):
                obj = pickle.load(f)
                self.c_list.append(obj)
            f.close()

    def __str__(self):
        total = str
        for i in range(0, len(self.c_list)):
            total += self.c_list[i].__str__()+"\n"
        return total


class Client:
    user = None
    token = None
    password = None
    name = None

    def __init__(self, user, token, name, encrypt_pwd):
        from controller.Crypter import Crypter
        self.token = token
        self.name = name
        self.password = Crypter.encrypt(encrypt_pwd)
        self.user = Crypter.encrypt(user)

    def __str__(self):
        return self.name

if __name__ == '__main__':
    from controller.Crypter import Crypter
    password = Crypter.encrypt("PASSWORD")
    c = Client("KL19267280729489", "antoine-laptop", password)
    cl = ClientList()
    cl.load_list()
    cl.add_client(c)
    cl.save_list()