import sys
import traceback

from PySide2 import QtCore


class ButtonsWorker(QtCore.QObject):
    changed = QtCore.Signal(bool)

    def __init__(self, buttons, parent=None):
        QtCore.QObject.__init__(self, parent)
        self.buttons = buttons
        self.buttons.parent = self

    def changed_(self, button, state):
        self.buttons.set_led(state)
        self.changed.emit(state)

    def exec_(self):
        try:
            self.buttons.exec_()
        except Exception as e:
            # be verbal since we are in a QThread
            traceback.print_exc(file=sys.stdout)
            raise

    def stop(self):
        self.buttons.stop()
