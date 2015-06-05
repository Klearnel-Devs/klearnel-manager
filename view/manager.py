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
import re

class ManagerScreen(Screen):
    fullscreen = BooleanProperty(False)

    def add_widget(self, *args):
        if 'content' in self.ids:
            return self.ids.content.add_widget(*args)
        return super(ManagerScreen, self).add_widget(*args)

class ListItems(ListItemButton):
    pass

class ScannerViewModal(BoxLayout):
    data = ListProperty()

    def __init__(self, **kwargs):
        self.scdata = list()
        self.orientation = 'vertical'
        for x in range(0, len(Active.scanList)):
            self.scdata.append({'path': Active.scanList[x].path,
                                'options': Active.scanList[x].options})
        self.list_adapter = ListAdapter(data=self.scdata,
                                        args_converter=self.formatter,
                                        cls=QrCompositeListItem,
                                        selection_mode='single',
                                        allow_empty_selection=False)

        super(ScannerViewModal, self).__init__(**kwargs)
        self.add_widget(ListView(adapter=self.list_adapter))

    def formatter(self, row_index, scdata):
        return {'text': scdata['path'],
                'size_hint_y': None,
                'height': 50,
                'cls_dicts': [{'cls': ListItemButton,
                               'kwargs': {'text': "Path: " + scdata['path'],
                                          'size_hint_x': 10.0}},
                              {'cls': CheckBox,
                               'kwargs': {'active': bool(scdata['options']['DUP_S'])}},
                              {'cls': CheckBox,
                               'kwargs': {'active': bool(scdata['options']['DUP_S'])}},
                              {'cls': CheckBox,
                               'kwargs': {'active': bool(scdata['options']['BACKUP'])}},
                              {'cls': CheckBox,
                               'kwargs': {'active': bool(scdata['options']['DEL_F_SIZE'])}},
                              {'cls': CheckBox,
                               'kwargs': {'active': bool(scdata['options']['DUP_F'])}},
                              {'cls': CheckBox,
                               'kwargs': {'active': bool(scdata['options']['FUSE'])}},
                              {'cls': CheckBox,
                               'kwargs': {'active': bool(scdata['options']['INTEGRITY'])}},
                              {'cls': CheckBox,
                               'kwargs': {'active': bool(scdata['options']['CL_TEMP'])}},
                              {'cls': CheckBox,
                               'kwargs': {'active': bool(scdata['options']['DEL_F_OLD'])}},
                              {'cls': CheckBox,
                               'kwargs': {'active': bool(scdata['options']['BACKUP_OLD'])}}]}

class QrDetailView(GridLayout):
    qr_name = StringProperty('', allownone=True)
    obj = None

    def __init__(self, **kwargs):
        kwargs['cols'] = 2
        self.qr_name = kwargs.get('qr_name', '')
        self.obj = kwargs.get('obj', '')
        print(self.obj)
        super(QrDetailView, self).__init__(**kwargs)
        if self.qr_name:
            self.redraw()

    def redraw(self, *args):
        self.clear_widgets()
        if self.qr_name:
            for x in range(0, len(Active.qrList)):
                if Active.qrList[x].f_name == self.qr_name:
                    self.add_widget(Label(text="Filename  :", halign='right'))
                    self.add_widget(Label(text=self.qr_name))
                    self.add_widget(Label(text="Old Path  :", halign='right'))
                    self.add_widget(Label(text=Active.qrList[x].o_path))
                    self.add_widget(Label(text="Entry Date:", halign='right'))
                    self.add_widget(Label(text=format(Active.qrList[x].get_begin())))
                    self.add_widget(Label(text="Expiration:", halign='right'))
                    self.add_widget(Label(text=format(Active.qrList[x].get_expire())))

    def qr_changed(self, list_adapter, *args):
        if len(list_adapter.selection) == 0:
            self.qr_name = None
        else:
            selected_object = list_adapter.selection[0]

            if type(selected_object) is str:
                self.qr_name = selected_object
            else:
                self.qr_name = selected_object.text

        self.redraw()

class QrCompositeListItem(CompositeListItem):
    text = ''

class QuarantineViewModal(BoxLayout):
    data = ListProperty()

    def __init__(self, **kwargs):
        self.qrdata = list()
        for x in range(0, len(Active.qrList)):
            self.qrdata.append({'filename': Active.qrList[x].f_name,
                                'old_path': Active.qrList[x].o_path})

        list_item_args_converter = \
                lambda row_index, selectable: {'text': selectable.name,
                                               'size_hint_y': None,
                                               'height': 25}

        self.dict_adapter = ListAdapter(data=self.qrdata,
                                        args_converter=self.formatter,
                                        selection_mode='single',
                                        allow_empty_selection=False,
                                        cls=QrCompositeListItem)

        super(QuarantineViewModal, self).__init__(**kwargs)
        self.add_widget(ListView(adapter=self.dict_adapter))

        detail_view = QrDetailView(
            qr_name=self.dict_adapter.selection[0].text,
            size_hint=(.6, 1.0))

        self.dict_adapter.bind(
            on_selection_change=detail_view.qr_changed)
        self.add_widget(detail_view)

    def formatter(self, row_index, qr_data):
        return {'text': qr_data['filename'],
                'size_hint_y': None,
                'height': 50,
                'cls_dicts': [{'cls': ListItemLabel,
                               'kwargs': {'text': "Filename:"}},
                              {'cls': ListItemButton,
                               'kwargs': {'text': qr_data['filename']}},
                              {'cls': ListItemLabel,
                               'kwargs': {'text': "Old Path:"}},
                              {'cls': ListItemLabel,
                               'kwargs': {'text': qr_data['old_path']}}]}



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
        #             net.send_val(Active.cl.c_list[x].token)
        #             if net.get_ack() != net.SOCK_ACK:
        #                 print("Error on token negotiation")
        #                 exit("End of program")
        #             net.send_val(Active.cl.c_list[x].password)
        #             if net.get_ack() != net.SOCK_ACK:
        #                 print("Error on root password negotiation")
        #             net.s.close()
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

if __name__ == '__main__':
    ManagerApp().run()