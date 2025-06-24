import os.path
import shutil
import time

from PySide2.QtWidgets import QPushButton

from .types_ import *
from .abstract import AbstractRaspberry
from photomatron.application import Application


class MockCamera:

    def init_cam(self):
        print('Mock camera init')

    def start_preview(self):
        print('Mock camera start preview')

    def set_geometry(self, x, y, w, h):
        print(f'Mock camera set geometry x={x}, y={y}, w={w}, h={h}')

    def capture(self, filepath):
        print(f'Mock camera capture to {filepath}')
        here = os.path.dirname(__file__)
        mock_filepath = os.path.join(os.path.dirname(here), "ui", "resources", "sample-capture.jpg")
        shutil.copyfile(mock_filepath, filepath)
        time.sleep(0.2)

    def close(self):
        print('Mock camera close')


class MockButtons:

    def exec_(self):
        print('Mock button exec_')


class Mock(AbstractRaspberry):
    LEFT = 'LEFT'
    CENTER = 'CENTER'
    RIGHT = 'RIGHT'

    def __init__(self):
        AbstractRaspberry.__init__(self)
        self.app = None
        self.camera = MockCamera()
        self.buttons = MockButtons()

    def _button(self):
        self.app.button_changed(self.button.isDown())

    def post_qapp(self, app: Application):
        self.app = app

        self.button = QPushButton('BUTTON CENTER')
        self.button.setFixedSize(200, 200)
        self.button.setWindowTitle("Photomatron's Button")
        self.button.pressed.connect(self._button)
        self.button.released.connect(self._button)
        self.button.show()

    def post_show(self, window):
        self.button.move(window.geometry().right(), self.button.pos().y())

    @property
    def wifi_status(self):
        import random
        return random.choice([
            WifiStatus(WifiStatus.DISCONNECTED),
            WifiStatus(WifiStatus.CONNECTED, ssid='Mock SSID', ip_address='0.0.0.0'),
            WifiStatus(WifiStatus.ERROR, message='Mock error has occured'),
        ])

    @property
    def cpu_temperature(self):
        return 47.248

    @property
    def available_disk_space(self):
        return 39329.73046875

    def print(self, filepath, printer_name):
        print(f"Mock print {filepath} to {printer_name}")

    def thermal_print(self, data, double_size=False):
        print(f"Mock thermal print (double_size:{double_size})")
        print(data)
        time.sleep(1)
        print("-" * 10)

    @property
    def camera_overlay_geometry(self):
        return None

    @camera_overlay_geometry.setter
    def camera_overlay_geometry(self, value):
        print("Mock set camera overlay geometry :", value)

    def reboot(self):
        print("Mock reboot = quit")
        self.button.close()

    def shutdown(self):
        print("Mock shutdown = quit")
        self.button.close()

    def renew_dhcp(self):
        print("Mock renew DHCP")

    def empty_print_queue(self):
        print("Mock empty print queue")
