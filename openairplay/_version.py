#!/usr/bin/env python3

import sys

__version__ = "0.0.33"

MIN_PYTHON = (3, 5)

if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)
