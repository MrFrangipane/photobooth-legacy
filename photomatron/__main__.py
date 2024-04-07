import argparse
import logging

from photomatron.application import Application


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mock', '-m', action='store_true')
    parser.add_argument('--photobooth-working-folder', '-f', required=True)
    parser.add_argument('--css-editor', '-c', action='store_true')
    return parser.parse_args()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    args = parse_args()

    if args.mock:
        from photomatron.hardware.mock import Mock
        raspberry_pi = Mock()
    else:
        from photomatron.hardware.raspberry import Raspberry
        raspberry_pi = Raspberry()

    app = Application(raspberry_pi, args.photobooth_working_folder)

    if args.css_editor:
        from guibedos.css.editor import CSSEditor
        editor = CSSEditor("Photomatron")

    app.exec_()
