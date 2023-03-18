from phBot import *
from threading import Timer
import phBotChat
import struct
import re

pName = 'JobSecure'
pVersion = '0.0.3'

# ______________________________ Initializing ______________________________ #

BOT_NAME = "Nick"

# Globals
findMasterName = None

# ______________________________ Methods ______________________________ #

# Request party match data
def Inject_RequestPartyMatch(pageIndex=0):
    p = struct.pack('B',pageIndex)
    inject_joymax(0x706C,p,False)

# ______________________________ Events ______________________________ #

# All chat messages received are sent to this function
def handle_chat(t,player,msg):
    # Check if is bot system nickname
    if player == BOT_NAME:
        # Asking press E
        if "E'ye bas." in msg:
            Inject_RequestPartyMatch()
        else:
            # Check if is asking for party match
            check = re.search(r'PartyNo ([a-zA-Z0-9_]*)',msg)
            if check:
                # Start scanning party match list to find the player
                global findMasterName
                findMasterName = check[1]
                log("Plugin: Starting Party Match scanner for \""+findMasterName+"\"...")
                Inject_RequestPartyMatch()

# All packets received from Silkroad will be passed to this function
# Returning True will keep the packet and False will not forward it to the game server
def handle_joymax(opcode,data):
    # SERVER_PARTY_MATCH_LIST_RESPONSE
    if opcode == 0xB06C:
        global findMasterName
        # Check if is scannnig
        if findMasterName:
            # Check success
            if data[0] != 1:
                log("Plugin: Party match request error!")
                findMasterName = None
                return True

            # The cursor to read the packet properly
            packetIndex = 1

            # page match setup
            pageCount = data[packetIndex]
            packetIndex+=1
            pageIndex = data[packetIndex]
            packetIndex+=1
            partyCount = data[packetIndex]
            packetIndex+=1

            log("Plugin: Scanning Party Match ("+str(pageIndex+1)+"/"+str(pageCount)+")...")
            partyNumber = None
            # Check match by match
            for i in range(partyCount):
                number = struct.unpack_from("<I",data,packetIndex)[0]
                packetIndex+=8
                # Extract master name
                masterNameLength = struct.unpack_from('<H',data,packetIndex)[0]
                packetIndex+=2
                masterName = struct.unpack_from('<'+str(masterNameLength)+'s',data,packetIndex)[0].decode('cp1252')
                packetIndex+=masterNameLength

                # Check the master name
                if findMasterName == masterName:
                    partyNumber = number
                    break

                # skip data
                packetIndex+=6
                titleLength = struct.unpack_from('<H',data,packetIndex)[0]
                packetIndex+=titleLength+2

            # Check if party has been found
            if partyNumber == None:
                nextPage = pageIndex+1
                if nextPage < pageCount:
                    # wait 1 second to request the next page
                    Timer(1.0,Inject_RequestPartyMatch(nextPage)).start()
                else:
                    log("Plugin: Party Match with \""+findMasterName+"\" as master doesn't exists")
                    findMasterName = None
            else:
                log("Plugin: Party Match #"+str(partyNumber)+" from \""+findMasterName+"\"")
                # Stop process
                findMasterName = None
                # Answering to the bot
                phBotChat.Private(BOT_NAME,str(partyNumber))
    return True

# Plugin loaded
log('Plugin: '+pName+' v'+pVersion+' succesfully loaded')