__author__ = 'Derek'
from kivy.uix.label import Label
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListItemButton, ListView, CompositeListItem, ListItemLabel
from kivy.uix.boxlayout import BoxLayout
from controller import Active
from model.ScanElem import *
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button, ButtonBehavior
from kivy.uix.togglebutton import ToggleButton
from model.Exceptions import ScanException
from kivy.uix.popup import Popup
from kivy.clock import Clock

update = 0

class ScCompositeListItem(CompositeListItem):
    text = ''

class ScButton(ListItemButton):
    def on_press(self):
        return False

class ScLabel(ListItemLabel):
    pass

class AddScannerElementButton(Button):
    pass

class ScToggleButton(ToggleButton):
    value = StringProperty('', allownone=True)

    def __init__(self, **kwargs):
        self.value = kwargs.get('value', '')
        super(ScToggleButton, self).__init__(**kwargs)

class ScDetailView(BoxLayout):
    sc_name = StringProperty('', allownone=True)
    obj = None

    def __init__(self, **kwargs):
        self.sc_name = kwargs.get('sc_name', '')
        super(ScDetailView, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_x = 1.0
        if self.sc_name:
            self.redraw()

    def redraw(self, *args):
        self.clear_widgets()
        if self.sc_name:
            for x in range(0, len(Active.scanList)):
                if Active.scanList[x].path == self.sc_name:
                    box1 = BoxLayout(orientation='horizontal')
                    box2 = BoxLayout(orientation='horizontal')
                    box3 = BoxLayout(orientation='horizontal')
                    box4 = BoxLayout(orientation='horizontal')
                    box5 = BoxLayout(orientation='horizontal')
                    box6 = BoxLayout(orientation='horizontal')
                    box1.add_widget(Label(text="Path:", halign='right'))
                    box1.add_widget(Label(id='path', text=self.sc_name))
                    box2.add_widget(Label(text="Broken Symlinks:", halign='right'))
                    box2.add_widget(ScToggleButton(value=self.sc_name, id='BR_S', text="Delete", halign='right',
                                          state='down' if bool(Active.scanList[x].options['BR_S']) else 'normal'))
                    box2.add_widget(Label(text="Duplicate Symlinks:", halign='right'))
                    box2.add_widget(ScToggleButton(value=self.sc_name, id='DUP_S', text="Delete", halign='right',
                                           state='down' if bool(Active.scanList[x].options['DUP_S']) else 'normal'))
                    box3.add_widget(Label(text="Duplicate Files:", halign='right'))
                    box3.add_widget(ScToggleButton(value=self.sc_name, id='DUP_F', text="Delete", halign='right',
                                           state='down' if bool(Active.scanList[x].options['DUP_F']) else 'normal'))
                    box3.add_widget(Label(text="Permissions Integrity:", halign='right'))
                    box3.add_widget(ScToggleButton(value=self.sc_name, id='INTEGRITY', text="Fix", halign='right',
                                           state='down' if bool(Active.scanList[x].options['INTEGRITY']) else 'normal'))

                    box4.add_widget(Label(text="Is Temporary Folder:", halign='right'))
                    btntmp = ScToggleButton(value=self.sc_name, id='is_temp', text="Clean", halign='right',
                                            state='down' if bool(Active.scanList[x].is_temp) else 'normal')
                    box4.add_widget(btntmp)
                    tmpSize = Active.scanList[x].back_limit_size if bool(Active.scanList[x].options['BACKUP']) \
                                                                 else Active.scanList[x].del_limit_size
                    box5.add_widget(Label(text="Files Larger Than {0:g}".format(float(tmpSize)) + "MB:", halign='right'))
                    box5.add_widget(ScToggleButton(value=self.sc_name, id='BACKUP', text="Backup", halign='right', group="sizeFiles",
                                                   state='down' if bool(Active.scanList[x].options['BACKUP'])
                                                   else 'normal',
                                                   disabled=True if float(Active.scanList[x].back_limit_size) < 1
                                                   else False))
                    box5.add_widget(ScToggleButton(value=self.sc_name, id='DEL_F_SIZE', text="Delete", halign='right', group="sizeFiles",
                                                   state='down' if bool(Active.scanList[x].options['DEL_F_SIZE'])
                                                   else 'normal',
                                                   disabled=True if float(Active.scanList[x].del_limit_size) < 1
                                                   else False))
                    tmpAge = Active.scanList[x].max_age
                    box6.add_widget(Label(text="Files Older than " + (str(tmpAge) if int(tmpAge) > 0 else 'N/A') + " days:",
                                          halign='right'))
                    box6.add_widget(ScToggleButton(value=self.sc_name, id='BACKUP_OLD', text="Backup", halign='right', group="oldFiles",
                                                 state='down' if bool(Active.scanList[x].options['BACKUP_OLD'])
                                                 else 'normal', disabled=True if float(tmpAge) < 1 else False))
                    box6.add_widget(ScToggleButton(value=self.sc_name, id='DEL_F_OLD', text="Delete", halign='right', group="oldFiles",
                                                 state='down' if bool(Active.scanList[x].options['DEL_F_OLD'])
                                                 else 'normal', disabled=True if float(tmpAge) < 1 else False))
                    self.add_widget(box1)
                    self.add_widget(box2)
                    self.add_widget(box3)
                    self.add_widget(box4)
                    self.add_widget(box5)
                    self.add_widget(box6)
                    self.add_widget(Button(text="Remove From Scanner",
                                           on_press=lambda a: self.deleteItem(Active.scanList[x], x)))
                    print(Active.scanList[x].get_options())
                    break

    def callback(self):
        Clock.schedule_once(lambda dt: self.redraw(), 0.5)

    def deleteItem(self, item, index):
        try:
            Active.scan_task.rm_from_scan(Active.client, item.path)
        except ScanException as se:
            popup = Popup(size_hint=(None, None), size=(400, 150))
            popup.add_widget(Label(text=se.value))
            popup.bind(on_press=popup.dismiss)
            popup.title = se.title
            popup.open()
            return
        Active.scanList.pop(index)
        global update
        update = 1

    def sc_changed(self, list_adapter, *args):
        if len(list_adapter.selection) == 0:
            self.sc_name = None
        else:
            selected_object = list_adapter.selection[0]

            if type(selected_object) is str:
                self.sc_name = selected_object
            else:
                self.sc_name = selected_object.text
        self.redraw()

class ScannerViewModal(BoxLayout):
    data = ListProperty()

    def __init__(self, **kwargs):
        self.scdata = list()
        self.orientation = 'vertical'
        # FOR NETWORK
        Active.scanList.clear()
        try:
            Active.scanList = Active.scan_task.get_scan_list(Active.client)
        except ScanException as se:
            popup = Popup(size_hint=(None, None), size=(400, 150))
            popup.add_widget(Label(text=se.value))
            popup.bind(on_press=popup.dismiss)
            popup.title = se.title
            popup.open()
            return
        for x in range(0, len(Active.scanList)):
            self.scdata.append({'path': Active.scanList[x].path,
                                'options': Active.scanList[x].options})

        self.list_adapter = ListAdapter(data=self.scdata,
                                        args_converter=self.formatter,
                                        cls=ScCompositeListItem,
                                        selection_mode='single',
                                        allow_empty_selection=False)

        super(ScannerViewModal, self).__init__(**kwargs)
        self.list_view = ListView(adapter=self.list_adapter)
        self.add_widget(self.list_view)

        detail_view = ScDetailView(sc_name=self.list_adapter.selection[0].text, size_hint=(.6, 1.0))

        self.list_adapter.bind(
            on_selection_change=detail_view.sc_changed)
        self.add_widget(detail_view)
        Clock.schedule_interval(self.callback, 60)
        Clock.schedule_interval(self.callback2, 5)

    def callback(self, dt):
        self.update_list()

    def callback2(self, dt):
        global update
        if update != 0:
            print("Updating")
            update = 0
            Clock.schedule_once(lambda dt: self.update_list(), 0.1)
        if Active.changed['sc'] != 0:
            print("Adding")
            Active.changed['sc'] = 0
            Clock.schedule_once(lambda dt: self.update_list(), 0.1)

    def update_list(self):
        print('Called')
        try:
            Active.scanList = Active.scan_task.get_scan_list(Active.client)
        except ScanException as se:
            popup = Popup(size_hint=(None, None), size=(400, 150))
            popup.add_widget(Label(text=se.value))
            popup.bind(on_press=popup.dismiss)
            popup.title = se.title
            popup.open()
            return
        self.scdata.clear()
        for x in range(0, len(Active.scanList)):
            self.scdata.append({'path': Active.scanList[x].path,
                              'options': Active.scanList[x].options})
        self.list_adapter.data = self.scdata
        if hasattr(self.list_view, '_reset_spopulate'):
            self.list_view._reset_spopulate()

    def formatter(self, rowindex, scdata):
        return {'text': scdata['path'],
                'size_hint_y': None,
                'height': 50,
                'cls_dicts': [{'cls': ListItemButton,
                               'kwargs': {'text': scdata['path'],
                                          'size_hint_x': 0.5}},
                              {'cls': ScButton,
                               'kwargs': {'text' : 'BR_S',
                                          'state': 'down' if bool(scdata['options']['BR_S']) else 'normal'}},
                              {'cls': ScButton,
                               'kwargs': {'text' : 'DUP_S',
                                          'state': 'down' if bool(scdata['options']['DUP_S']) else 'normal'}},
                              {'cls': ScButton,
                               'kwargs': {'text' : 'BACKUP',
                                          'state': 'down' if bool(scdata['options']['BACKUP']) else 'normal'}},
                              {'cls': ScButton,
                               'kwargs': {'text' : 'DEL_F_SIZE',
                                          'state': 'down' if bool(scdata['options']['DEL_F_SIZE']) else 'normal'}},
                              {'cls': ScButton,
                               'kwargs': {'text' : 'DUP_F',
                                          'state': 'down' if bool(scdata['options']['DUP_F']) else 'normal'}},
                              {'cls': ScButton,
                               'kwargs': {'text' : 'INTEGRITY',
                                          'state': 'down' if bool(scdata['options']['INTEGRITY']) else 'normal'}},
                              {'cls': ScButton,
                               'kwargs': {'text' : 'CL_TEMP',
                                          'state': 'down' if bool(scdata['options']['CL_TEMP']) else 'normal'}},
                              {'cls': ScButton,
                               'kwargs': {'text' : 'DEL_F_OLD',
                                          'state': 'down' if bool(scdata['options']['DEL_F_OLD']) else 'normal'}},
                              {'cls': ScButton,
                               'kwargs': {'text' : 'BACKUP_OLD',
                                          'state': 'down' if bool(scdata['options']['BACKUP_OLD']) else 'normal'}}]}

