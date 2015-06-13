## @package model
#   Defines classes to be displayed by the GUI and handled by Controller
#
# @author Antoine Ceyssens <a.ceyssens@nukama.be> & Derek Van Hove <d.vanhove@nukama.be>
from kivy.properties import NumericProperty, StringProperty
from datetime import datetime, timedelta
from time import time

## Class representing a single Quarantine item
class QrElem:
    ## The items filename as it appears in the Quarantine
    f_name = None
    ## The items original location, including its original filename
    o_path = None
    ## The items entry date into the Quarantine
    d_begin = None
    ## The items expiration date from the Quarantine
    d_expire = None

    ## Constructor
    def __init__(self, name):
        self.f_name = name

    ## Formats entry timestamp into date format
    def get_begin(self):
        return datetime.fromtimestamp(int(self.d_begin)).strftime('%Y-%m-%d %H:%M:%S')

    ## Formats expiration timestamp into date format
    def get_expire(self):
        return datetime.fromtimestamp(int(self.d_expire)).strftime('%Y-%m-%d %H:%M:%S')

    ## String override
    def __str__(self):
        return self.f_name + " - " + self.o_path + " - " + self.get_begin() + " - " + self.get_expire()
