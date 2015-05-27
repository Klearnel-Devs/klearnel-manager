__author__ = 'Derek'
"""
    Klearnel Manager GUI
"""
from time import time
from kivy.app import App
from os.path import dirname, join
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen
from model.Client import *
from controller import Active
import sys

class ManagerScreen(Screen):
    fullscreen = BooleanProperty(False)

    def add_widget(self, *args):
        if 'content' in self.ids:
            return self.ids.content.add_widget(*args)
        return super(ManagerScreen, self).add_widget(*args)


class ManagerApp(App):
    index = NumericProperty(-1)
    current_title = StringProperty()
    time = NumericProperty(0)
    show_sourcecode = BooleanProperty(False)
    sourcecode = StringProperty()
    screen_names = ListProperty([])
    hierarchy = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screens = {}
        self.available_screens = {}

    def build(self):
        self.title = 'Klearnel Manager'
        self.available_screens = sorted([
            'Creation', 'Login', 'Chooser', 'Scanner', 'Quarantine',
            'Settings', 'AddServ'])
        self.screen_names = self.available_screens
        curdir = dirname(__file__)
        self.available_screens = [join(curdir, 'data', 'screens', '{}.kv'.format(fn)) for fn in self.available_screens]
        self.initial_screen()

    def initial_screen(self):
        if Active.user is None:
            self.get_index('Creation')
        else:
            self.get_index('Login')
        self.load_screen(self.index)

    def go_next_screen(self):
        self.index = (self.index + 1) % len(self.available_screens)
        self.load_screen(self.index)

    def get_index(self, page):
        for x in range(0, len(self.available_screens)):
            if self.available_screens[x].find(page) != -1:
                self.index = x

    def load_screen(self, index):
        if index in self.screens:
            sm = self.root.ids.sm
            sm.switch_to(self.screens[index], direction='left')
            self.current_title = self.screens[index].name
            return self.screens[index]
        print(self.screens)
        screen = Builder.load_file(self.available_screens[index].lower())
        self.screens[index] = screen
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='left')
        self.current_title = screen.name

    def register(self):
        self.get_index('Login')
        self.load_screen(self.index)

    def login(self):
        if not Active.cl.c_list:
            self.get_index('AddServ')
        else:
            self.get_index('Chooser')
        self.load_screen(self.index)

    def connect(self):
        self.get_index('Scanner')
        self.load_screen(self.index)

    def addsrv(self, server, pw, token):
        Active.cl.add_client(Client(token, server, pw))
        self.get_index('Chooser')
        self.load_screen(self.index)

    def on_pause(self):
        return True

    def on_resume(self):
        pass

    def go_previous_screen(self):
        self.index = (self.index - 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='right')
        self.current_title = screen.name
        self.update_sourcecode()

    def quit(self):
        sys.exit(0)

if __name__ == '__main__':
    ManagerApp().run()