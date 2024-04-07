import datetime
import os.path
import time
import secrets
import string

from PySide2.QtGui import QPixmap, QTransform
from PySide2.QtCore import Qt

from photomatron.hardware.types_ import WifiStatus

from .activity_dialog import PhotoboothActivityDialog
from .configuration_dialog import PhotoboothConfigurationDialog
from .assembly import assemble
from .qrcode_maker import make_qr_code
from .cloud import Cloud
from photomatron.ui.extensions import warning_messagebox


PRINTER = "Canon_SELPHY_CP1300"
FOREGROUND = 'foreground.png'
PRINT_TIME = 80
QR_CODE_TEMP_FILENAME = "qr-code-temp.jpg"
THERMAL_TEMP_FILENAME = "termal-temp.jpg"
MANUAL_URL = "photobooth.frangitron.com"
CLOUD_URL = f"https://{MANUAL_URL}/retrieve"
CLOUD_CREDENTIALS_FILE = os.path.dirname(__file__) + '/cloud-credentials.json'


class PhotoboothActivity:

    def __init__(self, app, raspberry_pi, parent_window, working_folder):
        self.raspberry_pi = raspberry_pi
        self.raspberry_pi.camera.init_cam()
        self.raspberry_pi.camera.start_preview()

        self.working_folder = working_folder

        self.cloud_upload_enabled = True
        self.selphy_print_enabled = False
        self.thermal_print_enabled = True
        self.thermal_print_image_enabled = True

        self.dialog = PhotoboothActivityDialog(activity=self, parent=parent_window)
        self.configuration_dialog = PhotoboothConfigurationDialog(activity=self, parent=parent_window)

        self.app = app
        self.capturing = False

        self.reset()

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

        for seconds_left in range(5, 0, -1):
            self.dialog.set_message(f"{seconds_left}", 'message-large')
            time.sleep(1)

        self.dialog.set_title("Click !")
        self.dialog.set_message("")

        if not os.path.isdir(self.working_folder):
            os.mkdir(self.working_folder)

        photo_filepath = os.path.join(self.working_folder, now + '.jpg')
        self.raspberry_pi.camera.capture(photo_filepath)

        self.dialog.set_title(f"Please wait...")

        uid = "".join(secrets.choice(string.ascii_lowercase) for i in range(8))
        foreground_filepath = os.path.join(self.working_folder, FOREGROUND)
        assembly_filepath = os.path.join(self.working_folder, now + "assembled_" + uid + '.jpg')
        assemble(photo_filepath, foreground_filepath, assembly_filepath)

        if hasattr(os, "sync"):
            os.sync()

        # TODO: upload queue in a different thread (process ?)
        if self.cloud_upload_enabled:
            cloud = Cloud(CLOUD_CREDENTIALS_FILE)
            cloud.post(
                given_uid=uid,
                filepath=assembly_filepath
            )

        if self.selphy_print_enabled:
            print_start_timestamp = time.time()
            self.dialog.set_title(f"Printing...")
            self.raspberry_pi.print(assembly_filepath, PRINTER)

        if self.thermal_print_enabled:
            url = f"{CLOUD_URL.strip('/')}/{uid}"
            make_qr_code(
                data=url,
                jpg_filepath=os.path.join(self.working_folder, QR_CODE_TEMP_FILENAME),
                draw_logo=False
            )
            self.raspberry_pi.thermal_print(os.path.join(self.working_folder, QR_CODE_TEMP_FILENAME))
            self.raspberry_pi.thermal_print(1)
            self.raspberry_pi.thermal_print(uid, double_size=True)
            self.raspberry_pi.thermal_print(MANUAL_URL)
            self.raspberry_pi.thermal_print(1)

            if self.thermal_print_image_enabled:
                assembly = QPixmap(assembly_filepath)
                rotate_90 = QTransform()
                rotate_90.rotate(90)
                assembly = assembly.transformed(rotate_90)
                assembly = assembly.scaledToWidth(384, Qt.SmoothTransformation)
                assembly.save(os.path.join(self.working_folder, THERMAL_TEMP_FILENAME), "jpg", 100)

                self.raspberry_pi.thermal_print(os.path.join(self.working_folder, THERMAL_TEMP_FILENAME))

            self.raspberry_pi.thermal_print(2)
            self.raspberry_pi.thermal_print("by Frangitron")
            self.raspberry_pi.thermal_print(4)

        if self.selphy_print_enabled:
            time_left = PRINT_TIME - int(time.time() - print_start_timestamp)
            if time_left > 0:
                for seconds_left in range(time_left, 0, -1):
                    self.dialog.set_message(f"{seconds_left}", 'message-large')
                    time.sleep(1)

        self.reset()
