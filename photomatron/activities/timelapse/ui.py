import guibedos.helpers
from PySide2 import QtCore
from PySide2 import QtWidgets

from photomatron.ui.camera_overlay_placeholder import CameraOverlayPlaceholder


class TimelapseActivityDialog(QtWidgets.QWidget):
    """
    Photobooth activity
    """
    def __init__(self, activity, parent=None):
        self.activity = activity
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        self.camera_placeholder = CameraOverlayPlaceholder()
        self.camera_placeholder.resized.connect(self.update_camera_placeholder)
        self.camera_placeholder.setFixedWidth(self.camera_placeholder.height())

        self.title = QtWidgets.QLabel("Timelapse")
        guibedos.helpers.set_style_property(self.title, 'message-title')

        self.message = QtWidgets.QLabel("paused")
        guibedos.helpers.set_style_property(self.message, 'message')

        layout = QtWidgets.QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.camera_placeholder, 0, 0, 4, 1)
        layout.addWidget(QtWidgets.QLabel(), 0, 1)
        layout.addWidget(self.title, 1, 1)
        layout.addWidget(self.message, 2, 1)
        layout.addWidget(QtWidgets.QLabel(), 3, 1)
        layout.setRowStretch(0, 50)
        layout.setRowStretch(3, 50)

        self.setFixedSize(800, 480)
        self.setFocus()

    def update_camera_placeholder(self):
        geometry = self.camera_placeholder.geometry_global
        self.activity.update_camera_placeholder(geometry.x(), geometry.y(), geometry.width(), geometry.height())

    def set_title(self, title):
        self.title.setVisible(bool(title))
        self.title.setText(title)
        QtWidgets.QApplication.processEvents()

    def set_message(self, message, style='message'):
        self.message.setVisible(bool(message))
        self.message.setText(message)
        guibedos.helpers.set_style_property(self.message, style)
        QtWidgets.QApplication.processEvents()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.activity.terminate()
            self.deleteLater()

        QtWidgets.QWidget.keyPressEvent(self, event)
