import datetime
import os.path
import time
import secrets
import string
from dataclasses import dataclass

from PySide2.QtGui import QPixmap, QTransform, QPainter, QFont
from PySide2.QtCore import Qt

from photomatron.hardware.types_ import WifiStatus
from photomatron.hardware.raspberry import AbstractRaspberry

from .activity_dialog import PhotoboothActivityDialog
from .configuration_dialog import PhotoboothConfigurationDialog
from .assembly import assemble
from .qrcode_maker import make_qr_code
from .cloud import Cloud
from photomatron.ui.extensions import warning_messagebox


PRINTER = "Canon_SELPHY_CP1300"
FOREGROUND = 'foreground.png'
PRINT_TIME_SELPHY = 80
PRINT_TIME_THERMAL = 35
QR_CODE_TEMP_FILENAME = "qr-code-temp.jpg"
THERMAL_TEMP_FILENAME = "termal-temp"
MANUAL_URL = "photobooth.frangitron.com"
CLOUD_URL = f"https://{MANUAL_URL}/retrieve"
CLOUD_CREDENTIALS_FILE = os.path.dirname(__file__) + '/cloud-credentials.json'
QR_CODE_SIZE = 387
THERMAL_PADDING = 20
THERMAL_UID_SIZE = 60


class PhotoboothConfiguration:
    def __init__(self):
        self.photo_mode = None
        self.cloud_upload_enabled = None
        self.selphy_print_enabled = None
        self.thermal_print_enabled = None
        self.thermal_print_image_enabled = None


@dataclass
class ThermalPrintInfo:
    qr_code_filepath: str
    assembly_filepath: str
    temp_output_filepath: str
    uid: str
    is_print_image_enabled: bool


