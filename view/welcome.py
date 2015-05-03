__author__ = 'antoine'
"""
    Welcome Screen of the manager
"""
from kivy.app import App
from kivy.uix.widget import Widget


class LoginWindow(Widget):
    def show_login(self):
        Widget.size = 200


class Welcome(App):
    def set_title(self, title):
        return App(text=title)

