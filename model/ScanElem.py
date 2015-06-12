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
        self.options = dict(BR_S=int(options[0]), DUP_S=int(options[1]), BACKUP=int(options[2]),
                            DEL_F_SIZE=int(options[3]), DUP_F=int(options[4]), INTEGRITY=int(options[5]),
                            CL_TEMP=int(options[6]), DEL_F_OLD=int(options[7]), BACKUP_OLD=int(options[8]))

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

    def __str__(self):
        return self.path + " - " + str(self.options) + " - " + str(self.back_limit_size) + " - " \
               + str(self.del_limit_size)

def sc_temp_create1():
    scan_e = ScanElem("/home/antoine/Documents")
    scan_e.set_options("000100000")
    scan_e.back_limit_size = 100
    scan_e.del_limit_size = 100
    scan_e.is_temp = 0
    scan_e.max_age = 15
    return scan_e

def sc_temp_create2():
    scan_e = ScanElem("/home/antoine/Images")
    scan_e.set_options("000101101")
    scan_e.back_limit_size = 100
    scan_e.del_limit_size = 100
    scan_e.is_temp = 0
    scan_e.max_age = 15
    return scan_e

def sc_temp_create3():
    scan_e = ScanElem("/home/antoine/Downloads")
    scan_e.set_options("101001000")
    scan_e.back_limit_size = 100
    scan_e.del_limit_size = 100
    scan_e.is_temp = 0
    scan_e.max_age = 15
    return scan_e

def sc_temp_create4():
    scan_e = ScanElem("/home/antoine/Trial")
    scan_e.set_options("010101010")
    scan_e.back_limit_size = 100
    scan_e.del_limit_size = 100
    scan_e.is_temp = 0
    scan_e.max_age = 15
    return scan_e

def sc_temp_create5():
    scan_e = ScanElem("/home/antoine/Test")
    scan_e.set_options("100101001")
    scan_e.back_limit_size = 100
    scan_e.del_limit_size = 100
    scan_e.is_temp = 0
    scan_e.max_age = 15
    return scan_e

if __name__ == '__main__':
    sc_e = sc_temp_create1()
    print(sc_e.get_options())