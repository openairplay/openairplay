#!/usr/bin/env python

from setuptools import setup, find_packages

from openairplay._version import __version__

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="OpenAirplay",
    version=__version__,
    description="Open source implementation of Apple's Airplay Client",
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3 :: Only",
    ],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='airplay apple',
    author='Ben Klein',
    author_email='robobenklein@gmail.com',
    url='https://github.com/openairplay/openairplay',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests', 'vendor', 'venv']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "coloredlogs",
        "Pebble",
        "bpython",
        "zeroconf",
        "PyQt5",
    ],
    entry_points={
        'console_scripts': [
            'openairplay=openairplay.gui_main:__main__',
        ]
    },
    python_requires='>=3.5'
)