class PhotoboothActivity:

    def __init__(self, app, raspberry_pi, parent_window, working_folder, configuration: PhotoboothConfiguration):
        self.raspberry_pi = raspberry_pi
        self.raspberry_pi.camera.init_cam()
        self.raspberry_pi.camera.start_preview()

        self.working_folder = working_folder

        self.photo_mode = configuration.photo_mode
        self.cloud_upload_enabled = configuration.cloud_upload_enabled
        self.selphy_print_enabled = configuration.selphy_print_enabled
        self.thermal_print_enabled = configuration.thermal_print_enabled
        self.thermal_print_image_enabled = configuration.thermal_print_image_enabled

        self.dialog = PhotoboothActivityDialog(activity=self, parent=parent_window)
        self.configuration_dialog = PhotoboothConfigurationDialog(activity=self, parent=parent_window)

        self.app = app
        self.capturing = False

        self.reset()

        self.assembly_folder = os.path.join(self.working_folder, 'assembled')
        if not os.path.isdir(self.assembly_folder):
            os.mkdir(self.assembly_folder)

    def reset(self):
        self.capturing = False
        self.dialog.set_title("Photobooth")
        self.dialog.set_message("Push the button")

    def update_camera_placeholder(self, x, y, w, h):
        height = int(h * .6667)  # 3:2 hack
        offset = int((h - height) / 2)  # center vertically
        self.raspberry_pi.camera.set_geometry(x, y + offset, w, height)

    def show_configuration_dialog(self):
        if not os.path.exists(os.path.join(self.working_folder, "foreground.png")):
            warning_messagebox("No foreground image found", "No foreground image")
            return False

        return True

    def exec_(self):
        self.dialog.show()
        self.dialog.setFocus()

    def terminate(self):
        self.raspberry_pi.camera.close()
        self.app.activity_photobooth_terminate()

    def button_changed(self, value):
        if self.capturing:
            return

        self.capturing = True
        self.dialog.set_title("")

        now = datetime.datetime.now().strftime('%Y-%m-%d.%H-%M-%S.')

        self.dialog.set_title("")

        if not os.path.isdir(self.working_folder):
            os.mkdir(self.working_folder)

        photo_filepaths = list()
        photo_count = 1 if self.photo_mode == 'single' else 4
        for photo_index in range(photo_count):
            if photo_count > 1:
                self.dialog.set_title(f"Photo {photo_index + 1}")

            for seconds_left in range(5, 0, -1):
                self.dialog.set_message(f"{seconds_left}", 'message-large')
                time.sleep(1)

            self.dialog.set_title("Click !")
            self.dialog.set_message("")

            photo_filepath = os.path.join(self.working_folder, f"{now}-{photo_index}.jpg")
            self.raspberry_pi.camera.capture(photo_filepath)
            photo_filepaths.append(photo_filepath)

        self.dialog.set_title(f"Please wait...")

        uid = "".join(secrets.choice(string.ascii_lowercase) for i in range(8))

        url = f"{CLOUD_URL.strip('/')}/{uid}"
        qr_code_filepath = os.path.join(self.working_folder, QR_CODE_TEMP_FILENAME)
        make_qr_code(data=url, jpg_filepath=qr_code_filepath, draw_logo=False)

        foreground_filepath = os.path.join(self.working_folder, FOREGROUND)
        assembly_filepath = os.path.join(self.assembly_folder, now + "assembled_" + uid + '.jpg')
        assemble(photo_filepaths, foreground_filepath, assembly_filepath, self.photo_mode)

        if hasattr(os, "sync"):
            os.sync()

        # TODO: upload queue in a different thread (process ?)
        if self.cloud_upload_enabled:
            cloud = Cloud(CLOUD_CREDENTIALS_FILE)
            cloud.post(given_uid=uid, filepath=assembly_filepath)

        print_start_timestamp = time.time()
        print_time = 0

        if self.selphy_print_enabled:
            print_time += PRINT_TIME_SELPHY
            self.dialog.set_title(f"Printing...")
            self.raspberry_pi.print(assembly_filepath, PRINTER)

        if self.thermal_print_enabled:
            print_time += PRINT_TIME_THERMAL
            if self.cloud_upload_enabled:
                self.dialog.set_image(qr_code_filepath)
                self.dialog.set_title(f"Scan me !")
            else:
                self.dialog.set_title(f"Please wait...")

            thermal_print(self.raspberry_pi, ThermalPrintInfo(
                qr_code_filepath=os.path.join(self.working_folder, QR_CODE_TEMP_FILENAME),
                assembly_filepath=assembly_filepath,
                temp_output_filepath=os.path.join(self.working_folder, THERMAL_TEMP_FILENAME),
                uid=uid,
                is_print_image_enabled=self.thermal_print_image_enabled
            ))

        if self.selphy_print_enabled or self.thermal_print_enabled:
            time_left = print_time - int(time.time() - print_start_timestamp)
            if time_left > 0:
                for seconds_left in range(time_left, 0, -1):
                    if not self.thermal_print_enabled:
                        self.dialog.set_message(f"{seconds_left}", 'message-large')
                    time.sleep(1)

        self.reset()


def thermal_print(raspberry_pi: AbstractRaspberry, info: ThermalPrintInfo):
    if not info.is_print_image_enabled:
        raspberry_pi.thermal_print(info.qr_code_filepath)

    else:
        jpg = info.temp_output_filepath + ".jpg"

        photo = QPixmap(info.assembly_filepath)
        photo = photo.scaledToHeight(QR_CODE_SIZE, Qt.SmoothTransformation)
        padded_width = photo.width() + THERMAL_PADDING

        assembly = QPixmap(padded_width + QR_CODE_SIZE + THERMAL_UID_SIZE, QR_CODE_SIZE)
        assembly.fill(Qt.red)

        painter = QPainter()
        painter.setRenderHint(QPainter.Antialiasing)
        painter.begin(assembly)

        painter.drawPixmap(0, 0, photo)
        painter.drawPixmap(padded_width, 0, QPixmap(info.qr_code_filepath))

        painter.translate(padded_width + QR_CODE_SIZE + THERMAL_PADDING, assembly.height())
        painter.rotate(90)

        font = QFont("Arial", 32)
        painter.setFont(font)
        painter.drawText(0, 0, info.uid)

        painter.end()

        rotate_90 = QTransform()
        rotate_90.rotate(90)
        assembly = assembly.transformed(rotate_90)

        assembly.save(jpg, "jpg", 100)
        # raspberry_pi.thermal_print(jpg)
