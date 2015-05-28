__author__ = 'Derek'

from model.Client import *
from controller.Networker import *
def init():
    global cl
    global user
    user = None
    cl = ClientList()
    cl.load_list()
