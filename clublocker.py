#This module contains code for interacting with the ClubLocker APIs

import json
import requests


def getMatches():

    boxId = '7915'
    response = requests.get("https://api.ussquash.com/resources/res/box_leagues/{0}/results".format(boxId))
    # print(response)
    matches = json.loads(response.text)
    # print(matches)
    return(matches)


def getText(match):

    text = ''

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

