#!/usr/bin/env python3

import sys
try:
    import zeroconf
except ImportError:
    print("Python3 Zeroconf module could not be loaded.")
    print("Please ensure you have it installed.")
    sys.exit("Could not find zeroconf.")

from PyQt5.QtCore import QObject, pyqtSignal

from . import log, utils
from .receiver_device import AirplayReceiver, AirplayFeatures


# global airplayReceivers
# airplayReceivers = []
#
# global discoveryStarted
# discoveryStarted = False

# global DEBUG
# DEBUG = True

# browser = None

class AirplayServiceListener(QObject):
    receiver_added = pyqtSignal([AirplayReceiver])
    receiver_removed = pyqtSignal([AirplayReceiver])

    def __init__(self):
        self.ZC = zeroconf.Zeroconf()
        self.browser = zeroconf.ServiceBrowser(self.ZC, "_airplay._tcp.local.", self)
        self.devices = {}

        super().__init__()

    def remove_service(self, zeroconf, type, name):
        # airplayReceivers.remove(name)
        if name not in self.devices:
            log.warn(f"Device '{name}' not known, cannot remove service.")
            return
        log.debug(f"Airplay receiver '{name}' removed")
        self.receiver_removed.emit(self.devices[name])
        self.devices[name] = None # permit other references to persist

    def add_service(self, zeroconf, type, name):
        log.debug(f"Adding device '{name}' ...")
        info = zeroconf.get_service_info(type, name)
        # airplayReceivers.append(name)
        self.devices[name] = AirplayReceiver(
            name, info,
            # **{k.decode(): v.decode() for k, v in info.properties.items()}
        )
        log.debug(f"Airplay receiver '{name}' added, constructed: {self.devices[name]}")
        self.receiver_added.emit(self.devices[name])

        log.debug(f"Receiver addresses: {self.devices[name]._get_ip_addresses()}")

    def update_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        if name not in self.devices:
            log.warn(f"Device '{name}' not known, cannot update service.")
            return
        self.devices[name].update_service_info(info)
        log.debug(f"Airplay receiver '{name}' service updated: {self.devices[name]}")

    def quit(self):
        self.ZC.close()
        log.debug("Closed ZC browser")
