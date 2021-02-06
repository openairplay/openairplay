#!/usr/bin/env python3

#  Copyright (C) 2015-2016 Ben Klein. All rights reserved.
#
#  This application is licensed under the GNU GPLv3 License, included with
#  this application source.

import sys

global DEBUG
DEBUG = True

if __name__ == '__main__':
    print("Use main.py instead.")
    sys.exit();

# Qt GUI stuff
try:
    from PyQt5 import QtCore, QtGui
    from PyQt5.QtCore import QSettings
except ImportError:
    print("There was an error importing the Qt python3 libraries,")
    print("These are required by to operate this program.")
    print("If you are on Ubuntu/Debian, they should be available via APT.")
    sys.exit("Could not import Python3 Qt Libraries.")


class AirplayDevice():
    def __init__():
        print("")
