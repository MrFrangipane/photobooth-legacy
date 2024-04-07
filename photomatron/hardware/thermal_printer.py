import os.path

from PIL import Image
from thermalprinter import ThermalPrinter


def print_(data, double_size=False):
    with ThermalPrinter(port='/dev/serial0', heat_interval=40, most_heated_point=10) as printer:
        if os.path.isfile(data):
            printer.image(Image.open(data))

        else:
            printer.out(data, double_height=double_size, double_width=double_size)


def feed(line_count):
    with ThermalPrinter(port='/dev/serial0') as printer:
        printer.feed(line_count)
