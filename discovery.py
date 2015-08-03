#!/usr/bin/env python3

import sys
import zeroconf

global airplayReceivers
airplayReceivers = []

global discoveryStarted
discoveryStarted = False

class AirplayListener(object):

    def remove_service(self, zeroconf, type, name):
        airplayReceivers.remove(name)
        print("Airplay receiver %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        airplayReceivers.append(name)
        print("Airplay receiver %s added, service info: %s" % (name, info))

# Start the listener
def start():
    ZC = zeroconf.Zeroconf()
    listener = AirplayListener()
    browser = zeroconf.ServiceBrowser(ZC, "_airplay._tcp.local.", listener)
    started = True

# To stop it:
def stop():
    if (browser is not None) or (discoveryStarted is True):
        ZC.close()
        del listener
        del browser
        del ZC
        discoveryStarted = False
    else:
        print("WARN: discovery.stop() called but not running")
