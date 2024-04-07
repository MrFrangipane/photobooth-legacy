from PySide2.QtWidgets import QDialog, QCheckBox, QGridLayout, QLabel, QPushButton
from PySide2.QtCore import Qt

from photomatron.ui.extensions import create_with_style_property


class PhotoboothConfigurationDialog(QDialog):
    """
    Photobooth configuration
    """
    def __init__(self, activity, parent=None):
        self.activity = activity
        QDialog.__init__(self, parent)

        self._check_cloud = QCheckBox("Cloud upload")
        self._check_nice_print = QCheckBox("Nice print")
        self._check_ticket_print = QCheckBox("Ticket print")

        self._label_status = create_with_style_property(QLabel, "message-small")

        self._button_ok = create_with_style_property(QPushButton, "medium", "OK")
        self._button_ok.clicked.connect(self.accept)

        self._button_cancel = create_with_style_property(QPushButton, "medium", "Cancel")
        self._button_cancel.clicked.connect(self.reject)

        layout = QGridLayout(self)
        layout.addWidget(create_with_style_property(QLabel, "message-title", "Please check options"), 0, 0, 1, 2)
        layout.addWidget(self._check_cloud, 1, 0, 1, 2)
        layout.addWidget(self._check_nice_print, 2, 0, 1, 2)
        layout.addWidget(self._check_ticket_print, 3, 0, 1, 2)
        layout.addWidget(self._label_status, 4, 0, 1, 2)
        layout.addWidget(self._label_status, 5, 0, 1, 2)
        layout.addWidget(self._button_ok, 6, 0)
        layout.addWidget(self._button_cancel, 6, 1)

        self._label_status.setText("Internet not available: no cloud upload will be done")

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedSize(800, 480)
        self.setFocus()
