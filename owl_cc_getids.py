# Slightly changed version of Benjis Gist https://gist.github.com/Benjins/ae2535d28008a224686f2ce005c47b0d to suit my script.


# This script lists the various streams that OWL All-Access Pass viewers can tune into. This info can be
# plugged into Streamlink, etc. to archive one's own VODs of the games.
#
#   Output is of the form `Login: "{LOGIN_ID}"  (display: "{DISPLAY}") (type: "{TYPE_DESCRIPTION}") (player: "{PLAYER_NAME}")`
#
# The {LOGIN_ID} is the replacement for a Twitch username that you can feed into streamlink
# For instance, if the login is {LOGIN_ID}, you should run
#     `streamlink https://www.twitch.tv/{LOGIN_ID} ...`
# to download that perspective.
#
# There are a couple variations of each player: POV is just their view, Composite also has some other info
# There's also the main stream (which probably isn't worth archiving, since it's what's in the normal stream and the VODs),
# and also the "Map" stream that is a 3rd person view w/ some extra info/icons overlayed (this view is sometimes cut away to in the main stream)
#
# Which id's correspond to which view seems to be shuffled after each match (but not each game or map), so for a duration of two teams playing
# The same id will be the same player.
# Still, a lot that's not clear or may be change by Twitch/OWL

# NOTE: None of this is intended to circumvent OWL All-Access Pass.
# This is just to allow folks who may not be able to catch the whole game live to view POV's offline
#
# No information here was obtained by observing the Twitch Player source code, just by looking at external outputs and side-effects,
# and a healthy dose of cURL trial-and-error
#
# Finally, of course a lot of this may change. There are some bugs in the player, and Twitch/OWL may break this script or the compatibility w/ streamlink.
# They are not under any obligation to test their changes against some random gist on GitHub. :p

# I think this requires Python 3? Idk.

import json
import http.client

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'

# Not anything private, seems to be shared among all desktop users at least
CLIENT_ID = 'jzkbprff40iqj646a697cyrvl0zt2m6'


def GetGQLInfo():
    conn = http.client.HTTPSConnection("gql.twitch.tv")

    postData = [{"operationName": "MultiviewGetChanletDetails", "variables": {"channelLogin": "overwatchleague"},
                 "extensions": {"persistedQuery": {"version": 1,
                                                   "sha256Hash": "23e36d2b3a68dcb2f634dd5d7682e3a918a5598f63ad3a6415a6df602e3f7447"}}}]

    postDataStr = json.dumps(postData)

    headers = {}
    headers['Content-Type'] = 'text/plain;charset=UTF-8'
    headers['User-Agent'] = USER_AGENT
    headers['Referer'] = 'https://www.twitch.tv/overwatchleague/commandcenter'
    headers['Client-Id'] = CLIENT_ID
    conn.request("POST", '/gql', postDataStr, headers=headers)

    res = conn.getresponse()
    if res is not None and res.status == 200:
        info = json.loads(res.read().decode('utf-8'))
        conn.close()
        return info
    elif res is not None:
        print('Error on requesting GQL, status = %d' % res.status)
        print('Got: "%s"' % res.read().decode('utf-8'))
        conn.close()
        return None
    else:
        print('?????')
        conn.close()
        return None


gqlInfo = GetGQLInfo()

login = []
displayName = []
streamType = []
playerName = []

if gqlInfo is None:
    print('Problem...')
else:
    for chanlet in gqlInfo[0]['data']['user']['channel']['chanlets']:
        login.append(chanlet['owner']['login'])

        for attrib in chanlet['contentAttributes']:
            if attrib['key'] == 'displayTitle':
                displayName.append(attrib['value'])
            elif attrib['key'] == 'streamType':
                streamType.append(attrib['value'])
            elif attrib['key'] == 'player':
                playerName.append(attrib['value'])
