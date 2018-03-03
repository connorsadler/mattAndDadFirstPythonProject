from tkinter import font
from tkinter import *

TIMESTEP = 10

print("gameclient starts")





 #----------------------------
# Minecraft 2D
#----------------------------

import pygame, sys, random
from pygame.locals import *
from variables import *

fpsClock = pygame.time.Clock()

#variables for the map size
TILESIZE  = 3
MAPWIDTH  = 100
MAPHEIGHT = 30

#the position of the player [x,y]
playerPos = [0,0]

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

pygame.key.set_repeat(5)
                      
while True:

    #fill the background in black        
    DISPLAYSURF.fill(BLACK)

    #get all the user events
    for event in pygame.event.get():
        #if the user wants to quit
        if event.type == QUIT:
            #and the game and close the window
            pygame.quit()
            sys.exit()
        #if a key is pressed
        elif event.type == KEYDOWN:
            #if the right arrow is pressed
            if event.key == K_RIGHT and playerPos[0] < MAPWIDTH - 1:
                #change the player's x position
                playerPos[0] += 1
            if event.key == K_LEFT and playerPos[0] > 0:
                #change the player's x position
                playerPos[0] -= 1
            if event.key == K_UP and playerPos[1] > 0:
                #change the player's x position
                playerPos[1] -= 1
            if event.key == K_DOWN and playerPos[1] < MAPHEIGHT -1:
                #change the player's x position
                playerPos[1] += 1
                    
#     #loop through each row
#     for row in range(MAPHEIGHT):
#         #loop through each column in the row
#         for column in range(MAPWIDTH):
#             #draw the resource at that position in the tilemap, using the correct image
#             DISPLAYSURF.blit(textures[tilemap[row][column]], (column*TILESIZE,row*TILESIZE))
        
    #display the player at the correct position 
    DISPLAYSURF.blit(PLAYER,(playerPos[0] * TILESIZE,
                             playerPos[1] * TILESIZE)
                     )

    #update the display
    pygame.display.update()
    #create a short delay
    fpsClock.tick(24)
