import time
import picamera


CAPTURE_RESOLUTION = 1700, 1130
FRAMERATE = 40
CAPTURE_SLEEP = .2
OVER_SATURATION = 0  # 25
OVER_BRIGHTNESS = 4  # 8


class Camera:

    def __init__(self):
        self.camera = None
        self.init_cam()
        self._geometry = 0, 0, 1, 1

    def init_cam(self):
        try:
            self.camera = picamera.PiCamera()
            self.camera.resolution = CAPTURE_RESOLUTION
            self.camera.framerate = FRAMERATE
            self.camera.hflip = True

            self.camera.awb_mode = 'fluorescent'
            self.camera.iso = 0
            self.camera.exposure_mode = 'sports'

        except picamera.exc.PiCameraMMALError:
            print("Camera already in use !")

    def start_preview(self):
        if self.camera.preview is None:
            self.camera.start_preview(fullscreen=False)

    def set_geometry(self, x, y, width, height):
        self._geometry = x, y, width, height
        self.camera.preview.window = x, y, width, height

    def capture(self, filepath):
        time.sleep(CAPTURE_SLEEP)
        self.camera.saturation = min(100, self.camera.saturation + OVER_SATURATION)
        self.camera.brightness = min(100, self.camera.brightness + OVER_BRIGHTNESS)

        self.camera.capture(filepath)
        self.camera.close()

        self.init_cam()
        self.start_preview()
        self.camera.preview.window = self._geometry

    def close(self):
        self.camera.close()
