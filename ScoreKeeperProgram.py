###### Setup
#  Install Python, IMPORTANT: 'Add Python 3 to PATH' should be checked
#  https://www.python.org/downloads/release/python-397/
# 
#  then double click RUN.bat to start the script, closing the cmd window will stop it
# 
#  Below are parameters that can be changed if needed

# Default update freq
UpdateFreq = 10.0

# Arguments json
GitUrl = "https://raw.githubusercontent.com/GMHikaru/Speedrun/main/ScorekeeperLegendary.json"

# Path for the output file (default is same place as the script file)
Destination = 'chessScore.txt'

import threading, os, json
from urllib.request import Request, urlopen

def getScore():
    global UpdateFreq
    threading.Timer(UpdateFreq, getScore).start()

    # Get args from github url
    req = Request(GitUrl, headers={'User-Agent': 'Mozilla/5.0'})
    args = json.loads(urlopen(req).read().decode('utf-8'))
    UpdateFreq = args["updateFreq"]

    url = f"https://api.chess.com/pub/player/{args['username']}/stats"
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = json.loads(urlopen(req).read().decode('utf-8'))
    blitz = response[args['statsKey']]['record']
    win = blitz["win"] - args['startScore'][0]
    loss = blitz["loss"] - args['startScore'][1]
    draw = blitz["draw"] - args['startScore'][2]

    # Text that will be outputted, win/loss/draw are replaced with their respective value
    OutText = args["templateText"].format(win=win, loss=loss, draw=draw)

    outfile = open(Destination, "w")
    outfile.write(OutText)
    outfile.close()
    print('Score updated: ' + OutText)

getScore()
