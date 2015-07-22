
## These are the packages which you may need installed to use this program.

Python 3: `PyQt4`[supplies the Qt framework for the GUI]

Ubuntu Packages: `libavahi-compat-libdnssd-dev`[supplies dns_sd headers for Ruby Gem `dnssd`]

Ruby:  `airplay`[this requires multiple other Ruby Gems, installed automatically]

Install Instructions:
===
Ubuntu:
---
Ruby airplay dnssd:  
`sudo apt-get install libavahi-compat-libdnssd-dev ruby rubygems-integration`
Python 3 Qt Libraries:  
`sudo apt-get install python3 python3-pyqt4 python3-qt4`  

Ruby Airplay gem dependencies:  
`sudo gem install airplay dnssd`

Now you should be able to run `python3 main.py` to start the program.
