from PySide2.QtCore import QObject, QTimer


class Timer(QObject):
    def __init__(self, interval, callback, parent=None):
        QObject.__init__(self, parent)
        self._callback = callback
        self._timer = QTimer()
        self._timer.setInterval(interval * 1000)
        self._timer.timeout.connect(callback)

    def start(self):
        self._callback()
        self._timer.start()

    def stop(self):
        self._timer.stop()
