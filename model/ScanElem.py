## @package model
#   Defines classes to be displayed by the GUI and handled by Controller
#
# @author Antoine Ceyssens <a.ceyssens@nukama.be> & Derek Van Hove <d.vanhove@nukama.be>

from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty

## Class representing a scanner element
class ScanElem:
    ## The path to be scanned
    path = None
    ## The scanner options in the form of a python dict
    options = None
    ## The size from which to backup
    back_limit_size = None
    ## The size from which to delete
    del_limit_size = None
    ## Determines whether the element is a temporary folder
    is_temp = None
    ## Maximum age of files if directory or file if file
    max_age = None

    ## Constructor
    def __init__(self, path):
        self.path = path

    ## Sets the dictionary values
    # @param options The options in the form of a string
    def set_options(self, options):
        self.options = dict(BR_S=int(options[0]), DUP_S=int(options[1]), BACKUP=int(options[2]),
                            DEL_F_SIZE=int(options[3]), DUP_F=int(options[4]), INTEGRITY=int(options[5]),
                            CL_TEMP=int(options[6]), DEL_F_OLD=int(options[7]), BACKUP_OLD=int(options[8]))

    ## Transforms options dictionary values into string of options
    def get_options(self):
        opt = str(self.options['BR_S'])
        opt += str(self.options['DUP_S'])
        opt += str(self.options['BACKUP'])
        opt += str(self.options['DEL_F_SIZE'])
        opt += str(self.options['DUP_F'])
        opt += str(self.options['INTEGRITY'])
        opt += str(self.options['CL_TEMP'])
        opt += str(self.options['DEL_F_OLD'])
        opt += str(self.options['BACKUP_OLD'])
        return opt

    ## String override
    def __str__(self):
        return self.path + " - " + str(self.options) + " - " + str(self.back_limit_size) + " - " \
               + str(self.del_limit_size)
