## @package view
#   Defines classes to be displayed by the GUI
#
# @author Antoine Ceyssens <a.ceyssens@nukama.be> & Derek Van Hove <d.vanhove@nukama.be>
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
from model.Client import Client, ClientList
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

## Variable used to determine whether to schedule refresh event
update = 0

## Inherits from Screen and define add_widget
class ManagerScreen(Screen):
    ## Self explanatory
    fullscreen = BooleanProperty(False)

    ## Adds a widget
    def add_widget(self, *args):
        if 'content' in self.ids:
            return self.ids.content.add_widget(*args)
        return super(ManagerScreen, self).add_widget(*args)

## See Kivy Files
class StTextInput(TextInput):
    pass

class ConnectButton(Button):
    pass

class ClCompositeListItem(CompositeListItem):
    text = ''

## The view of an individual quarantine item
class ClientDetailView(GridLayout):
    ## Quarantine items name
    cl_name = StringProperty('', allownone=True)
    obj = None

    ## Constructor
    def __init__(self, **kwargs):
        kwargs['cols'] = 1
        self.cl_name = kwargs.get('cl_name', '')
        super(ClientDetailView, self).__init__(**kwargs)
        self.size_hint_x = 1.0
        if self.cl_name:
            self.redraw()

    ## Redraws the detail view
    def redraw(self, *args):
        self.clear_widgets()
        if self.cl_name:
            for x in range(0, len(Active.cl.c_list)):
                if Active.cl.c_list[x].name == self.cl_name:
                    box1 = BoxLayout(orientation='horizontal', size_hint_y=None, height= 40)
                    box2 = BoxLayout(orientation='horizontal', size_hint_y=None, height= 40)
                    box3 = BoxLayout(orientation='horizontal', size_hint_y=None, height= 40)
                    box4 = BoxLayout(orientation='horizontal', size_hint_y=None, height= 40)
                    box5 = BoxLayout(orientation='horizontal', size_hint_y=None, height= 40)
                    box1.add_widget(Label(text="Hostname  :", halign='right'))
                    input1 = StTextInput(text=self.cl_name)
                    box1.add_widget(input1)
                    box2.add_widget(Label(text="IP Address  :", halign='right'))
                    input2 = StTextInput(text=Active.cl.c_list[x].ip)
                    box2.add_widget(input2)
                    box3.add_widget(Label(text="Klearnel Password:", halign='right'))
                    input3 = StTextInput(text='', password=True)
                    box3.add_widget(input3)
                    box4.add_widget(Label(text="Token:", halign='right'))
                    input4 = StTextInput(text='', password=True)
                    box4.add_widget(input4)
                    box5.add_widget(ConnectButton(text="Connect", id=str(x)))
                    box5.add_widget(Button(text="Modify",
                                           on_press=lambda a: self.modify_item(input1.text, input2.text, input3.text,
                                                                               input4.text, x)))
                    box5.add_widget(Button(text="Remove",
                                           on_press=lambda a: self.delete_item(x)))
                    self.add_widget(box1)
                    self.add_widget(box2)
                    self.add_widget(box3)
                    self.add_widget(box4)
                    self.add_widget(box5)
                    break

    ## Determines whether to redraw if selection has changed
    # @param list_adapter
    # @param args
    def cl_changed(self, list_adapter, *args):
        if len(list_adapter.selection) == 0:
            self.cl_name = None
        else:
            selected_object = list_adapter.selection[0]

            if type(selected_object) is str:
                self.cl_name = selected_object
            else:
                self.cl_name = selected_object.text
        self.redraw()

    ## Triggered when modifying a client
    # @param item The item to restore
    # @param index The items index in the local list
    def modify_item(self, name, ip, pw, token, index):
        if Active.cl.c_list[index].name is not name:
            Active.cl.c_list[index].name = name
        if Active.cl.c_list[index].ip is not ip:
            Active.cl.c_list[index].ip = ip
        if len(pw) < 2:
            pass
        elif len(pw) < 4:
            popup = Popup(size_hint=(None, None), size=(400, 150))
            popup.add_widget(Label(text="Password must be at least 4 characters long"))
            popup.bind(on_press=popup.dismiss)
            popup.title = "Password Error"
            popup.open()
            return
        else:
            Active.cl.c_list[index].set_password(pw)
        if len(token) < 4:
            pass
        elif 'KL' not in token or not re.search(r'[0-9]', token):
            popup = Popup(size_hint=(None, None), size=(400, 150))
            popup.add_widget(Label(text="Invalid token format"))
            popup.bind(on_press=popup.dismiss)
            popup.title = "Token Error"
            popup.open()
            return
        else:
            Active.cl.c_list[index].token = token
        Active.cl.save_list(Active.cl)
        global update
        update = 1

    ## Triggered when removing a client
    # @param item The item to remove
    # @param index The items index in the local list
    # @exception QrException
    def delete_item(self, index):
        Active.cl.c_list.pop(index)
        Active.cl.save_list(Active.cl)
        global update
        update = 1

