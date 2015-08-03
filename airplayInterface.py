#!/usr/bin/env python3

import sys
from subprocess import Popen, PIPE, STDOUT # Using pipes to pass commands to the Ruby Script

# Import the right version of rython, 2 or 3
#if sys.version_info >= (3, 3):
#    import rython3 as rython
#    print("Using Rython3: " + str(sys.version_info))
#elif sys.version_info >= (2, 7):
#    import rython2 as rython
#    print("Using Rython2: " + str(sys.version_info))
#else: sys.exit("This program requires Python 2.7+ or 3.3+, please install either of those versions.")

# Set up our Ruby process to send commands to
slave = Popen(['ruby', 'airplayInterface.rb'], stdin=PIPE, stdout=PIPE, stderr=STDOUT)

def rubyParse(command):
    inputCommand = command + "\n"
    slave.stdin.write(inputCommand.encode('utf-8'))
    result = []
    while True:
        # read one line, remove newline chars and trailing spaces:
        line = slave.stdout.readline().rstrip()
        #if len(line) > 0:
        #    print 'line:', line
        if "[end]" in line:
            break
        result.append(line)
    return(result)

if __name__ == '__main__':
    print("Performing Tests...")
    print("List devices: Airplay::CLI.method(:list)")
    print(rubyParse("Airplay::CLI.method(:list)"))
    print("Test complete.")
