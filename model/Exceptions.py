## @package model
#   Defines classes to be displayed by the GUI and handled by Controller
#
# @author Antoine Ceyssens <a.ceyssens@nukama.be> & Derek Van Hove <d.vanhove@nukama.be>

## Exception class for handling wrong credentials
class BadCredentials(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

## Exception class for handling connection failures
class NoConnectivity(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

## Exception class for handling empty quarantine and scanner lists
class EmptyListException(Exception):
    title = 'Empty List'
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

## Exception class for handling empty input fields
class EmptyFields(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

## Exception class for handling communication errors in regards to the Scanner
class ScanException(Exception):
    title = 'Scanner Error'

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

## Exception class for handling communication errors in regards to the Quarantine
class QrException(Exception):
    title = 'Quarantine Error'

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

## Exception class for handling communication errors in regards to Configuration Settings
class ConfigException(Exception):
    title = 'Configuration Error'

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
