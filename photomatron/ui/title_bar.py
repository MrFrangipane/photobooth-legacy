from PySide2 import QtWidgets

from photomatron.hardware.types_ import WifiStatus

from guibedos.helpers import set_style_property


class TitleBar(QtWidgets.QWidget):
    """
    Top bar widget for status and messages
    """
    def __init__(self, title, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)
        layout = QtWidgets.QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.label_title = QtWidgets.QLabel(title)
        set_style_property(self.label_title, 'title')

        self.label_space = QtWidgets.QLabel("Available disk space...")
        set_style_property(self.label_space, 'wifi')

        self.label_temperature = QtWidgets.QLabel("Temperature ...")
        set_style_property(self.label_temperature, 'wifi')

        self.label_wifi_ssid = QtWidgets.QLabel("Wifi ...")
        set_style_property(self.label_wifi_ssid, 'wifi')
        self.label_wifi_icon = QtWidgets.QLabel()
        self.label_wifi_icon.setFixedSize(16, 16)

        set_style_property(self.label_wifi_icon, 'wifi-waiting')

        layout.addWidget(self.label_title, 0, 0, 2, 1)
        layout.addWidget(self.label_space, 0, 1)
        layout.addWidget(self.label_temperature, 1, 1)
        layout.addWidget(self.label_wifi_ssid, 0, 2, 2, 1)
        layout.addWidget(self.label_wifi_icon, 0, 3)

        layout.setColumnStretch(0, 100)

    def set_available_disk_space(self, space):
        if space >= 1000:
            self.label_space.setText(f"Free disk space {space / 1024:.1f}GB")
        else:
            self.label_space.setText(f"Free disk space {space:.1f}MB")

    def set_cpu_temperature(self, temperature):
        self.label_temperature.setText(f"CPU Temp {temperature:.1f}°C")

    def set_wifi_status(self, wifi_status):
        if wifi_status.status == WifiStatus.CONNECTED:
            set_style_property(self.label_wifi_icon, 'wifi-ok')
            self.label_wifi_ssid.setText(wifi_status.ssid + '\n' + wifi_status.ip_address)

        elif wifi_status.status == WifiStatus.DISCONNECTED:
            set_style_property(self.label_wifi_icon, 'wifi-waiting')
            self.label_wifi_ssid.setText("Wifi not connected")

        elif wifi_status.status == WifiStatus.ERROR:
            set_style_property(self.label_wifi_icon, 'wifi-error')
            self.label_wifi_ssid.setText(wifi_status.message)
