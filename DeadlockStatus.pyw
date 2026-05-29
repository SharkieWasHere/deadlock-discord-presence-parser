from pypresence import Presence
from pypresence.types import ActivityType
import time
import sys
import psutil
import os
import json

#Important File Logs
time.sleep(5)
log = open('game\\citadel\\console.log', "r")



with open ("heroes.json") as Heros:
        HeroData = json.load(Heros)


# Check for Deadlock

def IsOpen(process_name):
    for proc in psutil.process_iter(['name']):
        try:
            if process_name.lower() == proc.info['name'].lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


#============================================================================================================
# Skim Console Log

def ConsoleUpdate(log,InMatch = 0):

    
    Updated = True
    
    while True:
        line = log.readline()
    
        
        if not line:

                if not IsOpen("deadlock.exe"):
                        return None
            
                time.sleep(0.1)
                continue
        if "[Client] Map: \"start\"" in line:
                InMatch = 1
                Updated = False
                print("Found Match")
        elif "[Client] Map: \"new_player_basics\"" in line:
                InMatch = 2
                Updated = False
                print("Found Sandbox")
        elif "[Client] Map:" in line:
                InMatch = 0
                Updated = False
                print("Found Hideout")
                
                
        
        
        if(InMatch != 1 or (InMatch == 1 and Updated == False)):
                
                if " VMDL Camera Pose Success! " in line:
            
                        StringList = line.split("/")
                
                        StringClean= StringList[len(StringList)-1].split(".vmdl")

                        Updated = True

                        
                        return(StringClean[0], InMatch)
          
            


#============================================================================================================

        



#============================================================================================================

def SteamID():
    ID = 0
    with open('game\\citadel\\console.log', "r") as log:
        for i in log:
            CurrentLine = log.readline()
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
#Let Game Load Console

while (ID <= 0):
        try:
                
                UserData = SteamID()
                ID = UserData[0]
                User = UserData[1]
        except:
                pass
InMatch = 0
while IsOpen("deadlock.exe"):
        time.sleep(1)
        GameData = ConsoleUpdate(log,InMatch)
        if GameData is None:
                continue
           
        Debug = GameData[0]

        if(GameData[1] == 1):
                Status = "In Game"
                X = "Taking part in the ritual as"
        elif(GameData[1] == 2):
                Status = "In Sandbox"
                X = "Messing around with"
        else:
                try:
                        Status = HeroData[Debug]['hideout_text']
                        X = "Relaxing as"
                except:
                        Status = "In Hideout as"
                        X = "Relaxing as"

        Start = Debug

        if(Hero != Debug or InMatch != GameData[1]):
                try:
                        HeroName = HeroData[Debug]['name']
                except:
                        HeroName = "Unknown"
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



            
