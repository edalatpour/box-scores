# Tim Edalatpour 2023-04-27
#!/usr/bin/env python3
import datetime
import time
import sys

import json
import requests
import ip
import display


def getMatches():

    boxId = '7915'
    response = requests.get("https://api.ussquash.com/resources/res/box_leagues/{0}/results".format(boxId))
    # print(response)
    matches = json.loads(response.text)
    # print(matches)
    return(matches)


def getText(match):

    text = ''

    if 'ResultId' in match:
        resultId = match['ResultId']
        wPlayerName = match['wPlayerName1'].replace('  ',' ')
        oPlayerName = match['oPlayerName1'].replace('  ',' ')
        matchStatus = match['status']
        matchDate = match['MatchDate']
        score = match['score']

        if matchStatus == 'C':
            text = '{0}: {1} def {2} ({3})'.format(matchDate, wPlayerName, oPlayerName, score)
        else:
            text = '{0}: {1} vs {2} ({3})'.format(matchDate, wPlayerName, oPlayerName, score)

        return(text)


rotation = 0

if len(sys.argv) > 1:
    try:
        rotation = int(sys.argv[1])
    except ValueError:
        print("Usage: {} <rotation>".format(sys.argv[0]))
        sys.exit(1)

display.init(rotation)

ipaddr = ip.getAddress()
display.writeLine(ipaddr)

while True:

    try:

        matchIndex = 0

        matches = getMatches()

        while True:

            match = matches[matchIndex]
            #print(match)

            if 'ResultId' in match:
                text = getText(match)
                display.writeLine(text)

            matchIndex = matchIndex + 1

            if matchIndex == len(matches):
                matchIndex = 0

    except BaseException as err:
        text = err
        display.writeLine(text)
        time.sleep(30)
