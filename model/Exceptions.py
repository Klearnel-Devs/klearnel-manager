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

class EmptyListException(Exception):
    title = 'Empty List'
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
    title = 'Scanner Error'

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class QrException(Exception):
    title = 'Quarantine Error'

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class ConfigException(Exception):
    title = 'Configuration Error'

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
