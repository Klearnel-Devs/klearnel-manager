__author__ = 'Derek'
"""
    Klearnel Manager GUI
"""
from time import time
from kivy.app import App
from os.path import *
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
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from controller.Crypter import Crypter
from kivy.uix.button import Button
import ast
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from controller.Networker import *
from model.Exceptions import *
import re
from kivy.uix.actionbar import ActionBar

class ManagerScreen(Screen):
    fullscreen = BooleanProperty(False)

    def add_widget(self, *args):
        if 'content' in self.ids:
            return self.ids.content.add_widget(*args)
        return super(ManagerScreen, self).add_widget(*args)


class ScannerItem(ListItemButton):
    pass


class QuarantineItem(ListItemButton):
    pass


class ListItems(ListItemButton):
    pass


class ScannerViewModal(BoxLayout):
    data = ListProperty()

    def __init__(self, **kwargs):
        self.data = [{'text': format(i), 'is_selected': False} for i in range(0, 50)]
        args_converter = lambda row_index, rec: {'text': rec['text'],
                                                 'size_hint_y': None,
                                                 'height': 25}
        self.list_adapter = ListAdapter(data=self.data,
                                        args_converter=args_converter,
                                        cls=ScannerItem,
                                        selection_mode='single',
                                        allow_empty_selection=False)

        super(ScannerViewModal, self).__init__(**kwargs)
        self.add_widget(ListView(adapter=self.list_adapter))


class QuarantineViewModal(BoxLayout):
    data = ListProperty()

    def __init__(self, **kwargs):
        self.data = [{'text': format(i), 'is_selected': False} for i in range(0, 50)]
        args_converter = lambda row_index, rec: {'text': rec['text'],
                                                 'size_hint_y': None,
                                                 'height': 25}
        self.list_adapter = ListAdapter(data=self.data,
                                        args_converter=args_converter,
                                        cls=QuarantineItem,
                                        selection_mode='single',
                                        allow_empty_selection=False)

        super(QuarantineViewModal, self).__init__(**kwargs)
        self.add_widget(ListView(adapter=self.list_adapter))


class ListViewModal(BoxLayout):
    data = ListProperty()

    def __init__(self, **kwargs):
        self.data = [{'text': str(Active.cl.c_list[i]), 'is_selected': False} for i in range(len(Active.cl.c_list))]
        args_converter = lambda row_index, rec: {'text': rec['text'],
                                                 'size_hint_y': None,
                                                 'height': 25}
        self.list_adapter = ListAdapter(data=self.data,
                                        args_converter=args_converter,
                                        cls=ListItems,
                                        selection_mode='single',
                                        allow_empty_selection=False)
        super(ListViewModal, self).__init__(**kwargs)
        self.add_widget(ListView(adapter=self.list_adapter))