class ListViewModal(BoxLayout):
    ## The data containing clients
    data = ListProperty()

    ## Constructor
    def __init__(self, **kwargs):
        self.data = list()
        for x in range(0, len(Active.cl.c_list)):
            self.data.append({
                'hostname': Active.cl.c_list[x].name,
                'ip': Active.cl.c_list[x].ip
            })
        self.list_adapter = ListAdapter(data=self.data,
                                        args_converter=self.formatter,
                                        cls=ClCompositeListItem,
                                        selection_mode='single',
                                        allow_empty_selection=False)
        super(ListViewModal, self).__init__(**kwargs)
        self.list_view = ListView(adapter=self.list_adapter)
        self.add_widget(self.list_view)
        if len(self.data) is 0:
            detail_view = ClientDetailView(cl_name="List is empty", size_hint=(.6, 1.0))
        else:
            detail_view = ClientDetailView(cl_name=self.list_adapter.selection[0].text,
                                       size_hint=(.6, 1.0))

        self.list_adapter.bind(
            on_selection_change=detail_view.cl_changed)
        self.add_widget(detail_view)
        Clock.schedule_interval(self.callback, 5)

    ## Callback on clock schedule to update list
    def callback(self, dt):
        global update
        if update != 0:
            update = 0
            Clock.schedule_once(lambda dt: self.update_list(), 0.1)
        if Active.changed['cl'] != 0:
            Active.changed['cl'] = 0
            Clock.schedule_once(lambda dt: self.update_list(), 0.1)

    ## The args converter
    def formatter(self, rowindex, data):
        return {'text': data['hostname'],
                'size_hint_y': None,
                'height': 40,
                'cls_dicts': [{'cls': ListItemButton,
                               'kwargs': {'text': data['hostname']}},
                              {'cls': ListItemLabel,
                               'kwargs': {'text': data['ip']}}]}

    ## Updates the Client list
    # @exception QrException
    # @exception EmptyListException
    def update_list(self):
        self.data.clear()
        for x in range(0, len(Active.cl.c_list)):
            self.data.append({
                'hostname': Active.cl.c_list[x].name,
                'ip': Active.cl.c_list[x].ip
            })
        self.list_adapter.data = self.data
        if hasattr(self.list_view, '_reset_spopulate'):
            self.list_view._reset_spopulate()


