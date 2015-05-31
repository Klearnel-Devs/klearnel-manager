__author__ = 'antoine'
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty

class ScanElem:
    path = StringProperty()
    options = ListProperty()
    back_limit_size = NumericProperty()
    del_limit_size = NumericProperty()
    back_limit_size = NumericProperty()
    del_limit_size = NumericProperty()
    is_temp = BooleanProperty()
    max_age = NumericProperty()

    def __init__(self, path, options, back, del_size, tmp, age):
        self.path = path
        self.options = options
        self.back_limit_size = back
        self.del_limit_size = del_size
        self.is_temp = tmp
        self.max_age = age

    def set_options(self, options):
        i = 0
        for c in options:
            self.options[i]
            i += 1
