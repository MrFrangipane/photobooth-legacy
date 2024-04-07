from PySide2 import QtWidgets
from PySide2 import QtCore

from .title_bar import TitleBar
from .activity_selector import ActivitySelector
from .buttons_worker import ButtonsWorker


class Window(QtWidgets.QWidget):
    closed = QtCore.Signal()

    def __init__(self, app, title, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)
        self.setWindowTitle(title)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        self.title_bar = TitleBar(title)
        self.activity_selector = ActivitySelector(app)

        self.buttons_worker = ButtonsWorker(app.raspberry_pi.buttons)
        self.buttons_worker.changed.connect(app.button_changed)
        self._init_buttons_thread()

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self.title_bar)
        layout.addWidget(self.activity_selector)
        layout.setRowStretch(1, 100)

        self.setWindowTitle(title)
        self.setFixedSize(800, 480)

    def closeEvent(self, event):
        self.closed.emit()
        self.buttons_thread.quit()
        QtWidgets.QWidget.closeEvent(self, event)

    def _init_buttons_thread(self):
        self.buttons_thread = QtCore.QThread()
        self.buttons_worker.moveToThread(self.buttons_thread)
        self.closed.connect(self.buttons_worker.stop)
        self.buttons_thread.started.connect(self.buttons_worker.exec_)
        self.buttons_thread.finished.connect(self.buttons_thread.deleteLater)
        self.buttons_thread.start()
