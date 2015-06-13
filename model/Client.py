## @package model
#   Defines classes to be displayed by the GUI and handled by Controller
#
# @author Antoine Ceyssens <a.ceyssens@nukama.be> & Derek Van Hove <d.vanhove@nukama.be>
import os.path
import pickle
from controller import Active
## Class containing all modules connected to the manager
class ClientList:
    ## List of clients contained in the client database
    c_list = []
    ## Path to the client database
    filename = '../client.db'

    ## Adds a client to the client database
    # @param client The client on which to connect
    def add_client(self, client):
        self.c_list.append(client)
        self.save_list(self)

    ## Removes a client from the client database
    # @param idx The index that the client is found
    def rm_client(self, idx):
        self.c_list.pop(idx)

    ## Finds a given client's index
    # @param client The client to find
    # @return The found client's index
    def search_client(self, client):
        return self.c_list.index(client)

    ## Saves the client list to the database
    def save_list(self):
        f = open(self.filename, 'bw')
        pickle.dump(len(self.c_list), f)
        for i in range(0, len(self.c_list)):
            pickle.dump(self.c_list[i], f)
        f.close()
        self.c_list.clear()
        self.load_list(self)

    ## Loads the client list
    def load_list(self):
        if os.path.isfile(self.filename):
            f = open(self.filename, 'br')
            length = pickle.load(f)
            for i in range(0, length):
                obj = pickle.load(f)
                if obj.user == Active.user:
                    self.c_list.append(obj)
            f.close()

    ## String override
    def __str__(self):
        total = str
        for i in range(0, len(self.c_list)):
            total += self.c_list[i].__str__()+"\n"
        return total

## Class representing a single Klearnel host
class Client:
    ## The user that added the client
    user = None
    ## The Klearnel token, generated when Klearnel is launched for the first time
    token = None
    ## The user inputted Klearnel password when Klearnel is launched for the first time
    password = None
    ## The hostname or IP address
    name = None

    ## Constructor
    def __init__(self, token, name, encrypt_pwd):
        from controller.Crypter import Crypter
        self.token = token
        self.name = name
        self.password = Crypter.encrypt(encrypt_pwd)
        self.user = Active.user

    ## String override
    def __str__(self):
        return self.name
