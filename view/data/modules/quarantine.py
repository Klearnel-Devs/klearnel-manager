__author__ = 'Derek'
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

class QrCompositeListItem(CompositeListItem):
    text = ''

class QrDetailView(GridLayout):
    qr_name = StringProperty('', allownone=True)
    obj = None

    def __init__(self, **kwargs):
        kwargs['cols'] = 2
        self.qr_name = kwargs.get('qr_name', '')
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

class QuarantineViewModal(BoxLayout):
    data = ListProperty()

    def __init__(self, **kwargs):
        self.qrdata = list()
        for x in range(0, len(Active.qrList)):
            self.qrdata.append({'filename': Active.qrList[x].f_name,
                                'old_path': Active.qrList[x].o_path})

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

    def formatter(self, rowindex, qr_data):
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
