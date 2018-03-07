from tkinter import font
from tkinter import *
import sys

from chatclientlibrary import *

TIMESTEP = 10

print("gameclient starts")

#--------------------------------------------------
# Minecraft 2D - Heavily modified for multiplayer
#--------------------------------------------------

import pygame, sys, random
from pygame.locals import *
from variables import *

fpsClock = pygame.time.Clock()

#variables for the map size
TILESIZE  = 3
MAPWIDTH  = 100
MAPHEIGHT = 100

#the position of the player [x,y]
playerPos = [0,0]
automove = False
autoMoveMode = 0
# player id (aka client id) -> Player
otherPlayersById = {}

class Player():
    def __init__(self, playerId, name):
        self.playerId = playerId
        self.name = name
        self.location = [0, 0]
    
    def setLocation(self, x, y):
        self.location = [x, y]

#use list comprehension to create our tilemap
#tilemap = [ [DIRT for w in range(MAPWIDTH)] for h in range(MAPHEIGHT) ] 

#set up the display
pygame.init()
DISPLAYSURF = pygame.display.set_mode((MAPWIDTH * TILESIZE, MAPHEIGHT*TILESIZE))

#loop through each row
# for rw in range(MAPHEIGHT):
#     #loop through each column in that row
#     for cl in range(MAPWIDTH):
#         #pick a random number between 0 and 10
#         randomNumber = random.randint(0,10)
#         #WATER if the random number is a 1 or a 2
#         if randomNumber in [1,2]:
#             tile = WATER
#         #GRASS if the random number is a 3 or a 4
#         elif randomNumber in [3,4]:
#             tile = GRASS
#         #otherwise it's DIRT
#         else:
#             tile = DIRT
#         #set the position in the tilemap to the randomly chosen tile
#         tilemap[rw][cl] = tile

# Allow you to hold keys down to move continually
pygame.key.set_repeat(5)

myClientId = "None" 
serverEvents = []

def gameOnMessage(msg):
    # Processing these in the background (socket) thread doesn't seem to work very well
    serverEvents.append(msg)

def gameOnQuit():
    sys.exit()

def gameOnMessage_mainThread(msg):
    global myClientId
    print("gameOnMessage_mainThread: message from server: " + msg)
    idx = msg.find("MINECRAFT:")
    if idx != -1:
        msgMinecraft = msg[idx:]
        msgParts = msgMinecraft.rstrip().split(": ")
        if msgParts[1] == "YOURCLIENTID":
            print("gameOnMessage_mainThread: YOURCLIENTID: " + msgParts[2])
            myClientId = msgParts[2]
            setMyClientId(myClientId)
        elif msgParts[1] == "PLAYERUPDATE":
            handlePlayerUpdate(msgParts[2:])

def handlePlayerUpdate(msgPartsSub):
    print("handlePlayerUpdate: " + str(msgPartsSub))
    playerId = msgPartsSub[0]
    if playerId == myClientId:
        # Its me - ignore
        return
    
    # it's someone else

    # PLAYERCONNECTED
    # TODO: Parse other player's name? We already have their id if required
    if msgPartsSub[1] == "PLAYERCONNECTED":
        print("handlePlayerUpdate: Connect other player")
        newPlayer = Player(playerId, "other")
        otherPlayersById[playerId] = newPlayer
        return

    # TODO: Hack to get an unknown player inside our client
    if playerId not in otherPlayersById:
        print("handlePlayerUpdate: Hack to create unknown other player")
        newPlayer = Player(playerId, "other")
        otherPlayersById[playerId] = newPlayer

    # PLAYERDISCONNECTED
    if msgPartsSub[1] == "PLAYERDISCONNECTED":
        print("handlePlayerUpdate: Disconnect other player")
        # Simply remove the other player from our list of other players
        del otherPlayersById[playerId]
        return
    
    otherPlayer = otherPlayersById[playerId]
    
    # ['4', 'PLAYERMOVED', '[0, 8]']
    if msgPartsSub[1] == "PLAYERMOVED":
        print("handlePlayerUpdate: Move other player")
        newLocationStr = msgPartsSub[2].replace("[","").replace("]","")
        newLocationXY = newLocationStr.split(",")
        otherPlayer.setLocation(int(newLocationXY[0]), int(newLocationXY[1]))
        return
    
    print("handlePlayerUpdate: Not sure how to handle: " + str(msgPartsSub))
                  
