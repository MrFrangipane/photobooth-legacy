import argparse
import logging
import os.path
import json
from copy import copy

from photomatron.application import Application
from photomatron.activities.photobooth.activity import PhotoboothConfiguration


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mock', '-m', action='store_true')
    parser.add_argument('--photobooth-working-folder', '-f', required=True)
    parser.add_argument('--css-editor', '-c', action='store_true')
    return parser.parse_args()


def load_configuration(photobooth_working_folder) -> PhotoboothConfiguration:
    configuration_filepath = os.path.join(photobooth_working_folder, 'configuration.json')
    configuration_default = {
        'photo-mode': 'single',  # or 'quad'
        'cloud-upload-enabled': True,
        'selphy-print-enabled': False,
        'thermal-print-enabled': True,
        'thermal-print-image-enabled': True
    }
    if not os.path.isfile(configuration_filepath):
        with open(configuration_filepath, 'w') as configuration_file:
            json.dump(configuration_default, configuration_file, indent=2)
            print("Written default configuration to", configuration_filepath)

    with open(configuration_filepath, 'r') as configuration_file:
        loaded_config = json.load(configuration_file)
        print("Loaded configuration from", configuration_filepath)

    configuration = PhotoboothConfiguration()
    configuration.photo_mode = loaded_config['photo-mode']
    configuration.cloud_upload_enabled = loaded_config['cloud-upload-enabled']
    configuration.selphy_print_enabled = loaded_config['selphy-print-enabled']
    configuration.thermal_print_enabled = loaded_config['thermal-print-enabled']
    configuration.thermal_print_image_enabled = loaded_config['thermal-print-image-enabled']

    if configuration.photo_mode not in ('single', 'quad'):
        raise ValueError("Photo mode must be 'single' or 'quad', check config file")

    print("Loaded configuration is")
    print(json.dumps(vars(configuration), indent=2))

    return configuration


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    args = parse_args()
    configuration = load_configuration(args.photobooth_working_folder)

    if args.mock:
        from photomatron.hardware.mock import Mock
        raspberry_pi = Mock()
    else:
        from photomatron.hardware.raspberry import Raspberry
        raspberry_pi = Raspberry(configuration.photo_mode)

    app = Application(raspberry_pi, args.photobooth_working_folder, configuration)

    if args.css_editor:
        from guibedos.css.editor import CSSEditor
        editor = CSSEditor("Photomatron")

    app.exec_()
