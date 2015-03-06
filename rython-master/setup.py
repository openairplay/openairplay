import distribute_setup
from setuptools import setup, find_packages
import sys
import os
extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True

setup(
    name="rython",
    packages=["rython"],
    version="0.0.2",
    license="BSD",
    author="Matt Pizzimenti",
    author_email="mjpizz+rython@gmail.com",
    url="http://pypi.python.org/pypi/rython/",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Ruby",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Topic :: Software Development",
        "Topic :: Software Development :: Object Brokering",
        "Topic :: Software Development :: Libraries :: Ruby Modules",
    ],
    description="rython transparently mixes Ruby code into Python",
    long_description=open(os.path.join(os.path.dirname(__file__), "README.txt")).read(),
    **extra
    )
