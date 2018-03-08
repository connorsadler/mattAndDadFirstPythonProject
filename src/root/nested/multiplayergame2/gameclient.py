from tkinter import font
from tkinter import *
import sys
import inputboxlibrary
from chatclientlibrary import *
import pygame, sys, random
from pygame.locals import *
from variables import *
import random

#--------------------------------------------------
# Minecraft 2D - Heavily modified for multiplayer
#--------------------------------------------------

print("gameclient starts")

fpsClock = pygame.time.Clock()

#variables for the map size
TILESIZE  = 3
MAPWIDTH  = 100
MAPHEIGHT = 100

FPS = 24
TIMESTEP = 10  # not sure what this is

black = (0,0,0)
red = (150,10,15)
redbright = (250,10,15)

#the position of the player [x,y]
playerPos = [0,0]
automove = False
autoMoveMode = 0
# player id (aka client id) -> Player
otherPlayersById = {}
sprites = [ ]

class Player():
    def __init__(self, playerId, name):
        self.playerId = playerId
        self.name = name
        self.location = [0, 0]
    
    def setLocation(self, x, y):
        self.location = [x, y]
    
    def getLocation(self):
        return self.location

def drawText(gameDisplay, text, pos, font, colour):
    #font = pygame.font.SysFont(None, fontsize)
    t = font.render(text, True, colour)
    gameDisplay.blit(t,pos)

class Sprite():
    def __init__(self, pos):
        self.pos = pos
    
    def drawAndUpdate(self, DISPLAYSURF):
        pygame.draw.rect(DISPLAYSURF, black, [self.pos[0], self.pos[1], 20, 20])
    
    def isDead(self):
        return False;
    
    def onDeathSpawn(self):
        return [];
    
class SpeechBubble(Sprite):
    def __init__(self, text, pos):
        super().__init__(pos)
        self.text = text
        self.font = pygame.font.SysFont(None, 30)
        self.timer = 3 * FPS
        self.colorredbright = [255,10,15]
    
    def drawAndUpdate(self, DISPLAYSURF):
        drawText(DISPLAYSURF, self.text, self.pos, self.font, (self.colorredbright[0], self.colorredbright[1], self.colorredbright[2]))
        self.timer -= 1
        self.colorredbright[0] -= 3
        if self.timer % 2 == 0:
            self.pos = (self.pos[0], self.pos[1] + 1)
    
    def isDead(self):
        return self.timer <= 0 or self.colorredbright[0] < 50

BOMB_FRAME_WIDTH = 24

class Bomb(Sprite):
    def __init__(self, pos):
        super().__init__(pos)
        self.timer = 100
        # crop rect
        cropx,cropy = 0,29  # Change value to crop different rect areas
        self.cropRect = (cropx, cropy, 22, 27)
    
    def drawAndUpdate(self, DISPLAYSURF):
        DISPLAYSURF.blit(BOMB,(self.pos[0] * TILESIZE, self.pos[1] * TILESIZE), self.cropRect)
        self.timer -= 1
        
        # shake
        xvel = self.timer % 3 + -1
        yvel = 1 - (self.timer % 3)
        self.pos = (self.pos[0] + xvel, self.pos[1] + yvel)
        
        # every 25 frames, move the crop rect along the image so it shows a different part of the source bomb image
        # this is effectively a differently coloured bomb image frame
        if self.timer % 25 == 0:
            self.cropRect = (self.cropRect[0] + BOMB_FRAME_WIDTH, self.cropRect[1], self.cropRect[2], self.cropRect[3])

    def isDead(self):
        return self.timer <= 0

    def onDeathSpawn(self):
        return [BombFragment(self.pos, 5, 0), BombFragment(self.pos, -5, 0),
                BombFragment(self.pos, 0, 5), BombFragment(self.pos, 0, -5)
               ];

