__author__ = 'antoine'
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty

class QrElem:
    f_name = StringProperty()
    o_path = StringProperty()
    d_begin = NumericProperty()
    d_expire = NumericProperty()

    def __init__(self, f_name):
        self.f_name = f_name
