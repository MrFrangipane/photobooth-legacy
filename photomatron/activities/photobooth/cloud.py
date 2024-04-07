import logging
import os.path
import json

import requests


_logger = logging.getLogger(__name__)


class Cloud:

    def __init__(self, credentials_file):
        if not os.path.isfile(credentials_file):
            _logger.warning(f"Could not find credentials file : {credentials_file}")
            self.connected = False

        else:
            with open(credentials_file, 'r') as file_credentials:
                credentials = json.load(file_credentials)
                self._base_url = credentials['url'].strip('/') + '/'

                self.session = requests.Session()
                self.session.auth = (credentials['user'], credentials['password'])
            self.connected = True

    def post(self, given_uid, filepath) -> None:
        if not self.connected:
            _logger.warning(f"Not connected")
            return

        if not os.path.isfile(filepath):
            _logger.warning(f"{filepath} is not a file")
            return

        self.session.post(
            url=self._base_url,
            files={'media': open(filepath, 'rb')},
            data={"given_uid": given_uid},
            headers={'Connection': 'close'}
        )
