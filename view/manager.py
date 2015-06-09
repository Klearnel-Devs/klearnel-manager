__author__ = 'Derek'
"""
    Klearnel Manager GUI
"""
from kivy.app import App
from os.path import *
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
import sys
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListItemButton, ListView, CompositeListItem, ListItemLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from controller.Networker import *
from controller.Tasker import *
from model.Client import Client
from controller import Active
from model.Config import Config
from model.QrElem import *
from model.ScanElem import *
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from view.data.modules.scanner import *
from view.data.modules.config import *

from view.data.modules.quarantine import *
import re

class ManagerScreen(Screen):
    fullscreen = BooleanProperty(False)

    def add_widget(self, *args):
        if 'content' in self.ids:
            return self.ids.content.add_widget(*args)
        return super(ManagerScreen, self).add_widget(*args)

class ListItems(ListItemButton):
    pass


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
        Active.cl = ClientList
        Active.confList = Config
        Active.qrList = [qr_temp_create1(), qr_temp_create2(), qr_temp_create3(), qr_temp_create4(), qr_temp_create5()]
        Active.scanList = [sc_temp_create1(), sc_temp_create2(), sc_temp_create3(), sc_temp_create4(), sc_temp_create5()]
        Active.scan_task = TaskScan()
        Active.qr_task = TaskQR()

    def build(self):
        self.title = 'Klearnel Manager'
        self.available_screens = ([
            'Creation', 'Login', 'Chooser', 'Scanner', 'Quarantine',
            'Settings', 'AddServ', 'addscan', 'addquar'])
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
        f = open(self.user_db, mode='r')
        file_c = f.read()
        f.close()
        user = Crypter.encrypt(user)
        pwd = Crypter.encrypt(pwd)
        tab_user = file_c.split(':sep:')
        user_f = tab_user[0]
        pwd_f = tab_user[1]
        if (str(user_f) != str(user)) or (str(pwd_f) != str(pwd)):
                popup = Popup(size_hint=(None, None), size=(300, 150))
                popup.add_widget(Label(text="Wrong username or password"))
                popup.bind(on_press=popup.dismiss)
                popup.title = "Bad Credentials"
                popup.open()
        else:
            Active.user = user
            Active.cl.load_list(Active.cl)
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
        #             try:
        #                 net.send_val(Active.cl.c_list[x].token)
        #                 if net.get_ack() != net.SOCK_ACK:
        #                     raise BadCredentials("Connection rejected by " + host)
        #                 net.send_val(Active.cl.c_list[x].password)
        #                 if net.get_ack() != net.SOCK_ACK:
        #                     raise BadCredentials("Connection rejected by " + host)
        #                 net.s.close()
        #             except BadCredentials as bc:
        #                 popup = Popup(size_hint=(None, None), size=(300, 150))
        #                 popup.add_widget(Label(text=bc.value))
        #                 popup.bind(on_press=popup.dismiss)
        #                 popup.title = "Wrong Credentials"
        #                 popup.open()
        #                 return
        #             Active.client = Active.cl.c_list[x]
        #             break
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
            Active.cl.add_client(Active.cl, Client(token, server, pw))
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

    def logout(self):
        self.get_index("Login")
        self.load_screen(self.index)

    def getConf(self, section, entry):
        return Active.confList.get_value(Active.confList, section, entry)

    def setConf(self, *kwargs):
        print('!')
        for arg in kwargs:
            if arg.__class__ is CfgCheckBox:
                if arg.active is not bool(Active.confList.get_value(Active.confList, arg.value1, arg.value2)):
                    pass
            else:
                if str(arg.text) != Active.confList.get_value(Active.confList, arg.value1, arg.value2):
                    pass

    def addscan(self, path, is_temp, size, age, *args):
        try:
            if not path or not re.search(r'^[\'"]?(?:/[^/]+)*[\'"]?$', path):
                raise EmptyFields("Text fields empty or incorrect format")
            if not age or not re.search(r'^[0-9]+$', age):
                raise EmptyFields("Text fields empty or incorrect format")
            if not size or not re.search(r'^[0-9]+$', size):
                raise EmptyFields("Text fields empty or incorrect format")
        except EmptyFields as ef:
            popup = Popup(size_hint=(None, None), size=(400, 150))
            popup.add_widget(Label(text=ef.value))
            popup.bind(on_press=popup.dismiss)
            popup.title = "Input Error"
            popup.open()
            return
        tmp = ScanElem(path)
        tmp.is_temp = 0 if is_temp is 'normal' else 1
        opt = ''
        for arg in args:
            opt += '0' if arg is 'normal' else '1'
        tmp.set_options(opt)
        tmp.back_limit_size = float(size) if tmp.options['BACKUP'] is '1' else None
        tmp.del_limit_size = float(size) if tmp.options['DEL_F_SIZE'] is '1' else None
        tmp.max_age = age
        # try:
        #     Active.scan_task.add_to_scan(Active.client, tmp)
        # except ScanException as se:
        #     popup = Popup(size_hint=(None, None), size=(400, 150))
        #     popup.add_widget(Label(text=se.value))
        #     popup.bind(on_press=popup.dismiss)
        #     popup.title = se.title
        #     popup.open()
        #     return
        self.get_index("Scanner")
        self.load_screen(self.index)

    def addQR(self, filename):
        try:
            if not filename or not re.search(r'^[\'"]?(?:/[^/]+)*[\'"]?$', filename):
                raise EmptyFields("Incorrect format for filename")
        except EmptyFields as ef:
            popup = Popup(size_hint=(None, None), size=(400, 150))
            popup.add_widget(Label(text=ef.value))
            popup.bind(on_press=popup.dismiss)
            popup.title = "Input Error"
            popup.open()
            return
        # try:
        #     Active.qr_task.add_to_qr(Active.client, filename)
        # except QrException as qr:
        #     popup = Popup(size_hint=(None, None), size=(400, 150))
        #     popup.add_widget(Label(text=qr.value))
        #     popup.bind(on_press=popup.dismiss)
        #     popup.title = qr.title
        #     popup.open()
        #     return
        self.get_index("Quarantine")
        self.load_screen(self.index)

    def mod_sc(self, btn, path, id, state):
        for x in range(0, len(Active.scanList)):
            if path is Active.scanList[x].path:
                break
        tmp = Active.scanList[x]
        if id is 'is_temp':
            Active.scanList[x].is_temp = 1 if state is 'down' else 0
            Active.scanList[x].options['CL_TEMP'] = 1 if state is 'down' else '0'
        else:
            Active.scanList[x].options[id] = '1' if state is 'down' else '0'
            if id is 'BACKUP' and state is 'down':
                Active.scanList[x].options['DEL_F_SIZE'] = '0'
            elif id is 'DEL_F_SIZE' and state is 'down':
                Active.scanList[x].options['BACKUP'] = '0'
            elif id is 'BACKUP_OLD' and state is 'down':
                Active.scanList[x].options['DEL_F_OLD'] = '0'
            elif id is 'DEL_F_OLD' and state is 'down':
                Active.scanList[x].options['BACKUP_OLD'] = '0'
        try:
            if id is 'is_temp':
                Active.scan_task.mod_from_scan(Active.client, path, Active.scanList[x].is_temp)
            else:
                Active.scan_task.mod_from_scan(Active.client, path, Active.scanList[x].get_options)
        except ScanException as se:
            popup = Popup(size_hint=(None, None), size=(500, 150))
            popup.add_widget(Label(text=se.value))
            popup.bind(on_press=popup.dismiss)
            popup.title = se.title
            popup.open()
            btn.state = 'normal' if state is 'down' else 'down'
            Active.scanList[x] = tmp
        print(Active.scanList[x].get_options())

if __name__ == '__main__':
    ManagerApp().run()