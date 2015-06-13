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
from model.Client import Client
from controller import Active
from model.Config import Config
from model.QrElem import *
from model.ScanElem import *
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from view.data.modules.scanner import *
from view.data.modules.quarantine import *
from model.Exceptions import QrException

## Variable used to determine whether to schedule refresh event
update = 0
## Variable used to avoid multiple instances of warning whether list is empty
empty = 0

## Extends CompositeListItem to add text attribute
class QrCompositeListItem(CompositeListItem):
    text = ''

## The view of an individual quarantine item
class QrDetailView(GridLayout):
    ## Quarantine items name
    qr_name = StringProperty('', allownone=True)
    obj = None

    ## Constructor
    def __init__(self, **kwargs):
        kwargs['cols'] = 1
        self.qr_name = kwargs.get('qr_name', '')
        super(QrDetailView, self).__init__(**kwargs)
        self.size_hint_x = 1.0
        if self.qr_name:
            self.redraw()

    ## Redraws the detail view
    def redraw(self, *args):
        self.clear_widgets()
        if self.qr_name:
            for x in range(0, len(Active.qrList)):
                if Active.qrList[x].f_name == self.qr_name:
                    box1 = BoxLayout(orientation='horizontal')
                    box2 = BoxLayout(orientation='horizontal')
                    box3 = BoxLayout(orientation='horizontal')
                    box4 = BoxLayout(orientation='horizontal')
                    box1.add_widget(Label(text="Filename  :", halign='right'))
                    box1.add_widget(Label(text=self.qr_name))
                    box2.add_widget(Label(text="Old Path  :", halign='right'))
                    box2.add_widget(Label(text=Active.qrList[x].o_path))
                    box3.add_widget(Label(text="Entry Date:", halign='right'))
                    box3.add_widget(Label(text=format(Active.qrList[x].get_begin())))
                    box3.add_widget(Label(text="Expiration:", halign='right'))
                    box3.add_widget(Label(text=format(Active.qrList[x].get_expire())))
                    box4.add_widget(Button(text="Restore From Quarantine",
                                           on_press=lambda a: self.restoreItem(Active.qrList[x], x)))
                    box4.add_widget(Button(text="Permanently Delete",
                                           on_press=lambda a: self.deleteItem(Active.qrList[x], x)))
                    self.add_widget(box1)
                    self.add_widget(box2)
                    self.add_widget(box3)
                    self.add_widget(box4)
                    break

    ## Determines whether to redraw if selection has changed
    # @param list_adapter
    # @param args
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

    ## Triggered when restoring an item from Klearnel's Quarantine
    # @param item The item to restore
    # @param index The items index in the local list
    # @exception QrException
    def restoreItem(self, item, index):
        try:
            Active.qr_task.restore_from_qr(Active.client, item.f_name)
        except QrException as qr:
            popup = Popup(size_hint=(None, None), size=(400, 150))
            popup.add_widget(Label(text=qr.value))
            popup.bind(on_press=popup.dismiss)
            popup.title = qr.title
            popup.open()
            return
        Active.qrList.pop(index)
        global update
        update = 1

    ## Triggered when removing an item from Klearnel's Quarantine
    # @param item The item to remove
    # @param index The items index in the local list
    # @exception QrException
    def deleteItem(self, item, index):
        try:
            Active.qr_task.rm_from_qr(Active.client, item.f_name)
        except QrException as qr:
            popup = Popup(size_hint=(None, None), size=(400, 150))
            popup.add_widget(Label(text=qr.value))
            popup.bind(on_press=popup.dismiss)
            popup.title = qr.title
            popup.open()
            return
        Active.qrList.pop(index)
        global update
        update = 1

## Class containing all necessary components for creating a dynamic list view
class QuarantineViewModal(BoxLayout):

    ## Constructon
    # @exception QrException
    # @exception EmptyListException
    def __init__(self, **kwargs):
        self.qrdata = list()
        # FOR NETWORK
        Active.qrList.clear()
        try:
            Active.qrList = Active.qr_task.get_qr_list(Active.client)
        except QrException as qr:
            popup = Popup(size_hint=(None, None), size=(400, 150))
            popup.add_widget(Label(text=qr.value))
            popup.bind(on_press=popup.dismiss)
            popup.title = qr.title
            popup.open()
        except EmptyListException as ee:
            global empty
            if empty is 0:
                empty = 1
                popup = Popup(size_hint=(None, None), size=(400, 150))
                popup.add_widget(Label(text=ee.value))
                popup.bind(on_press=popup.dismiss)
                popup.title = ee.title
                popup.open()
        for x in range(0, len(Active.qrList)):
            self.qrdata.append({'filename': Active.qrList[x].f_name,
                                'old_path': Active.qrList[x].o_path})

        self.list_adapter = ListAdapter(data=self.qrdata,
                                        args_converter=self.formatter,
                                        selection_mode='single',
                                        allow_empty_selection=False,
                                        cls=QrCompositeListItem)

        super(QuarantineViewModal, self).__init__(**kwargs)
        self.list_view = ListView(adapter=self.list_adapter)
        self.add_widget(self.list_view)
        if len(self.qrdata) is 0:
            detail_view = QrDetailView(qr_name="List is empty", size_hint=(.6, 1.0))
        else:
            detail_view = QrDetailView(qr_name=self.list_adapter.selection[0].text,
                                       size_hint=(.6, 1.0))

        self.list_adapter.bind(
            on_selection_change=detail_view.qr_changed)
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
        if Active.changed['qr'] != 0:
            Active.changed['qr'] = 0
            Clock.schedule_once(lambda dt: self.update_list(), 0.1)

    ## Updates the Quarantine list
    # @exception QrException
    # @exception EmptyListException
    def update_list(self):
        try:
            Active.qrList = Active.qr_task.get_qr_list(Active.client)
        except QrException as qr:
            popup = Popup(size_hint=(None, None), size=(400, 150))
            popup.add_widget(Label(text=qr.value))
            popup.bind(on_press=popup.dismiss)
            popup.title = qr.title
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
        self.qrdata.clear()
        for x in range(0, len(Active.qrList)):
                self.qrdata.append({'filename': Active.qrList[x].f_name,
                                  'old_path': Active.qrList[x].o_path})
        self.list_adapter.data = self.qrdata
        if hasattr(self.list_view, '_reset_spopulate'):
            self.list_view._reset_spopulate()

    ## The args converter
    def formatter(self, rowindex, qr_data):
        return {'text': qr_data['filename'],
                'size_hint_y': None,
                'height': 50,
                'cls_dicts': [{'cls': ListItemButton,
                               'kwargs': {'text': qr_data['filename']}},
                              {'cls': ListItemLabel,
                               'kwargs': {'text': "Old Path:"}},
                              {'cls': ListItemLabel,
                               'kwargs': {'text': qr_data['old_path']}}]}
