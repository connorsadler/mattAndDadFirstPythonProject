import pygame, sys, random
from pygame.locals import *
from collections import deque

#--------------------------------------------------
# Snake in pygame
#--------------------------------------------------

print("snakepygame starts")

fpsClock = pygame.time.Clock()

#variables for the map size
MAPWIDTH  = 500
MAPHEIGHT = 500

FPS = 160

black = (0,0,0)
white = (255,255,255)
red = (150,10,15)
redbright = (250,10,15)

sprites = [ ]

class Sprite():
    def __init__(self, pos):
        self.pos = pos
    
    def processKey(self, event):
        # by default a Sprite does nothing with key events 
        pass 
    
    def drawAndUpdate(self, DISPLAYSURF):
        pygame.draw.rect(DISPLAYSURF, black, [self.pos[0], self.pos[1], 20, 20])
    
    def isDead(self):
        return False;
    
    def onDeathSpawn(self):
        return [];
    
    def moveBy(self, xvel, yvel):
        self.pos = (self.pos[0] + xvel, self.pos[1] + yvel)

class Player(Sprite):
    def __init__(self, pos):
        super().__init__(pos)
        self.playerxvel = 1
        self.playeryvel = 0
        # trail is a queue of position (x,y) tuples
        # leftmost entry is "tail" of our snake, and rightmost entry is "head"
        self.trail = deque()
        # length of snake i.e. max entries in trail
        self.snakelength = 50

    def processKey(self, event):
        # change direction on keydown events
        if event.type == KEYDOWN:
            if event.key == K_RIGHT and self.pos[0] < MAPWIDTH - 1:
                self.playerxvel = 1
                self.playeryvel = 0
            if event.key == K_LEFT and self.pos[0] > 0:
                self.playerxvel = -1
                self.playeryvel = 0
            if event.key == K_UP and self.pos[1] > 0:
                self.playeryvel = -1
                self.playerxvel = 0
            if event.key == K_DOWN and self.pos[1] < MAPHEIGHT -1:
                self.playeryvel = 1
                self.playerxvel = 0
        # dont bother with keyup events, as we keep the snaking moving all the time
        #             elif event.type == KEYUP:
        #                 if event.key == K_RIGHT or event.key == K_LEFT:
        #                     playerxvel = 0
        #                 if event.key == K_UP or event.key == K_DOWN:
        #                     playeryvel = 0
            
    def drawAndUpdate(self, DISPLAYSURF):
        #
        # TRAIL MANAMGEMENT
        #
        # add item to end of trail
        self.trail.append(self.pos)
        # remove "tail" of snake
        if len(self.trail) > self.snakelength:
            self.trail.popleft()
        # increase length randomly
        if random.randint(0,100) > 75:
            self.snakelength += 1
        
        #
        # CHECK SCROLLING OR JUST MOVING WITHIN CENTRE OF PLAY AREA
        #
        # check if we're near the edge of the screen and heading towards that edge
        scrollx = 0
        if self.pos[0] >= MAPWIDTH-100 and self.playerxvel == 1:
            scrollx = 1
        if self.pos[0] <= 100 and self.playerxvel == -1:
            scrollx = -1
        scrolly = 0
        if self.pos[1] >= MAPHEIGHT-100 and self.playeryvel == 1:
            scrolly = 1
        if self.pos[1] <= 100 and self.playeryvel == -1:
            scrolly = -1
        scrolling = scrollx != 0 or scrolly != 0

        #
        # MOVE OR SCROLL
        #
        if not scrolling:
            # move "head" of snake onscreen
            self.moveBy(self.playerxvel,self.playeryvel)
        else:
            # instead of moving our snake, we "scroll" everything else
            for sprite in sprites:
                if isinstance(sprite, Apple):
                    sprite.moveBy(-1 * scrollx, -1 * scrolly)
            # we need to scroll our trail also
            newtrail = []
            for trailitem in self.trail:
                newtrailitem = (trailitem[0] + (-1 * scrollx), trailitem[1] + (-1 * scrolly))
                newtrail.append(newtrailitem)
            self.trail.clear()
            self.trail.extend(newtrail)
        
        #
        # DRAWING
        #
        # draw "head" of snake at self.pos
        super().drawAndUpdate(DISPLAYSURF)
        # draw trail
        for trailitem in self.trail:
            pygame.draw.rect(DISPLAYSURF, black, [trailitem[0], trailitem[1], 20, 20])    


class AppleGenerator(Sprite):
    def __init__(self):
        super().__init__((0,0))

    def drawAndUpdate(self, DISPLAYSURF):
        if random.randint(0,100) > 95:
            sprites.append(Apple())

class Apple(Sprite):
    def __init__(self):
        super().__init__((random.randint(0, MAPWIDTH), random.randint(0, MAPHEIGHT)))

    def drawAndUpdate(self, DISPLAYSURF):
        #self.moveBy(0, 1)
        pygame.draw.circle(DISPLAYSURF, red, self.pos, 5)
    
    def isDead(self):
        #return self.pos[1] > MAPHEIGHT
        pass
    

# Player is the snake + trail 
sprites.append(Player((MAPWIDTH/2, MAPHEIGHT/2)))
# AppleGenerator randomly makes apples fall from the sky 
sprites.append(AppleGenerator())
    
#set up the display
pygame.init()
DISPLAYSURF = pygame.display.set_mode((MAPWIDTH, MAPHEIGHT))

#
# main code to run a game client
#
def gameclientMain():
    global sprites
    
    pygame.display.set_caption("snakepygame")
    
    #w, h = pygame.display.get_surface().get_size()
    tick = 0

    while True:
        #fill the background in black        
        DISPLAYSURF.fill(white)
    
        #get all the user events
        for event in pygame.event.get():
            #if the user wants to quit
            if event.type == QUIT:
                #and the game and close the window
                pygame.quit()
                sys.exit()
            #if a key is pressed
            elif event.type == KEYDOWN or event.type == KEYUP:
                for sprite in sprites:
                    sprite.processKey(event)
    
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
        
        #update the display
        pygame.display.update()
        #create a short delay
        fpsClock.tick(FPS)
        
        tick += 1
        if tick % 100 == 0:
            print("tick: " + str(tick) + ", sprites length: " + str(len(sprites)))


if __name__ == '__main__':
    # This is the code running when you run this file directly
    gameclientMain()
