## @package controller
#   Handles communication between Klearnel & Klearnel Manager
#
# @author Antoine Ceyssens <a.ceyssens@nukama.be> & Derek Van Hove <d.vanhove@nukama.be>
from hashlib import sha256

## Class used for Crypting data
class Crypter:
    @staticmethod
    def encrypt(data_to_hash):
        h = sha256()
        h.update(bytes(data_to_hash, 'UTF-8'))
        return h.digest()

