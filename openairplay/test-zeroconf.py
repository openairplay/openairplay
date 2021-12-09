#!/usr/bin/env python3

from six.moves import input
from zeroconf import ServiceBrowser, Zeroconf

class MyListener(object):

    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        print("Service %s added, service info: %s" % (name, info))


zeroconf = Zeroconf()
listener = MyListener()
browser = ServiceBrowser(zeroconf, "_tcp.", listener)

try:
    input("Press enter to exit...\n\n")
finally:
    zeroconf.close()
