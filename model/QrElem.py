__author__ = 'antoine'
from kivy.properties import NumericProperty, StringProperty
from datetime import datetime, timedelta
from time import time

class QrElem:
    f_name = None
    o_path = None
    d_begin = None
    d_expire = None

    def __init__(self, name):
        self.f_name = name

    def get_begin(self):
        return datetime.fromtimestamp(self.d_begin).strftime('%Y-%m-%d %H:%M:%S')

    def get_expire(self):
        return datetime.fromtimestamp(self.d_expire).strftime('%Y-%m-%d %H:%M:%S')

    def __str__(self):
        return self.f_name + " - " + self.o_path + " - " + self.get_begin() + " - " + self.get_expire()

def qr_temp_create():
    qr_e = QrElem("yolo.txt")
    qr_e.o_path = "/home/nuccah/yolo/yolo.txt"
    qr_e.d_begin = int(time())
    qr_e.d_expire = int(time()) + timedelta(days=30).seconds
    return qr_e

if __name__ == '__main__':
    qr_e = qr_temp_create()
    print(qr_e)
