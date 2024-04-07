import os.path
import subprocess
import sys
import datetime

from PySide2 import QtWidgets

import guibedos.helpers
from guibedos.helpers import load_stylesheet

from .ui.timer import Timer
from .ui.window import Window
from .ui.wifi_config import WifiConfigDialog
from .activities.photobooth import PhotoboothActivity
from .activities.timelapse import TimelapseActivity
from .hardware.types_ import WifiStatus
from .ui.extensions import confirmation_messagebox, WARNING


class Application:
    """
    Main application
    """
    def __init__(self, raspberry_pi, photobooth_working_folder):
        self.raspberry_pi = raspberry_pi

        self._install_log_filepath = os.path.expanduser('~/photobooth-updates.log')

        self._photobooth_working_folder = photobooth_working_folder

        self._qapp = QtWidgets.QApplication([])
        self.raspberry_pi.post_qapp(self)

        self.window = Window(app=self, title="Photomatron 2")
        load_stylesheet(self.window, os.path.dirname(__file__) + "/ui/resources/style.css")

        self.status_timer = Timer(interval=2, callback=self.update_status_bar)

        self._current_activity = None

    def exec_(self):
        self.window.show()
        self.raspberry_pi.post_show(self.window)
        self.status_timer.start()
        return self._qapp.exec_()

    def update_status_bar(self):
        self.window.title_bar.set_available_disk_space(self.raspberry_pi.available_disk_space)
        self.window.title_bar.set_cpu_temperature(self.raspberry_pi.cpu_temperature)
        self.window.title_bar.set_wifi_status(self.raspberry_pi.wifi_status)

    def button_changed(self, value):
        if self._current_activity is not None:
            self._current_activity.button_changed(value)

    #
    ##
    def quit(self):
        self.window.close()

    def reboot(self):
        self.window.close()
        self.raspberry_pi.reboot()

    def shutdown(self):
        self.window.close()
        self.raspberry_pi.shutdown()

    def update(self):
        with guibedos.helpers.Hourglass(self.window):
            output_text = subprocess.check_output([
                '/usr/bin/python3', '-m', 'pip', 'install', 'git+https://github.com/MrFrangipane/photobooth-legacy.git'
            ]).decode()
            with open(self._install_log_filepath, 'w') as log_file:
                log_file.write(datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
                log_file.write("\n")
                log_file.write(output_text)

            subprocess.Popen([sys.executable] + sys.argv)
            sys.exit(0)

    def renew_dhcp(self):
        self.raspberry_pi.renew_dhcp()

    def add_wifi(self):
        dialog = WifiConfigDialog(parent=self.window)
        dialog.list_ssids()
        dialog.setModal(True)
        dialog.exec_()

    def show_log(self):
        subprocess.call(["xdg-open", self._install_log_filepath])

    #
    ##
    def activity_timelapse(self):
        timelapse = TimelapseActivity(
            app=self,
            raspberry_pi=self.raspberry_pi,
            parent_window=self.window
        )
        timelapse.exec_()
        self._current_activity = timelapse

    def activity_timelapse_terminate(self):
        self._current_activity = None

    def activity_photobooth(self):
        photobooth = PhotoboothActivity(
            app=self,
            raspberry_pi=self.raspberry_pi,
            parent_window=self.window,
            working_folder=self._photobooth_working_folder
        )
        if photobooth.show_configuration_dialog():
            photobooth.exec_()
            self._current_activity = photobooth

    def activity_photobooth_terminate(self):
        self._current_activity = None
