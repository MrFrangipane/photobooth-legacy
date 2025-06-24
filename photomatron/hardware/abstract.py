

class AbstractRaspberry:

    @property
    def wifi_status(self):
        raise NotImplementedError

    @property
    def cpu_temperature(self):
        raise NotImplementedError

    @property
    def available_disk_space(self):
        raise NotImplementedError

    def print(self, filepath, printer_name):
        raise NotImplementedError

    def thermal_print(self, data, double_size=False):
        raise NotImplementedError

    def reboot(self):
        raise NotImplementedError

    def shutdown(self):
        raise NotImplementedError

    def renew_dhcp(self):
        raise NotImplementedError

    def post_qapp(self, app):
        """app is the Application, not the QApplication"""
        raise NotImplementedError

    def empty_print_queue(self):
        raise NotImplementedError
