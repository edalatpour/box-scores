# Tim Edalatpour 2023-04-27
#!/usr/bin/env python3
import datetime
import time
import sys

import clublocker as cl
import ip

try:
    import unicorn as d
except ImportError:
    import console as d


rotation = 0

if len(sys.argv) > 1:
    try:
        rotation = int(sys.argv[1])
    except ValueError:
        print("Usage: {} <rotation>".format(sys.argv[0]))
        sys.exit(1)

ipaddr = ip.getAddress()
d.writeLine(ipaddr)

while True:

    try:

        matches = cl.getMatches()

        for match in matches:

            if 'ResultId' in match:
                text = cl.getText(match)
                d.writeLine(text)

    except BaseException as err:
        text = err
        d.writeLine(text)
        #time.sleep(30)