def setMyClientId(myClientIdNew):
    global myClientId
    myClientId = myClientIdNew
    pygame.display.set_caption("gameclient - " + myClientId)
    # Usually we have already received the YOURCLIENTID message and set our clientId, so we send that 
    # as first message back to chatroom, thussetting our name
    chatClient.send("PLAYER" + myClientId, BUFSIZ_FIRSTMESSAGE)
    # Now tell all clients that new player has connected
    chatClient.send("MINECRAFT: PLAYERUPDATE: " + myClientId + ": PLAYERCONNECTED")

def doAutomove(playerPos):
    global autoMoveMode
    if autoMoveMode == 1:
        playerPos[0] += 1
        if playerPos[0] >= MAPWIDTH - 8:
            autoMoveMode += 1
    elif autoMoveMode == 2:
        playerPos[1] += 1
        if playerPos[1] >= MAPHEIGHT - 8:
            autoMoveMode += 1
    elif autoMoveMode == 3:
        playerPos[0] -= 1
        if playerPos[0] <= 1:
            autoMoveMode += 1
    elif autoMoveMode == 4:
        playerPos[1] -= 1
        if playerPos[1] <= 1:
            autoMoveMode = 1
    return playerPos

# Connect to server
chatClient = ChatClient()
HOST = 'localhost'
PORT = '33000'

chatClient.connect(HOST, PORT, gameOnMessage, gameOnQuit)

# Alternate "client id" could be local port that we're connecting o
# myClientId2 = chatClient.getClientId()
# print("myClientId2: " + myClientId2)
                      
pygame.display.set_caption("gameclient - " + myClientId)
                      
while True:
    #fill the background in black        
    DISPLAYSURF.fill(BLACK)

    moved = False

    #get all the user events
    for event in pygame.event.get():
        #if the user wants to quit
        if event.type == QUIT:
            #and the game and close the window
            pygame.quit()
            chatClient.send("MINECRAFT: PLAYERUPDATE: " + myClientId + ": PLAYERDISCONNECTED")
            chatClient.send("{quit}")
            sys.exit()
        #if a key is pressed
        elif event.type == KEYDOWN:
            #if the right arrow is pressed
            if event.key == K_RIGHT and playerPos[0] < MAPWIDTH - 1:
                #change the player's x position
                playerPos[0] += 1
                moved = True
            if event.key == K_LEFT and playerPos[0] > 0:
                #change the player's x position
                playerPos[0] -= 1
                moved = True
            if event.key == K_UP and playerPos[1] > 0:
                #change the player's x position
                playerPos[1] -= 1
                moved = True
            if event.key == K_DOWN and playerPos[1] < MAPHEIGHT -1:
                #change the player's x position
                playerPos[1] += 1
                moved = True
            if event.key == K_SPACE:
                automove = not automove
                if automove:
                    autoMoveMode = 1

    if automove:
        doAutomove(playerPos)
        moved = True

    if moved:
        chatClient.send("MINECRAFT: PLAYERUPDATE: " + myClientId + ": PLAYERMOVED: " + str(playerPos))

    if len(serverEvents) > 0:
        serverEventsCopy = list(serverEvents)
        serverEvents.clear()
        for serverEvent in serverEventsCopy:
            gameOnMessage_mainThread(serverEvent)
                    
#     #loop through each row
#     for row in range(MAPHEIGHT):
#         #loop through each column in the row
#         for column in range(MAPWIDTH):
#             #draw the resource at that position in the tilemap, using the correct image
#             DISPLAYSURF.blit(textures[tilemap[row][column]], (column*TILESIZE,row*TILESIZE))
        
    #display the player at the correct position 
    DISPLAYSURF.blit(PLAYER,(playerPos[0] * TILESIZE, playerPos[1] * TILESIZE)
                     )
    # display all other players
    for otherPlayer in otherPlayersById.values():
        DISPLAYSURF.blit(OTHERPLAYER,(otherPlayer.location[0] * TILESIZE, otherPlayer.location[1] * TILESIZE)
                         )
        

    #update the display
    pygame.display.update()
    #create a short delay
    fpsClock.tick(24)
