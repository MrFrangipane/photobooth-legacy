import os.path

from PySide2 import QtGui
from PySide2 import QtCore

PADDING_X = 40
PADDING_Y = 40
SIZE = 540


def assemble(photo_filepath, foreground_filepath, assembly_filepath):
    if not os.path.isfile(foreground_filepath):
        raise FileExistsError(f'Impossible to find foreground {foreground_filepath}')

    if not os.path.isfile(photo_filepath):
        raise FileExistsError(f'Impossible to find photo {photo_filepath}')

    foreground = QtGui.QPixmap(foreground_filepath)
    photo = QtGui.QPixmap(photo_filepath)

    canvas = QtGui.QPixmap(foreground.size())
    canvas.fill(QtCore.Qt.transparent)
    canvas.fill(QtCore.Qt.white)

    painter = QtGui.QPainter()
    painter.begin(canvas)
    painter.drawPixmap(
        int((canvas.width() - photo.width()) / 2),
        int((canvas.height() - photo.height()) / 2),
        photo
    )
    painter.drawPixmap(
        int((canvas.width() - foreground.width()) / 2),
        int((canvas.height() - foreground.height()) / 2),
        foreground
    )
    painter.end()

    canvas.save(assembly_filepath, "jpg", 100)
