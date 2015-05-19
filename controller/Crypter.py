__author__ = 'antoine'

from hashlib import sha256

class Crypter():
    def encrypt(self, data_to_hash):
        h = sha256()
        h.update(bytes(data_to_hash, 'UTF-8'))
        print(h.digest())
        return h.digest()