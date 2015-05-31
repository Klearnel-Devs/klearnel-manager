__author__ = 'antoine'
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty



class ScanElem:
    path = None
    options = None
    back_limit_size = None
    del_limit_size = None
    is_temp = None
    max_age = None

    def __init__(self, path):
        self.path = path

    def set_options(self, options):
        self.options = dict(BR_S=options[0], DUP_S=options[1], BACKUP=options[2],
                            DEL_F_SIZE=options[3], DUP_F=options[4], FUSE=options[5],
                            INTEGRITY=options[6], CL_TEMP=options[7], DEL_F_OLD=options[8],
                            BACKUP_OLD=options[9])

    def __str__(self):
        return self.path + " - " + str(self.options) + " - " + str(self.back_limit_size) + " - " \
               + str(self.del_limit_size)

def sc_temp_create():
    scan_e = ScanElem("/home/antoine/Images")
    scan_e.set_options("1011000000")
    scan_e.back_limit_size = 100
    scan_e.del_limit_size = 100
    scan_e.is_temp = 0
    scan_e.max_age = 15
    return scan_e

if __name__ == '__main__':
    sc_e = sc_temp_create()
    print(sc_e)