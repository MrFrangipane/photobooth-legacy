from PySide2.QtWidgets import QDialog, QListWidget, QGridLayout, QLineEdit, QPushButton, QLabel
from PySide2.QtCore import QTimer

import pywifi
from pywifi.iface import Interface as PyWifiInterface
from guibedos.helpers import set_style_property

from .extensions import update_list_widget



class WifiConfigDialog(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self._wlan_interface: PyWifiInterface = None

        self.setWindowTitle("Add Wifi")
        self.resize(720, 400)

        self._list_ssids = QListWidget()
        self._line_password = QLineEdit()
        self._button_add = QPushButton("Add")

        _label_password = QLabel("Password:")

        set_style_property(self._list_ssids, "small")
        set_style_property(_label_password, "small")
        set_style_property(self._line_password, "small")
        set_style_property(self._button_add, "small")

        layout = QGridLayout(self)
        layout.addWidget(self._list_ssids, 0, 0, 1, 3)
        layout.addWidget(_label_password, 1, 0)
        layout.addWidget(self._line_password, 1, 1)
        layout.addWidget(self._button_add, 1, 2)

        self._timer_list_refresh = QTimer(self)

        self._timer_list_refresh.timeout.connect(self._timer_list_refresh_timeout)
        self._button_add.clicked.connect(self._add_ssid)
        self.accepted.connect(self._timer_list_refresh.stop)
        self.finished.connect(self._timer_list_refresh.stop)
        self.rejected.connect(self._timer_list_refresh.stop)

    def list_ssids(self):
        self._timer_list_refresh.start(200)
        self._list_ssids.clear()

        interfaces = pywifi.PyWiFi().interfaces()
        if not interfaces:
            self._list_ssids.addItem("No wifi interface")
            self._list_ssids.setEnabled(False)
            self._line_password.setEnabled(False)
            self._button_add.setEnabled(False)
            return

        self._wlan_interface = interfaces[-1]
        self._wlan_interface.scan()
        self._timer_list_refresh.start(200)

    def _add_ssid(self):
        profile = self._wlan_interface.scan_results()[self._list_ssids.currentRow()]
        profile.key = self._line_password.text()
        self._wlan_interface.add_network_profile(profile)
        self._wlan_interface.connect(profile)
        self.accept()

    def _timer_list_refresh_timeout(self):
        if self._wlan_interface is None:
            return

        update_list_widget(self._list_ssids, [p.ssid for p in self._wlan_interface.scan_results()])
        self._list_ssids.setEnabled(True)
        self._line_password.setEnabled(True)
        self._button_add.setEnabled(True)
