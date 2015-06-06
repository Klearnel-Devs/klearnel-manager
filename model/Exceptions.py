__author__ = 'Derek'

class BadCredentials(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class NoConnectivity(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class EmptyFields(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class ScanException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class QrException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
