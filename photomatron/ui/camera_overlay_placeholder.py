from PySide2 import QtCore
from PySide2 import QtWidgets

from guibedos.helpers import set_style_property


class CameraOverlayPlaceholder(QtWidgets.QLabel):
    """
    Holds Raspberry Pi camera overlay Geometry
    """
    resized = QtCore.Signal()

    def __init__(self, parent=None):
        QtWidgets.QLabel.__init__(self, parent)
        set_style_property(self, "activity")
        self.setText("Please wait for camera ...")

    def resizeEvent(self, event):
        self.resized.emit()
        return QtWidgets.QLabel.resizeEvent(self, event)

    @property
    def geometry_global(self):
        geo = self.geometry()
        return QtCore.QRect(self.mapToGlobal(geo.topLeft()), geo.size())
