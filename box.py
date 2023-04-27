import datetime
import time
import sys

from colorsys import hsv_to_rgb

from PIL import Image, ImageDraw, ImageFont
from unicornhatmini import UnicornHATMini

import json
import requests

import socket
testIP = "8.8.8.8"
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((testIP, 0))
ipaddr = s.getsockname()[0]
host = socket.gethostname()
print ("IP:", ipaddr, " Host:", host)

#color = 0, 255, 16
color = 0, 255, 0

def getMatches():

#    boxId = '7829'
    boxId = '7915'

    today = datetime.datetime.now()
    dateString = today.strftime('%Y-%m-%d')

    if len(sys.argv) > 2:
        dateString = sys.argv[2]
    #print(dateString)

    # response = requests.get("https://api.ussquash.com/resources/res/trn/live_matrix?date={0}&tournamentId={1}".format(dateString, tournamentId))
    response = requests.get("https://api.ussquash.com/resources/res/box_leagues/{0}/results".format(boxId))
    # print(response)
    matches = json.loads(response.text)
    # print (matches)
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


def drawImage(text):

    # Load a nice 5x7 pixel font
    # Granted it's actually 5x8 for some reason :| but that doesn't matter
    font = ImageFont.truetype("5x7.ttf", 8)
    
    # Measure the size of our text, we only really care about the width for the moment
    # but we could do line-by-line scroll if we used the height
    text_width, text_height = font.getsize(text)
    
    # Create a new PIL image big enough to fit the text
    image = Image.new('P', (text_width + display_width + display_width, display_height), 0)
    draw = ImageDraw.Draw(image)
    
    # Draw the text into the image
    draw.text((display_width, -1), text, font=font, fill=255)

    return(image)


rotation = 0
if len(sys.argv) > 1:
    try:
        rotation = int(sys.argv[1])
    except ValueError:
        print("Usage: {} <rotation>".format(sys.argv[0]))
        sys.exit(1)

unicornhatmini = UnicornHATMini()
unicornhatmini.set_rotation(rotation)
display_width, display_height = unicornhatmini.get_shape()

print("{}x{}".format(display_width, display_height))

# Do not look at unicornhatmini with remaining eye
unicornhatmini.set_brightness(0.04)

while True:

    matchIndex = 0

    try:
        matches = getMatches()
    except:
        matches = None

    while True:

        try:
            # matches = getMatches()
            match = matches[matchIndex]
        except:
            # matches = None
            match = None
        #print(matchIndex)
        
        if 'ResultId' in match:
            #print(match)
            try:
                text = getText(match)
                print(text)
            except BaseException as err:
                text = err
            image = drawImage(text)

            status = match['status']

#            if status == 'C':
#                color = 255, 0, 0
#            elif status == 'S':
#                color = 0, 255, 0
#            else:
#                color = 255, 255, 255

            offset_x = 0

            while offset_x + display_width < image.size[0]:

                for y in range(display_height):
                    for x in range(display_width):
                        hue = (time.time() / 10.0) + (x / float(display_width * 2))
                        #r, g, b = [int(c * 255) for c in hsv_to_rgb(hue, 1.0, 1.0)]
                        r, g, b = color
                        if image.getpixel((x + offset_x, y)) == 255:
                            unicornhatmini.set_pixel(x, y, r, g, b)
                        else:
                            unicornhatmini.set_pixel(x, y, 0, 0, 0)

                offset_x += 1
    #        if offset_x + display_width > image.size[0]:
    #            offset_x = 0

                unicornhatmini.show()
                time.sleep(0.05)

        matchIndex = matchIndex + 1
        if matchIndex == len(matches):
            matchIndex = 0
