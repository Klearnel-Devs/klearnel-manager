__author__ = 'antoine'
"""
 Main class of the program
"""
from view.manager import ManagerApp
from controller import Active
from model.Client import *

Active.init()
mainView = ManagerApp()
mainView.run()


