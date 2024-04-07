

class WifiStatus:
    CONNECTED = 'CONNECTED'
    DISCONNECTED = 'DISCONNECTED'
    ERROR = 'ERROR'

    def __init__(self, status, ssid="", message="", ip_address=""):
        self.status = status
        self.ssid = ssid
        self.message = message
        self.ip_address = ip_address

    def __repr__(self):
        return f'<{self.__class__.__name__}(status={self.status}, ssid="{self.ssid}")>'
