from PySide2 import QtWidgets

from guibedos.helpers import set_style_property
from guibedos.widgets import FlowLayout


class ActivitySelector(QtWidgets.QWidget):
    """
    Let the user select what to do
    """
    def __init__(self, app, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)

        activities = QtWidgets.QWidget()
        system = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(activities)
        layout.addWidget(system)
        layout.setStretch(0, 100)

        #
        ##
        layout_activities = FlowLayout(activities)
        layout_activities.setContentsMargins(0, 0, 0, 0)
        layout_activities.setSpacing(20)

        self.button_timelapse = QtWidgets.QPushButton("Timelapse")
        set_style_property(self.button_timelapse, 'large')
        self.button_timelapse.clicked.connect(app.activity_timelapse)
        layout_activities.addWidget(self.button_timelapse)

        self.button_photobooth = QtWidgets.QPushButton("Photobooth")
        set_style_property(self.button_photobooth, 'large')
        self.button_photobooth.clicked.connect(app.activity_photobooth)
        layout_activities.addWidget(self.button_photobooth)

        #
        ##
        layout_system = FlowLayout(system)
        layout_system.setContentsMargins(0, 0, 0, 0)
        layout_system.setSpacing(20)

        self.button_renew_dhcp = QtWidgets.QPushButton("Renew DHCP")
        set_style_property(self.button_renew_dhcp, 'medium')
        self.button_renew_dhcp.clicked.connect(app.renew_dhcp)
        layout_system.addWidget(self.button_renew_dhcp)

        self.button_update = QtWidgets.QPushButton("Update app")
        set_style_property(self.button_update, 'medium')
        self.button_update.clicked.connect(app.update)
        layout_system.addWidget(self.button_update)

        self.button_exit = QtWidgets.QPushButton("Exit app")
        set_style_property(self.button_exit, 'medium')
        self.button_exit.clicked.connect(app.quit)
        layout_system.addWidget(self.button_exit)

        self.button_shutdown = QtWidgets.QPushButton("Shutdown pi")
        set_style_property(self.button_shutdown, 'medium')
        self.button_shutdown.clicked.connect(app.shutdown)
        layout_system.addWidget(self.button_shutdown)

        self.button_reboot = QtWidgets.QPushButton("Reboot pi")
        set_style_property(self.button_reboot, 'medium')
        self.button_reboot.clicked.connect(app.reboot)
        layout_system.addWidget(self.button_reboot)

        self.button_wifi = QtWidgets.QPushButton("Add Wifi")
        set_style_property(self.button_wifi, 'medium')
        self.button_wifi.clicked.connect(app.add_wifi)
        layout_system.addWidget(self.button_wifi)

        self.button_show_log = QtWidgets.QPushButton("Show inst. log")
        set_style_property(self.button_show_log, 'medium')
        self.button_show_log.clicked.connect(app.show_log)
        layout_system.addWidget(self.button_show_log)

        self.button_empty_print_queue = QtWidgets.QPushButton("Empty print queue")
        set_style_property(self.button_empty_print_queue, 'medium')
        self.button_empty_print_queue.clicked.connect(app.empty_print_queue)
        layout_system.addWidget(self.button_empty_print_queue)
