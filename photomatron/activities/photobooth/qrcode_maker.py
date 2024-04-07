import os.path

from PySide2.QtCore import Qt
from PySide2.QtGui import QImage, QPixmap, QPainter
import qrcode


class _QRCodeImage(qrcode.image.base.BaseImage):
    def __init__(self, border, width, box_size, *args, **kwargs):
        # qrcode.image.base.BaseImage.__init__(self, border, width, box_size, *args, **kwargs)
        self.border = border
        self.width = width
        self.box_size = box_size
        size = (width + border * 2) * box_size
        self._image = QImage(
            size, size, QImage.Format_RGB16)
        self._image.fill(Qt.white)

    def pixmap(self):
        return QPixmap.fromImage(self._image)

    def drawrect(self, row, col):
        painter = QPainter(self._image)
        painter.fillRect(
            (col + self.border) * self.box_size,
            (row + self.border) * self.box_size,
            self.box_size, self.box_size,
            Qt.black
        )

    def save(self, stream, kind=None):
        pass


def make_qr_code(data, jpg_filepath, draw_logo):
    # QR code
    qr_code_pixmap = qrcode.make(
        data=data,
        image_factory=_QRCodeImage,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        border=0
    ).pixmap()

    # Logo
    qr_code_logo = QPixmap(os.path.dirname(__file__) + '/qr-code-talent-chill.png')
    qr_code_logo = qr_code_logo.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    # Assemble on canvas
    canvas = QPixmap(qr_code_pixmap.width(), qr_code_pixmap.height())
    canvas.fill(Qt.transparent)
    canvas.fill(Qt.white)

    painter = QPainter()
    painter.begin(canvas)
    painter.drawPixmap(0, 0, qr_code_pixmap)
    if draw_logo:
        painter.drawPixmap(
            int((qr_code_pixmap.width() - qr_code_logo.width()) / 2),
            int((qr_code_pixmap.height() - qr_code_logo.height()) / 2),
            qr_code_logo
        )
    painter.end()

    canvas = canvas.scaled(384, 384, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    canvas.save(jpg_filepath, "jpg", 100)
