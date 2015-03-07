Python 2/3: `PyQt4`[supplies the Qt framework for the GUI]

Ubuntu Packages: `libavahi-compat-libdnssd-dev`[supplies dns_sd headers for Ruby Gem `dnssd`]

Ruby:  `airplay`[this requires multiple other Ruby Gems, installed automatically]

Install Instructions:
===
Ubuntu:
---
Install packages needed:  
`sudo apt-get install libavahi-compat-libdnssd-dev ruby rubygems-integration`  
Python 2:  
`sudo apt-get install python python-qt4`  
Python 3:  
`sudo apt-get install python3 python3-pyqt4 python3-qt4`  

Now for the Ruby dependencies:  
`sudo gem install airplay dnssd`
