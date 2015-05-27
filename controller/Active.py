__author__ = 'Derek'

from model.Client import *
from model.Client import Client
from controller.Crypter import Crypter

def init():
    global cl
    global user
    user = None
    cl = ClientList()
    cl.load_list()
