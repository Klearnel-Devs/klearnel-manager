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

class ScCompositeListItem(CompositeListItem):
    text = ''

class ScButton(ListItemButton):
    def on_press(self):
        return False

class ScLabel(ListItemLabel):
    pass

class AddScannerElementButton(Button):
    pass

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
                    box1.add_widget(Label(text=self.sc_name))
                    box2.add_widget(Label(text="Broken Symlinks:", halign='right'))
                    box2.add_widget(ToggleButton(id='BR_S', text="Delete", halign='right',
                                           state='down' if bool(Active.scanList[x].options['BR_S']) else 'normal'))
                    box2.add_widget(Label(text="Duplicate Symlinks:", halign='right'))
                    box2.add_widget(ToggleButton(id='DUP_S', text="Delete", halign='right',
                                           state='down' if bool(Active.scanList[x].options['DUP_S']) else 'normal'))
                    box3.add_widget(Label(text="Duplicate Files:", halign='right'))
                    box3.add_widget(ToggleButton(id='DUP_F', text="Delete", halign='right',
                                           state='down' if bool(Active.scanList[x].options['DUP_F']) else 'normal'))
                    box3.add_widget(Label(text="Permissions Integrity:", halign='right'))
                    box3.add_widget(ToggleButton(id='INTEGRITY', text="Fix", halign='right',
                                           state='down' if bool(Active.scanList[x].options['INTEGRITY']) else 'normal'))
                    box5.add_widget(Label(text="Files Larger Than X Size:", halign='right'))
                    box4.add_widget(Label(text="Is Temporory Folder:", halign='right'))
                    box4.add_widget(ToggleButton(id='is_temp', text="Yes", halign='right',
                                           state='down' if bool(Active.scanList[x].is_temp) else 'normal'))
                    box4.add_widget(Label(text="Temp Folders:", halign='right'))
                    box4.add_widget(ToggleButton(id='CL_TEMP', text="Clean", halign='right',
                                           state='down' if bool(Active.scanList[x].options['CL_TEMP']) else 'normal',
                                         disabled=False if bool(Active.scanList[x].is_temp) else True))
                    box5.add_widget(ToggleButton(id='BACKUP', text="Backup", halign='right', group="sizeFiles",
                                                 state='down' if bool(Active.scanList[x].options['BACKUP'])
                                                 else 'normal'))
                    box5.add_widget(ToggleButton(id='DEL_F_SIZE', text="Delete", halign='right', group="sizeFiles",
                                                 state='down' if bool(Active.scanList[x].options['DEL_F_SIZE'])
                                                 else 'normal'))
                    box6.add_widget(Label(text="Files Older than " + str(Active.scanList[x].max_age) + " days:",
                                          halign='right'))
                    box6.add_widget(ToggleButton(id='BACKUP_OLD', text="Backup", halign='right', group="oldFiles",
                                                 state='down' if bool(Active.scanList[x].options['BACKUP_OLD'])
                                                 else 'normal'))
                    box6.add_widget(ToggleButton(id='DEL_F_OLD', text="Delete", halign='right', group="oldFiles",
                                                 state='down' if bool(Active.scanList[x].options['DEL_F_OLD'])
                                                 else 'normal'))
                    self.add_widget(box1)
                    self.add_widget(box2)
                    self.add_widget(box3)
                    self.add_widget(box4)
                    self.add_widget(box5)
                    self.add_widget(box6)
                    self.add_widget(Button(text="Remove From Scanner",
                                           on_press=lambda a: self.deleteItem(Active.scanList[x])))
                    break

    def deleteItem(self, item):
        print(str(item))
    #     TO IMPLEMENT

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
        for x in range(0, len(Active.scanList)):
            self.scdata.append({'path': Active.scanList[x].path,
                                'options': Active.scanList[x].options})

        self.list_adapter = ListAdapter(data=self.scdata,
                                        args_converter=self.formatter,
                                        cls=ScCompositeListItem,
                                        selection_mode='single',
                                        allow_empty_selection=False)

        super(ScannerViewModal, self).__init__(**kwargs)
        self.add_widget(ListView(adapter=self.list_adapter))

        detail_view = ScDetailView(sc_name=self.list_adapter.selection[0].text, size_hint=(.6, 1.0))

        self.list_adapter.bind(
            on_selection_change=detail_view.sc_changed)
        self.add_widget(detail_view)

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

