from pypresence import Presence
from pypresence.types import ActivityType
import time
import sys
import psutil
import os
import json

#Important File Logs
time.sleep(30) #Let file reset and load (30 seconds)
log = open('game/citadel/console.log', "r")



with open ("heroes.json") as Heros:
        HeroData = json.load(Heros)


# Check for Deadlock

def IsOpen(process_name):
    for proc in psutil.process_iter(['name']):
        try:
            if process_name.lower() == proc.info['name'].lower() or proc.info['name'].lower() == 'deadlock.exe':
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


##============================================================================================================
# Skim Console Log

def ConsoleUpdate(log,InMatch = 0):

    Match = None
    Updated = True

    while True:
        line = log.readline()


        if not line:

                if not IsOpen("mainthrd"):
                        return None

                time.sleep(0.1)
                continue



        # Log Most Recent Match ID
        if "match_id=" in line:
                MatchTemp = line.split("match_id=") #For Testing
                Match = MatchTemp[1].strip()
        elif ".com/tv/" in line:
                MatchTemp = line.split(".com/tv/")
                MatchTemp = MatchTemp[1].split("_")
                Match = MatchTemp[0].strip()
        elif "replays/" in line:
                MatchTemp = line.split("replays/")
                MatchTemp = MatchTemp[1].split(".")
                Match = MatchTemp[0].strip()

        #Start Game State check
        if "[Client] Map: \"start\"" in line:
                InMatch = 1
                Updated = False

        elif "[Client] Map: \"new_player_basics\"" in line:
                InMatch = 2
                Updated = False

        elif "[Client] Map:" in line:
                InMatch = 0
                Updated = False

        elif "Signon traffic \"BROADCAST\"" in line:
                InMatch = 4
                Updated = False
                return("None", InMatch, Match)
        elif "Signon traffic \"DEMO\"" in line:
                InMatch = 3
                Updated = False
                return("None", InMatch, Match)
        #In Future might change to list... This if chain is killing me..



        if(InMatch == 0 or InMatch == 2 or (InMatch == 1 and Updated == False)):

                if " VMDL Camera Pose " in line:

                        StringList = line.split("/")

                        StringClean= StringList[len(StringList)-1].split(".vmdl")

                        Updated = True


                        return(StringClean[0], InMatch, Match)




#============================================================================================================





#============================================================================================================

def SteamID():
    ID = 0
    with open('game/citadel/console.log', "r") as log:
        for i in log:
            CurrentLine = i
            if "AuthStatus (steamid:" in CurrentLine:
                StringList = CurrentLine.split("steamid:")

                StringClean= StringList[len(StringList)-1].split(")")

                ID = StringClean[0]
                try:
                    ID = int(ID)
                except:
                    ID=0
            if "Server] Client 0 " in CurrentLine:
                StringList = CurrentLine.split("0 ")

                StringClean= StringList[len(StringList)-1].split("'")

                User = StringClean[1]




                return(ID,User)



#============================================================================================================

CLIENT_ID = "1496084650735570974"

rpc = Presence(CLIENT_ID)
rpc.connect()

Start = 0
ID = 0
Hero = "Slork"
MatchID = 0
#Let Game Load Console

while (ID <= 0):
        try:

                UserData = SteamID()
                ID = UserData[0]
                User = UserData[1]
        except:
                pass
InMatch = 0
while IsOpen("mainthrd"):
        time.sleep(1)
        GameData = ConsoleUpdate(log,InMatch) #Returns Hero, Game State, Match ID
        if GameData is None:
                continue

        Debug = GameData[0] #Debug for Internal Hero Name

        if GameData[2] is not None:
                MatchID = GameData[2]

        if(GameData[1] == 1):
                Status = f"In Match: {MatchID}"
                X = "Taking part in the ritual as"
        elif(GameData[1] == 2):
                Status = "In Sandbox"
                X = "Messing around with"
        elif(GameData[1] == 0):
                try:
                        Status = HeroData[Debug]['hideout_text']
                        X = "Relaxing as"
                except:
                        Status = "In Hideout as"
                        X = "Relaxing as"
        elif(GameData[1] == 3):
                Status = f"Watching Replay: {MatchID}"
                X = "Viewing through the patrons eyes"
        elif(GameData[1] == 4):
                Status = f"Spectating Live Match: {MatchID}"
                X = "Viewing through the patrons eyes"


        if(Hero != Debug or InMatch != GameData[1]):
                try:
                        HeroName = HeroData[Debug]['name']
                except:
                        HeroName = ":3" #This is a place holder..
                rpc.update(
                activity_type=ActivityType.PLAYING,
                state=f"{Status}",
                details=f"{X} {HeroName}",
                large_image="icon",
                buttons=[
                        {"label": "Status made by Sharkie", "url": "https://statlocker.gg/profile/1223916924/matches"},
                        {"label": f"Logged in as '{User}'", "url": f"https://statlocker.gg/profile/{ID}/matches"}
                        ]
                )
        Hero = Debug
        InMatch = GameData[1]


time.sleep(3)
rpc.clear()
rpc.close()
sys.exit()






