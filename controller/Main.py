## @package controller
#   Handles communication between Klearnel & Klearnel Manager
#
# @author Antoine Ceyssens <a.ceyssens@nukama.be> & Derek Van Hove <d.vanhove@nukama.be>
from view.manager import ManagerApp
from controller import Active
from model.Client import *

Active.init()
mainView = ManagerApp()
mainView.run()


