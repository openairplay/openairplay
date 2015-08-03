#!/usr/bin/env python3

import sys
import zeroconf

global airplayReceivers
airplayReceivers = []

global started = False

class MyListener(object):

    def remove_service(self, zeroconf, type, name):
        airplayReceivers.remove(name)
        print("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        airplayReceivers.append(name)
        print("Service %s added, service info: %s" % (name, info))

# Start the listener
def start(self):
    ZC = zeroconf.Zeroconf()
    listener = AirplayListener()
    browser = zeroconf.ServiceBrowser(ZC, "_airplay._tcp.local.", listener)
    started = True

# To stop it:
def stop(self):
    if (browser is not None) or (started = True):
        ZC.close()
        del listener
        del browser
        del ZC
        started = False
    else:
        print("WARN: discovery.stop() called but not running")
