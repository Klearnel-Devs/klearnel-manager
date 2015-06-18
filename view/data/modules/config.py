## @package view
#   Defines classes to be displayed by the GUI
#
# @author Antoine Ceyssens <a.ceyssens@nukama.be> & Derek Van Hove <d.vanhove@nukama.be>

from kivy.app import App
from os.path import *
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
import sys
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListItemButton, ListView, CompositeListItem, ListItemLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from controller.Networker import *
from controller.Tasker import *
from model.Client import Client
from controller import Active
from model.Config import Config
from model.QrElem import *
from model.ScanElem import *
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput

## Subclass of text input
class CfgTextInput(TextInput):
    ## Contains a section value
    value1 = StringProperty('', allownone=True)
    ## Contains a key value
    value2 = StringProperty('', allownone=True)

    ## Constructor
    def __init__(self, **kwargs):
        self.value1 = kwargs.get('value', '')
        self.value2 = kwargs.get('value', '')
        super(CfgTextInput, self).__init__(**kwargs)

class CfgCheckBox(CheckBox):
    ## Contains a section value
    value1 = StringProperty('', allownone=True)
    ## Contains a key value
    value2 = StringProperty('', allownone=True)

    ## Constructor
    def __init__(self, **kwargs):
        self.value1 = kwargs.get('value', '')
        self.value2 = kwargs.get('value', '')
        super(CfgCheckBox, self).__init__(**kwargs)