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
from kivy.uix.carousel import Carousel
from kivy.uix.label import Label
import sys
from kivy.uix.modalview import ModalView
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListItemButton, ListView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

class ManagerScreen(Screen):
    fullscreen = BooleanProperty(False)

    def add_widget(self, *args):
        if 'content' in self.ids:
            return self.ids.content.add_widget(*args)
        return super(ManagerScreen, self).add_widget(*args)

class ListViewModal(BoxLayout):
    data = ListProperty()

    def __init__(self, **kwargs):
        self.data = [{'text': str(Active.cl.c_list[i]), 'is_selected': False} for i in range(len(Active.cl.c_list))]
        args_converter = lambda row_index, rec: {'text': rec['text'],
                                             'size_hint_y': None,
                                             'height': 25}
        self.list_adapter = ListAdapter(data=self.data,
                                        args_converter=args_converter,
                                        cls=ListItemButton,
                                        selection_mode='single',
                                        allow_empty_selection=False)

        super(ListViewModal, self).__init__(**kwargs)
        self.add_widget(ListView(adapter=self.list_adapter))
        Clock.schedule_interval(self.update_data, 5)

    def update_data(self, dt):
        if len(self.data) != len(Active.cl.c_list):
            for x in range(len(self.data), len(Active.cl.c_list)):
                self.data.append({'text': str(Active.cl.c_list[x]), 'is_selected': False})
                self.list_adapter.update_for_new_data()
                print("Added")


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