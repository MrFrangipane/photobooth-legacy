import time
from RPi import GPIO


class ButtonsState:
    def __init__(self):
        self.left = False
        self.center = False
        self.right = False
        self.led = False

    def __eq__(self, other):
        return self.left == other.left and self.center == other.center and self.right == other.right

    def __repr__(self):
        return "<{}(left={}, center={}, right={}, led={})>".format(
            self.__class__.__name__,
            self.left,
            self.center,
            self.right,
            self.led
        )


class Buttons:
    LEFT = 'LEFT'
    CENTER = 'CENTER'
    RIGHT = 'RIGHT'

    GPIO_GROUND = 34
    GPIO_BUTTON_LEFT = 38
    GPIO_BUTTON_CENTER = 35
    GPIO_BUTTON_RIGHT = 37
    GPIO_LED = 36
    INTERVAL = 0.02

    def __init__(self):
        self.parent = None

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.GPIO_BUTTON_LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.GPIO_BUTTON_CENTER, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.GPIO_BUTTON_RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.GPIO_LED, GPIO.OUT, initial=GPIO.LOW)

        self.previous_state = ButtonsState()

        self.is_running = False

    def state(self):
        state = ButtonsState()
        state.left = GPIO.input(self.GPIO_BUTTON_LEFT) == GPIO.LOW
        state.center = GPIO.input(self.GPIO_BUTTON_CENTER) == GPIO.LOW
        state.right = GPIO.input(self.GPIO_BUTTON_RIGHT) == GPIO.LOW
        state.led = GPIO.input(self.GPIO_LED) == GPIO.HIGH
        return state

    def exec_(self):
        self.is_running = True

        assert hasattr(self.parent, 'changed_')

        while self.is_running:

            time.sleep(self.INTERVAL)
            try:
                state = self.state()
            except RuntimeError as e:
                break

            if self.previous_state.left != state.left:
                self.previous_state.left = state.left
                self.parent.changed_(self.LEFT, state.left)

            if self.previous_state.center != state.center:
                self.previous_state.center = state.center
                self.parent.changed_(self.CENTER, state.center)

            if self.previous_state.right != state.right:
                self.previous_state.right = state.right
                self.parent.changed_(self.RIGHT, state.right)

    def stop(self):
        self.is_running = False

    def set_led(self, status):
        GPIO.output(self.GPIO_LED, GPIO.HIGH if status else GPIO.LOW)

    def cleanup(self):
        GPIO.cleanup()
