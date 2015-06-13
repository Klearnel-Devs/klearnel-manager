## @package view
#   Defines classes to be displayed by the GUI
#
# @author Antoine Ceyssens <a.ceyssens@nukama.be> & Derek Van Hove <d.vanhove@nukama.be>
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
from model.Exceptions import ScanException, EmptyListException
from kivy.uix.popup import Popup
from kivy.clock import Clock

## Variable used to determine whether to schedule refresh event
update = 0
## Variable used to avoid multiple instances of warning whether list is empty
empty = 0

## Extends CompositeListItem to add text attribute
class ScCompositeListItem(CompositeListItem):
    text = ''

## Defined in Kivy files
class ScCheckBox(CheckBox, ListItemLabel):
    def __init__(self, **kwargs):
        super(ScCheckBox, self).__init__(**kwargs)

## Defined in Kivy files
class ScLabel(ListItemLabel):
    pass

## Defined in Kivy files
class AddScannerElementButton(Button):
    pass

## Extends ToggleButton to add value attribute
class ScToggleButton(ToggleButton):
    value = StringProperty('', allownone=True)

    def __init__(self, **kwargs):
        self.value = kwargs.get('value', '')
        super(ScToggleButton, self).__init__(**kwargs)

class HeaderBox(BoxLayout):
    pass

## The view of an individual scanner item
class ScDetailView(BoxLayout):
    ## Quarantine items name
    sc_name = StringProperty('', allownone=True)
    obj = None

    ## Constructor
    def __init__(self, **kwargs):
        self.sc_name = kwargs.get('sc_name', '')
        super(ScDetailView, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_x = 1.0
        if self.sc_name:
            self.redraw()

    ## Redraws the detail view
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
                    break

    ## Callback on clock schedule to redraw
    def callback(self):
        Clock.schedule_once(lambda dt: self.redraw(), 0.5)

    ## Validates deletion of item from Scanner list
    # @param item The item to delete
    # @param index The index found
    # @exception ScanException
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

    ## Determines whether to redraw if selection has changed
    # @param list_adapter
    # @param args
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

## Class containing all necessary components for creating a dynamic list view
class ScannerViewModal(BoxLayout):

    ## Constructor
    # @exception ScanException
    # @exception EmptyListException
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
        except EmptyListException as ee:
            global empty
            if empty is 0:
                empty = 1
                popup = Popup(size_hint=(None, None), size=(400, 150))
                popup.add_widget(Label(text=ee.value))
                popup.bind(on_press=popup.dismiss)
                popup.title = ee.title
                popup.open()
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
        self.add_widget(HeaderBox())
        self.add_widget(self.list_view)
        if len(self.scdata) is 0:
            detail_view = ScDetailView(sc_name="List is empty", size_hint=(.6, 1.0))
        else:
            detail_view = ScDetailView(sc_name=self.list_adapter.selection[0].text, size_hint=(.6, 1.0))

        self.list_adapter.bind(
            on_selection_change=detail_view.sc_changed)
        self.add_widget(detail_view)
        Clock.schedule_interval(self.callback, 60)
        Clock.schedule_interval(self.callback2, 5)

    ## Callback on clock schedule to update list
    def callback(self, dt):
        self.update_list()

    ## Callback on clock schedule to update list
    def callback2(self, dt):
        global update
        if update != 0:
            update = 0
            Clock.schedule_once(lambda dt: self.update_list(), 0.1)
        if Active.changed['sc'] != 0:
            Active.changed['sc'] = 0
            Clock.schedule_once(lambda dt: self.update_list(), 0.1)

    ## Updates the Scanner list
    # @exception ScanException
    # @exception EmptyListException
    def update_list(self):
        try:
            Active.scanList = Active.scan_task.get_scan_list(Active.client)
        except ScanException as se:
            popup = Popup(size_hint=(None, None), size=(400, 150))
            popup.add_widget(Label(text=se.value))
            popup.bind(on_press=popup.dismiss)
            popup.title = se.title
            popup.open()
            return
        except EmptyListException as ee:
            global empty
            if empty is 0:
                empty = 1
                popup = Popup(size_hint=(None, None), size=(400, 150))
                popup.add_widget(Label(text=ee.value))
                popup.bind(on_press=popup.dismiss)
                popup.title = ee.title
                popup.open()
        self.scdata.clear()
        for x in range(0, len(Active.scanList)):
            self.scdata.append({'path': Active.scanList[x].path,
                              'options': Active.scanList[x].options})
        self.list_adapter.data = self.scdata
        if hasattr(self.list_view, '_reset_spopulate'):
            self.list_view._reset_spopulate()

    ## The args converter
    def formatter(self, rowindex, scdata):
        return {'text': scdata['path'],
                'size_hint_y': None,
                'height': 50,
                'cls_dicts': [{'cls': ListItemButton,
                               'kwargs': {'text': scdata['path'],
                                          'size_hint_x': 0.5}},
                              {'cls': ScCheckBox,
                               'kwargs': {'disabled': True,
                                          'active': True if bool(scdata['options']['BR_S']) else False,
                                          'size_hint_x': 0.1}},
                              {'cls': ScCheckBox,
                               'kwargs': {'disabled': True,
                                          'active': True if bool(scdata['options']['DUP_S']) else False,
                                          'size_hint_x': 0.1}},
                              {'cls': ScCheckBox,
                               'kwargs': {'disabled': True,
                                          'active': True if bool(scdata['options']['BACKUP']) else False,
                                          'size_hint_x': 0.1}},
                              {'cls': ScCheckBox,
                               'kwargs': {'disabled': True,
                                          'active': True if bool(scdata['options']['DEL_F_SIZE']) else False,
                                          'size_hint_x': 0.1}},
                              {'cls': ScCheckBox,
                               'kwargs': {'disabled': True,
                                          'active': True if bool(scdata['options']['DUP_F']) else False,
                                          'size_hint_x': 0.1}},
                              {'cls': ScCheckBox,
                               'kwargs': {'disabled': True,
                                          'active': True if bool(scdata['options']['INTEGRITY']) else False,
                                          'size_hint_x': 0.1}},
                              {'cls': ScCheckBox,
                               'kwargs': {'disabled': True,
                                          'active': True if bool(scdata['options']['CL_TEMP']) else False,
                                          'size_hint_x': 0.1}},
                              {'cls': ScCheckBox,
                               'kwargs': {'disabled': True,
                                          'active': True if bool(scdata['options']['DEL_F_OLD']) else False,
                                          'size_hint_x': 0.1}},
                              {'cls': ScCheckBox,
                               'kwargs': {'disabled': True,
                                          'active': True if bool(scdata['options']['BACKUP_OLD']) else False,
                                          'size_hint_x': 0.1}}]}