class BombFragment(Sprite):
    def __init__(self, pos, xvel, yvel):
        super().__init__(pos)
        self.xvel = xvel
        self.yvel = yvel
        self.timer = 50
        # crop rect - 4th frame of bomb
        cropx,cropy = 4 * BOMB_FRAME_WIDTH,29  # Change value to crop different rect areas
        self.cropRect = (cropx, cropy, 22, 27)
    
    def drawAndUpdate(self, DISPLAYSURF):
        DISPLAYSURF.blit(BOMB,(self.pos[0] * TILESIZE, self.pos[1] * TILESIZE), self.cropRect)
        self.timer -= 1
        self.pos = (self.pos[0] + self.xvel, self.pos[1] + self.yvel)

    def isDead(self):
        return self.timer <= 0

#use list comprehension to create our tilemap
#tilemap = [ [DIRT for w in range(MAPWIDTH)] for h in range(MAPHEIGHT) ] 

#set up the display
pygame.init()
DISPLAYSURF = pygame.display.set_mode((MAPWIDTH * TILESIZE, MAPHEIGHT * TILESIZE))

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

def createSpeechBubble(text, pos):
    s = SpeechBubble(text, (TILESIZE* (pos[0] + 5), TILESIZE * (pos[1] + 5)))
    sprites.append(s)

# parse something like: '[0, 8]' into a tuple of int's
def parseLocation(s):
    newLocationStr = s.replace("[","").replace("]","")
    newLocationXY = newLocationStr.split(",")
    return ( int(newLocationXY[0]), int(newLocationXY[1]) )

def handlePlayerUpdate(msgPartsSub):
    print("handlePlayerUpdate: " + str(msgPartsSub))
    playerId = msgPartsSub[0]
    
    
    if playerId == myClientId:
        # Its me - only message we listen for is SAYSOMETHING
        
        if msgPartsSub[1] == "SAYSOMETHING":
            createSpeechBubble(msgPartsSub[2], playerPos)
        
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
        x,y = parseLocation(msgPartsSub[2])
        otherPlayer.setLocation(x, y)
        return

    # SAYSOMETHING
    if msgPartsSub[1] == "SAYSOMETHING":
        createSpeechBubble(msgPartsSub[2], otherPlayer.getLocation())

    # DROPBOMB
    if msgPartsSub[1] == "DROPBOMB":
        x,y = parseLocation(msgPartsSub[2])
        s = Bomb((x, y))
        sprites.append(s)        
    
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

def saySomething(text):
    print("saySomething: " + text)
    chatClient.send("MINECRAFT: PLAYERUPDATE: " + myClientId + ": SAYSOMETHING: " + text)

# Connect to server
chatClient = ChatClient()
HOST = 'localhost'
PORT = '33000'

chatClient.connect(HOST, PORT, gameOnMessage, gameOnQuit)

# Alternate "client id" could be local port that we're connecting o
# myClientId2 = chatClient.getClientId()
# print("myClientId2: " + myClientId2)
                      
pygame.display.set_caption("gameclient - " + myClientId)

w, h = pygame.display.get_surface().get_size()
input_box1 = inputboxlibrary.InputBox(10, h - 35, 270, 32, saySomething)

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
            if event.key == K_TAB:
                automove = not automove
                if automove:
                    autoMoveMode = 1
            if event.key == K_b:
                s = Bomb(playerPos.copy())
                sprites.append(s)
                chatClient.send("MINECRAFT: PLAYERUPDATE: " + myClientId + ": DROPBOMB: " + str(playerPos))
        # send all events to input box also
        input_box1.handle_event(event)

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
    # display any sprites
    anySpritesDead = False
    for sprite in sprites:
        sprite.drawAndUpdate(DISPLAYSURF)
        anySpritesDead = anySpritesDead or sprite.isDead()
    deathSpawnedNewSprites = []
    if anySpritesDead:
        for sprite in sprites:
            if (sprite.isDead()):
                sprites.remove(sprite)
                deathSpawnedNewSprites = deathSpawnedNewSprites + sprite.onDeathSpawn()
        sprites = sprites + deathSpawnedNewSprites
    
    # input box
    input_box1.draw(DISPLAYSURF)

    #update the display
    pygame.display.update()
    #create a short delay
    fpsClock.tick(FPS)
