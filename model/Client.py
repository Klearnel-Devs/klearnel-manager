__author__ = 'antoine'
"""
    Class containing all modules connected to the manager
"""


class Client():
    token = None
    name = None
    last_ip = None
    last_seen = None

    def build(self, token, name):
        self.token = token
        self.name = name
    pass