class ManagerApp(App):
    index = NumericProperty(-1)
    current_title = StringProperty()
    time = NumericProperty(0)
    show_sourcecode = BooleanProperty(False)
    prev = 'Scanner'
    sourcecode = StringProperty()
    screen_names = ListProperty([])
    hierarchy = ListProperty([])
    user_db = "../user.db"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screens = {}
        self.available_screens = {}

    def build(self):
        self.title = 'Klearnel Manager'
        self.available_screens = ([
            'Creation', 'Login', 'Chooser', 'Scanner', 'Quarantine',
            'Settings', 'AddServ'])
        self.screen_names = ['Scanner', 'Quarantine', 'Settings']
        curdir = "../view/"
        self.available_screens = [join(curdir, 'data', 'screens', '{}.kv'.format(fn)) for fn in self.available_screens]
        self.initial_screen()

    def initial_screen(self):
        if not exists(self.user_db):
            self.get_index('Creation')
        else:
            self.get_index('Login')
        self.load_screen(self.index)

    def get_index(self, page):
        for x in range(0, len(self.available_screens)):
            if self.available_screens[x].find(page) != -1:
                self.index = x

    def load_screen(self, index):
        # REMOVE FOR CONSISTENT REFRESH
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

    def register(self, user, pwd, pwd_verif):
        if pwd != pwd_verif:
            popup = Popup(size_hint=(None, None), size=(300, 150))
            popup.add_widget(Label(text="Passwords do not match"))
            popup.bind(on_press=popup.dismiss)
            popup.title = "Registration Error"
            popup.open()
        elif not re.search(r'[a-z]', user) or (len(user) < 4):
            popup = Popup(size_hint=(None, None), size=(400, 150))
            popup.add_widget(Label(text="Username must not be empty\n"
                                        "and a minimum of 4 characters"))
            popup.bind(on_press=popup.dismiss)
            popup.title = "Registration Error"
            popup.open()
        elif (len(pwd) < 6) or not re.search(r'[a-z]', pwd) or not re.search(r'[0-9]', pwd):
            popup = Popup(size_hint=(None, None), size=(400, 150))
            popup.add_widget(Label(text="Password must not be empty and a\n"
                                        "minimum of 6 characters and numbers"))
            popup.bind(on_press=popup.dismiss)
            popup.title = "Registration Error"
            popup.open()
        else:
            f = open(self.user_db, mode='w')
            f.write(str(Crypter.encrypt(user)))
            f.write(':sep:')
            f.write(str(Crypter.encrypt(pwd)))
            f.close()
            self.get_index('Login')
            self.load_screen(self.index)

    def login(self, user, pwd):
        # f = open(self.user_db, mode='r')
        # file_c = f.read()
        # f.close()
        # user = Crypter.encrypt(user)
        # pwd = Crypter.encrypt(pwd)
        # tab_user = file_c.split(':sep:')
        # user_f = tab_user[0]
        # pwd_f = tab_user[1]
        # if (str(user_f) != str(user)) or (str(pwd_f) != str(pwd)):
        #         popup = Popup(size_hint=(None, None), size=(300, 150))
        #         popup.add_widget(Label(text="Wrong username or password"))
        #         popup.bind(on_press=popup.dismiss)
        #         popup.title = "Bad Credentials"
        #         popup.open()
        # else:
            if not Active.cl.c_list:
                self.get_index('AddServ')
            else:
                self.get_index('Chooser')
            self.load_screen(self.index)

    def connect(self, host):
        # net = Networker()
        # for x in range(0, len(Active.cl.c_list)):
        #     try:
        #         if Active.cl.c_list[x].name == host:
        #             net.connect_to(host)
        #             net.send_val(Active.cl.c_list[x].token)
        #         if net.get_ack() != net.SOCK_ACK:
        #             print("Error on token negociation")
        #             exit("End of program")
        #         net.send_val(Active.cl.c_list[x].password)
        #         if net.get_ack() != net.SOCK_ACK:
        #             print("Error on root password negociation")
        #         net.s.close()
        #         break
        #     except NoConnectivity:
        #         popup = Popup(size_hint=(None, None), size=(300, 150))
        #         popup.add_widget(Label(text="Unable to connect to host " + host))
        #         popup.bind(on_press=popup.dismiss)
        #         popup.title = "No connectivity"
        #         popup.open()
        #         return
        self.get_index('Scanner')
        self.load_screen(self.index)

    def addsrv(self, server, pw, token):
        if len(server) < 1:
            popup = Popup(size_hint=(None, None), size=(300, 150))
            popup.add_widget(Label(text="Client name must not be empty"))
            popup.bind(on_press=popup.dismiss)
            popup.title = "Client Name Error"
            popup.open()
        elif len(pw) < 4:
            popup = Popup(size_hint=(None, None), size=(400, 150))
            popup.add_widget(Label(text="Password must not be empty"))
            popup.bind(on_press=popup.dismiss)
            popup.title = "Password Error"
            popup.open()
        elif 'KL' not in token or not re.search(r'[0-9]', token):
            popup = Popup(size_hint=(None, None), size=(400, 150))
            popup.add_widget(Label(text="Invalid token format"))
            popup.bind(on_press=popup.dismiss)
            popup.title = "Token Error"
            popup.open()
        else:
            Active.cl.add_client(Client(token, server, pw))
            self.get_index('Chooser')
            self.load_screen(self.index)

    def on_pause(self):
        return True

    def on_resume(self):
        pass

    def go_screen(self, idx):
        if self.prev != idx:
            self.prev = idx
            self.get_index(idx)
            self.load_screen(self.index)

    def quit(self):
        sys.exit(0)

if __name__ == '__main__':
    ManagerApp().run()