import os
import shutil
import subprocess

import pywifi

from .types_ import *
from .abstract import AbstractRaspberry
from .camera import Camera
from .buttons import Buttons
from .printer import Printer
from . import thermal_printer


class Raspberry(AbstractRaspberry):

    def __init__(self, photo_mode: str):
        AbstractRaspberry.__init__(self)
        self.camera = Camera(photo_mode)
        self.buttons = Buttons()
        self.printer = Printer()

    def post_qapp(self, app):
        pass

    def post_show(self, window):
        pass

    def print(self, filepath, printer_name):
        self.printer.print_picture(filepath, printer_name)

    def thermal_print(self, data, double_size=False):
        if isinstance(data, int):
            thermal_printer.feed(data)
        else:
            thermal_printer.print_(data, double_size)

    @property
    def wifi_status(self):  # FIXME use pywifi now that we use it elsewhere
        try:
            result = subprocess.check_output('iwgetid')

            if result:
                ssid = result.decode().split('"')[1]
                ip_address = subprocess.check_output(['hostname', '-I']).decode().splitlines()[0]

                return WifiStatus(WifiStatus.CONNECTED, ssid=ssid, ip_address=ip_address)

        except subprocess.CalledProcessError:
            return WifiStatus(WifiStatus.ERROR, message="Wifi error")

        return WifiStatus(WifiStatus.DISCONNECTED)

    @property
    def cpu_temperature(self):
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as file_temperature:
            return int(file_temperature.read()) / 1000

    @property
    def available_disk_space(self):
        usage = shutil.disk_usage('.')
        return usage.free / 1024 / 1024

    def reboot(self):
        if hasattr(os, "sync"):
            os.sync()

        subprocess.call(['sudo', 'reboot', 'now'])

    def shutdown(self):
        if hasattr(os, "sync"):
            os.sync()

        subprocess.call(['sudo', 'shutdown', 'now'])

    def renew_dhcp(self):
        subprocess.call(['sudo', 'systemctl', 'restart', 'dhcpcd'])
