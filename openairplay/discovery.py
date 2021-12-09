#!/usr/bin/env python3

import sys
try:
    import zeroconf
except ImportError:
    print("Python3 Zeroconf module could not be loaded.")
    print("Please ensure you have it installed.")
    sys.exit("Could not find zeroconf.")

global airplayReceivers
airplayReceivers = []

global discoveryStarted
discoveryStarted = False

global DEBUG
DEBUG = True

browser = None

class AirplayListener(object):

    def remove_service(self, zeroconf, type, name):
        airplayReceivers.remove(name)
        print("Airplay receiver %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        airplayReceivers.append(name)
        if DEBUG:
            print("Airplay receiver %s added, service info: %s" % (name, info))

# Start the listener
def start():
    ZC = zeroconf.Zeroconf()
    listener = AirplayListener()
    browser = zeroconf.ServiceBrowser(ZC, "_airplay._tcp.local.", listener)
    started = True
    if DEBUG:
        print("Listener started.")

# To stop it:
def stop():
    if (browser is not None) or (discoveryStarted is True):
        ZC.close()
        del listener
        del browser
        del ZC
        discoveryStarted = False
        if DEBUG:
            print("Listener stopped.")
    else:
        print("WARN: discovery.stop() called but not running")
