import os.path
import subprocess


def print_(data, double_size=False):
    if os.path.isfile(data):
        subprocess.check_call([
            "lp", "-d", "ThermalPrinter", "-o", "fit-to-page", data
        ])

    else:
        subprocess.check_call([
            "echo", f'"{data}"', "|", "lp", "-d", "ThermalPrinter"
        ])


def feed(line_count):
    subprocess.check_call([
        "echo", '""', "|", "lp", "-d", "ThermalPrinter"
    ])
