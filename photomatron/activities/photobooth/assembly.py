import os.path

from PySide2 import QtGui
from PySide2 import QtCore

PADDING_X = 40
PADDING_Y = 40
SIZE = 540


def assemble(photo_filepaths, foreground_filepath, assembly_filepath, photo_mode: str):
    if not os.path.isfile(foreground_filepath):
        raise FileExistsError(f'Impossible to find foreground {foreground_filepath}')

    for photo_filepath in photo_filepaths:
        if not os.path.isfile(photo_filepath):
            raise FileExistsError(f'Impossible to find photo {photo_filepath}')

    foreground = QtGui.QPixmap(foreground_filepath)
    canvas = QtGui.QPixmap(foreground.size())
    canvas.fill(QtCore.Qt.transparent)
    canvas.fill(QtCore.Qt.white)

    painter = QtGui.QPainter()
    painter.begin(canvas)

    if photo_mode == 'single':
        photo = QtGui.QPixmap(photo_filepaths[0])
        photo = photo.transformed(QtGui.QTransform().scale(-1, 1))

        painter.drawPixmap(
            int((canvas.width() - photo.width()) / 2),
            int((canvas.height() - photo.height()) / 2),
            photo
        )

    elif photo_mode == 'quad':
        photos = [
            QtGui.QPixmap(photo_filepaths[i]).scaled(
                SIZE, SIZE,
                QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
            ) for i in range(4)
        ]

        painter = QtGui.QPainter()
        painter.begin(canvas)
        painter.drawPixmap(PADDING_X, PADDING_Y, photos[0])
        painter.drawPixmap(PADDING_X + PADDING_X + SIZE, PADDING_Y, photos[1])
        painter.drawPixmap(PADDING_X, PADDING_Y + PADDING_Y + SIZE, photos[2])
        painter.drawPixmap(PADDING_X + PADDING_X + SIZE, PADDING_Y + PADDING_Y + SIZE, photos[3])

    painter.drawPixmap(
        int((canvas.width() - foreground.width()) / 2),
        int((canvas.height() - foreground.height()) / 2),
        foreground
    )
    painter.end()

    canvas.save(assembly_filepath, "jpg", 100)
