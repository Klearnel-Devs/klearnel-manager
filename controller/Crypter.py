__author__ = 'antoine'

from hashlib import sha256


class Crypter:
    @staticmethod
    def encrypt(data_to_hash):
        h = sha256()
        h.update(bytes(data_to_hash, 'UTF-8'))
        return h.digest()

