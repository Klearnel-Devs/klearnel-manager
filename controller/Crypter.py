__author__ = 'antoine'

from Crypto.Hash import SHA256


class Crypter():
    def encrypt(self, data_to_hash):
        h = SHA256.new()
        h.update(bytes(data_to_hash, 'UTF-8'))
        print(h.digest())
        return h.digest()