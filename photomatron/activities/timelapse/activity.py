import os

from .ui import TimelapseActivityDialog
from photomatron.ui.timer import Timer

OUTPUT_DIR = './timelapse'
COUNTER = '.counter'


class TimelapseActivity:

    def __init__(self, app, raspberry_pi, parent_window):
        self.raspberry_pi = raspberry_pi
        self.raspberry_pi.camera.init_cam()
        self.raspberry_pi.camera.start_preview()

        self.dialog = TimelapseActivityDialog(activity=self, parent=parent_window)
        self.timer = Timer(interval=10, callback=self.capture)

        self.app = app
        self.capturing = False
        self.reset()
        self.timer.start()

    def reset(self):
        self.capturing = False
        self.dialog.set_title("Timelapse")
        self.dialog.set_message("[paused]")

    def update_camera_placeholder(self, x, y, w, h):
        self.raspberry_pi.camera.set_geometry(x, y, w, h)

    def exec_(self):
        self.dialog.show()

    def capture(self):
        if self.capturing:
            if not os.path.isdir(OUTPUT_DIR):
                os.mkdir(OUTPUT_DIR)

            counter_filepath = os.path.join(OUTPUT_DIR, COUNTER)
            if not os.path.isfile(counter_filepath):
                with open(counter_filepath, 'w+') as counter_file:
                    counter_file.write("0")
                    counter = 0
            else:
                with open(counter_filepath, 'r') as counter_file:
                    counter = int(counter_file.read())

            photo = os.path.join(OUTPUT_DIR, f'{counter:06d}.jpg')
            self.raspberry_pi.camera.capture(photo)

            counter += 1
            with open(counter_filepath, 'w+') as counter_file:
                counter_file.write(str(counter))

    def terminate(self):
        self.timer.stop()
        self.raspberry_pi.camera.close()
        self.app.activity_timelapse_terminate()

    def button_changed(self, value):
        if not value:
            return

        self.capturing = not self.capturing
        self.dialog.set_message(["[paused]", "[capturing]"][self.capturing])
