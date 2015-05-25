__author__ = 'antoine'


class ScanElem:
    path = None
    options = None
    back_limit_size = 0
    del_limit_size = 0
    is_temp = 0
    max_age = 0

    def __init__(self, path):
        self.path = path
