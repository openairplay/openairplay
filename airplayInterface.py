#!/usr/bin/env python3

import subprocess

def getAirDevices():
    try:
        rawStringOutput = subprocess.check_output("ruby airplay/air list", shell=True)
    except Exception as ErrorDetail:
        rawStringOutput = ErrorDetail.output
    #TODO Get sample output from the call and format it into a python list of devices
    devicelist = rawStringOutput.decode(encoding='UTF-8').split('\n')
    print(devicelist)

def sendAirImage(imageFile, device = None):
    if imageFile is None: raise ValueError # If the imageFile is none, it's not a valid Value.
    if device is None: raise ValueError # We need to know where to send the image.
    #TODO Set up image sending
    # use: 'ruby airplay/air view test.jpg [--device <deviceName>]'
    raise NotImplementedError