## The root application
class ManagerApp(App):
    ## Self explanatory
    index = NumericProperty(-1)
    ## Current screens title
    current_title = StringProperty()
    ## Self explanatory
    time = NumericProperty(0)
    ## Self explanatory
    prev = 'Scanner'
    ## List of screen names
    screen_names = ListProperty()
    ## User database path
    user_db = "../user.db"

    ## Constructor
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screens = {}
        self.available_screens = {}
        Active.cl = ClientList
        Active.confList = Config()
        Active.qrList = list()
        Active.scanList = list()
        Active.scan_task = TaskScan()
        Active.qr_task = TaskQR()
        Active.conf_task = TaskConfig()

    ## Builder
    def build(self):
        self.title = 'Klearnel Manager'
        self.available_screens = ([
            'Creation', 'Login', 'Chooser', 'Scanner', 'Quarantine',
            'Settings', 'AddServ', 'addscan', 'addquar'])
        self.screen_names = ['Scanner', 'Quarantine', 'Settings']
        curdir1 = "../view/"
        self.available_screens = [join(curdir1, 'data', 'screens', '{}.kv'.format(fn)) for fn in self.available_screens]
        self.initial_screen()

    ## Determines initial screen depending on existence of user database file
    def initial_screen(self):
        if not exists(self.user_db):
            self.get_index('Creation')
        else:
            self.get_index('Login')
        self.load_screen(self.index)

    ## GETTER
    # @param page The page name to find
    def get_index(self, page):
        for x in range(0, len(self.available_screens)):
            if self.available_screens[x].find(page) != -1:
                self.index = x

    ## Loads a previously unloaded screen or returns an already loaded screen
    # @param index The page index
    # @return The page
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

    ## Used for user registration -> input validations, screen control
    # @param user The username to validate
    # @param pwd The password to validate
    # @param pwd_verif The password to validate and crosscheck with pwd
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

    ## For user login
    # @param user The inputted user name to validate
    # @param pwd The inputted password to validate
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

    ## Connects to a Klearnel host
    # @param idx The index in the client list of the host
    # @throws BadCredentials
    # @exception BadCredentials
    # @exception ConnectionError
    # @exception NoConnectivity
    # @exception ConfigException
    def connect(self, idx):
        netw = Networker()
        try:
            netw.connect_to(Active.cl.c_list[idx])
            netw.send_val(Active.cl.c_list[idx].token)
            if netw.get_ack() != netw.SOCK_ACK:
                raise BadCredentials("Connection rejected by " + Active.cl.c_list[idx].name)
            netw.send_val(Active.cl.c_list[idx].password)
            if netw.get_ack() != netw.SOCK_ACK:
                raise BadCredentials("Connection rejected by " + Active.cl.c_list[idx].name)
            netw.send_val(str(NET_CONNEC) + ":0")
            netw.s.close()
            Active.client = Active.cl.c_list[idx]
            Active.conf_task.get_config(Active.client)
        except BadCredentials as bc:
            popup = Popup(size_hint=(None, None), size=(300, 150))
            popup.add_widget(Label(text=bc.value))
            popup.bind(on_press=popup.dismiss)
            popup.title = "Wrong Credentials"
            popup.open()
            return
        except ConnectionError:
            popup = Popup(size_hint=(None, None), size=(300, 150))
            popup.add_widget(Label(text="Unable to connect to host " + Active.cl.c_list[idx].name))
            popup.bind(on_press=popup.dismiss)
            popup.title = "Connection Error"
            popup.open()
            return
        except NoConnectivity:
            popup = Popup(size_hint=(None, None), size=(300, 150))
            popup.add_widget(Label(text="Unable to connect to host " + Active.cl.c_list[idx].name))
            popup.bind(on_press=popup.dismiss)
            popup.title = "No connectivity"
            popup.open()
            return
        except ConfigException as ce:
            popup = Popup(size_hint=(None, None), size=(400, 150))
            popup.add_widget(Label(text=ce.value))
            popup.bind(on_press=popup.dismiss)
            popup.title = ce.title
            popup.open()
            return
        self.get_index('Scanner')
        self.load_screen(self.index)

    ## Validates and adds a client to client database
    # @param server The client name or IP
    # @param pw The Klearnel password
    # @param token The Klearnel token
    def addsrv(self, server, ip, pw, token):
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
            Active.cl.add_client(Active.cl, Client(token, ip, server, pw))
            self.get_index('Chooser')
            self.load_screen(self.index)
            global update
            update = 1

    ## Sets indexing for screen navigation
    # @param idx The index
    def go_screen(self, idx):
        if self.prev != idx:
            self.prev = idx
            self.get_index(idx)
            self.load_screen(self.index)

    ## Self explanatory
    def quit(self):
        sys.exit(0)

    ## Returns to Login screen
    def logout(self):
        self.get_index("Login")
        self.load_screen(self.index)

    ## Gets a configuration value
    # @param section The concerning section
    # @param key The concerning key
    def getConf(self, section, key):
        return Active.confList.get_value(section, key)

    ## Validates configuration changes
    # @param kwargs A variable argument list containing each configuration screen button
    # @exception ConfigException
    def setConf(self, *kwargs):
        modified = False
        for arg in kwargs:
            if arg.__class__ is CfgCheckBox:
                if arg.active is not bool(Active.confList.get_value(arg.value1, arg.value2)):
                    tmp = Active.confList
                    Active.confList.set_config(arg.value1, arg.value2, int(arg.active))
                    try:
                        Active.conf_task.send_conf_mod(Active.client, arg.value1, arg.value2, str(int(arg.active)))
                    except ConfigException as ce:
                        Active.confList = tmp
                        popup = Popup(size_hint=(None, None), size=(400, 150))
                        popup.add_widget(Label(text=ce.value))
                        popup.bind(on_press=popup.dismiss)
                        popup.title = ce.title
                        popup.open()
                        return
                    modified = True
            else:
                if str(arg.text) != Active.confList.get_value(arg.value1, arg.value2):
                    tmp = Active.confList
                    Active.confList.set_config(arg.value1, arg.value2, arg.text)
                    try:
                        Active.conf_task.send_conf_mod(Active.client, arg.value1, arg.value2,
                                                       Active.confList.get_value_res(arg.value1, arg.value2))
                    except ConfigException as ce:
                        Active.confList = tmp
                        popup = Popup(size_hint=(None, None), size=(400, 150))
                        popup.add_widget(Label(text=ce.value))
                        popup.bind(on_press=popup.dismiss)
                        popup.title = ce.title
                        popup.open()
                        return
                    modified = True
        if modified:
            popup = Popup(title='Configuration Saved', size_hint=(None, None), size=(400, 150))
            popup.add_widget(Label(text="Configuration settings have been saved"))
            popup.bind(on_press=popup.dismiss)
            popup.open()

    ## Validates scanner additions
    # @param path The item path
    # @param is_temp Whether its a temporary folder or not
    # @param size The max file size for backup/delete
    # @param age The max age for backup/delete
    # @param args The options selected
    # @throws EmptyFields
    # @exception EmptyFields
    # @exception ScanException
    def addscan(self, path, is_temp, size, age, *args):
        try:
            if not path or not re.search(r'^[\'"]?(?:/[^/]+)*[\'"]?$', path):
                raise EmptyFields("Text fields empty or incorrect format")
            if not age or not re.search(r'^[0-9]+$', age):
                if age != "Age in days":
                    raise EmptyFields("Text fields empty or incorrect format")
            if not size or not re.search(r'^[0-9]+$', size):
                if size != "Size in MB":
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
        if size == "Size in MB":
            tmp.back_limit_size = -1
            tmp.del_limit_size = -1
        else:
            tmp.back_limit_size = int(size)
            tmp.del_limit_size = int(size)
        if age == "Age in days":
            tmp.max_age = -1
        else:
            tmp.max_age = age
        try:
            Active.scan_task.add_to_scan(Active.client, tmp)
        except ScanException as se:
            popup = Popup(size_hint=(None, None), size=(400, 150))
            popup.add_widget(Label(text=se.value))
            popup.bind(on_press=popup.dismiss)
            popup.title = se.title
            popup.open()
            return
        Active.changed['sc'] = 1
        self.get_index("Scanner")
        self.load_screen(self.index)

    ## Validates additions to Klearnel's QR
    # @param filename The file to add
    # @throws EmptyFields
    # @exception EmptyFields
    # @exception QrException
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
        try:
            Active.qr_task.add_to_qr(Active.client, filename)
        except QrException as qr:
            popup = Popup(size_hint=(None, None), size=(400, 150))
            popup.add_widget(Label(text=qr.value))
            popup.bind(on_press=popup.dismiss)
            popup.title = qr.title
            popup.open()
            return
        Active.changed['qr'] = 1
        self.get_index("Quarantine")
        self.load_screen(self.index)

    ## Validates and modifies scanner item options
    # @param btn The selected button
    # @param path The item path
    # @param ids ID of button
    # @param state The button state
    # @exception ScanException
    def mod_sc(self, btn, path, ids, state):
        for x in range(0, len(Active.scanList)):
            if path is Active.scanList[x].path:
                tmp = Active.scanList[x]
                break
        if ids is 'is_temp':
            Active.scanList[x].is_temp = 1 if state is 'down' else 0
            Active.scanList[x].options['CL_TEMP'] = 1 if state is 'down' else '0'
        else:
            Active.scanList[x].options[ids] = '1' if state is 'down' else '0'
            if ids is 'BACKUP' and state is 'down':
                Active.scanList[x].options['DEL_F_SIZE'] = '0'
            elif ids is 'DEL_F_SIZE' and state is 'down':
                Active.scanList[x].options['BACKUP'] = '0'
            elif ids is 'BACKUP_OLD' and state is 'down':
                Active.scanList[x].options['DEL_F_OLD'] = '0'
            elif ids is 'DEL_F_OLD' and state is 'down':
                Active.scanList[x].options['BACKUP_OLD'] = '0'
        try:
            Active.scan_task.mod_from_scan(Active.client, path, Active.scanList[x].get_options(),
                                           Active.scanList[x].is_temp)
        except ScanException as se:
            popup = Popup(size_hint=(None, None), size=(500, 150))
            popup.add_widget(Label(text=se.value))
            popup.bind(on_press=popup.dismiss)
            popup.title = se.title
            popup.open()
            btn.state = 'normal' if state is 'down' else 'down'
            Active.scanList[x] = tmp
            return
