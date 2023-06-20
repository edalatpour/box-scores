#This module contains code for interacting with the ClubLocker APIs

import json
import requests

def getBoxId():

    boxId = 0

    # get latest boxid from DynamoDB table
    response = requests.get("https://api.ussquash.com/resources/res/box_leagues/list?Status=1&TopRecords=50&clubId=492")
    # print(response)
    boxes = json.loads(response.text)
    # interate over boxIds to find the latest
    for box in boxes:
        if box['eventId'] > boxId:
            boxId = box['eventId']

    return(boxId)

def getMatches():

    boxId = getBoxId()
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

