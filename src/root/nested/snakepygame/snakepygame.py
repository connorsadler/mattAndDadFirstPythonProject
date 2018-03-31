import pygame, sys, random
from pygame.locals import *
from collections import deque
from math import pi, sin, cos, tan

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
    
    def drawAndUpdate(self, DISPLAYSURFX):
        DISPLAYSURFX.pygame_draw_rect(black, [self.pos[0], self.pos[1], 20, 20])
    
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
        self.trail = deque(maxlen = 5000)
        # length of snake i.e. max entries in trail
        self.snakelength = 50
        # frame of animation
        self.frame = 0
        self.piDividedBy2 = pi / 2
        self.angleMovePerFrame = self.piDividedBy2 / 50

    def getTrailLength(self):
        return len(self.trail)

    def processKey(self, event):
        # change direction on keydown events
        if event.type == KEYDOWN:
            screenx = DISPLAYSURFX.transformx(self.pos[0])
            screeny = DISPLAYSURFX.transformy(self.pos[1])
            if event.key == K_RIGHT and screenx < MAPWIDTH - 1:
                self.playerxvel = 1
                self.playeryvel = 0
            if event.key == K_LEFT and screenx > 0:
                self.playerxvel = -1
                self.playeryvel = 0
            if event.key == K_UP and screeny > 0:
                self.playeryvel = -1
                self.playerxvel = 0
            if event.key == K_DOWN and screeny < MAPHEIGHT -1:
                self.playeryvel = 1
                self.playerxvel = 0
        # dont bother with keyup events, as we keep the snaking moving all the time
        #             elif event.type == KEYUP:
        #                 if event.key == K_RIGHT or event.key == K_LEFT:
        #                     playerxvel = 0
        #                 if event.key == K_UP or event.key == K_DOWN:
        #                     playeryvel = 0
            
    def drawAndUpdate(self, DISPLAYSURFX):
        self.frame += 1
        if self.frame == 100:
            self.frame = 0
        
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
        
        screenx = DISPLAYSURFX.transformx(self.pos[0])
        screeny = DISPLAYSURFX.transformy(self.pos[1])
        
        #
        # CHECK SCROLLING OR JUST MOVING WITHIN CENTRE OF PLAY AREA
        #
        # check if we're near the edge of the screen and heading towards that edge
        scrollx = 0
        if screenx >= MAPWIDTH-100 and self.playerxvel == 1:
            scrollx = 1
        if screenx <= 100 and self.playerxvel == -1:
            scrollx = -1
        scrolly = 0
        if screeny >= MAPHEIGHT-100 and self.playeryvel == 1:
            scrolly = 1
        if screeny <= 100 and self.playeryvel == -1:
            scrolly = -1
        DISPLAYSURFX.scrollBy(scrollx, scrolly)

        # move "head" of snake in world coords
        self.moveBy(self.playerxvel,self.playeryvel)
        
        #
        # DRAWING
        #
        # draw "head" of snake at self.pos
        ###super().drawAndUpdate(DISPLAYSURFX)
        if self.frame < 50:
            startAngle = self.piDividedBy2 - (self.frame * self.angleMovePerFrame)
        else:
            startAngle = (self.frame - 50) * self.angleMovePerFrame
        DISPLAYSURFX.pygame_draw_arc(red, [self.pos[0], self.pos[1], 50, 50], startAngle, -1 * startAngle)
        centrex = self.pos[0]+25
        centrey = self.pos[1]+25
        cosStartAngle = 24 * cos(startAngle)
        sinStartAngle = 24 * sin(startAngle)
        DISPLAYSURFX.pygame_draw_line(red, centrex, centrey, centrex + cosStartAngle, centrey + sinStartAngle)
        DISPLAYSURFX.pygame_draw_line(red, centrex, centrey, centrex + cosStartAngle, centrey - sinStartAngle)
        
        # draw trail
        for trailitem in self.trail:
            DISPLAYSURFX.pygame_draw_rect(black, [trailitem[0], trailitem[1], 20, 20])    


class AppleGenerator(Sprite):
    def __init__(self):
        super().__init__((0,0))

    def drawAndUpdate(self, DISPLAYSURFX):
        if random.randint(0,100) > 95:
            sprites.append(Apple())

class Apple(Sprite):
    def __init__(self):
        super().__init__((random.randint(0, MAPWIDTH), random.randint(0, MAPHEIGHT)))

    def drawAndUpdate(self, DISPLAYSURFX):
        #self.moveBy(0, 1)
        DISPLAYSURFX.pygame_draw_circle(red, self.pos, 5)
    
    def isDead(self):
        #return self.pos[1] > MAPHEIGHT
        pass

# Wrapper for python display surface
# DISPLAYSURF will have been created by a call to: https://www.pygame.org/docs/ref/display.html#pygame.display.set_mode
# This surface can draw things but will transform all coordinates by an "offset". If you move the offset then
# the drawn items will "scroll" around    
class DisplaySurfaceWithScrolling():
    def __init__(self, DISPLAYSURF):
        self.DISPLAYSURF = DISPLAYSURF
        self.offsetx = 0
        self.offsety = 0
        
    def fill(self, color):
        self.DISPLAYSURF.fill(color)
    
    def scrollBy(self, scrollx, scrolly):
        self.offsetx += scrollx
        self.offsety += scrolly
    
    # transform an X coord from "world" to "screen" coords
    def transformx(self, xworld):
        return xworld - self.offsetx

    # transform a Y coord from "world" to "screen" coords
    def transformy(self, yworld):
        return yworld - self.offsety
    
    def transformRect(self, rect):
        return [self.transformx(rect[0]), self.transformy(rect[1]), rect[2], rect[3]]
    
    def pygame_draw_rect(self, color, rect):
        pygame.draw.rect(self.DISPLAYSURF, black, self.transformRect(rect))
    
    def pygame_draw_circle(self, color, pos, radius):
        pygame.draw.circle(self.DISPLAYSURF, color, (self.transformx(pos[0]), self.transformy(pos[1])), radius)

    def pygame_draw_arc(self, color, rect, startAngle, stopAngle):
        pygame.draw.arc(self.DISPLAYSURF, color, self.transformRect(rect), startAngle, stopAngle, 1)
    
    def pygame_draw_line(self, color, x1,y1, x2,y2):
        pygame.draw.line(self.DISPLAYSURF, color, (self.transformx(x1), self.transformy(y1)), (self.transformx(x2), self.transformy(y2)))

# Player is the snake + trail 
player = Player((MAPWIDTH/2, MAPHEIGHT/2))
sprites.append(player)
# AppleGenerator randomly makes apples fall from the sky 
sprites.append(AppleGenerator())
    
#set up the display
pygame.init()
DISPLAYSURFPYGAME = pygame.display.set_mode((MAPWIDTH, MAPHEIGHT))
DISPLAYSURFX = DisplaySurfaceWithScrolling(DISPLAYSURFPYGAME)

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
        DISPLAYSURFX.fill(white)
    
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
            sprite.drawAndUpdate(DISPLAYSURFX)
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
            print("tick: " + str(tick) + ", sprites length: " + str(len(sprites)) + ", trail length: " + str(player.getTrailLength()))


if __name__ == '__main__':
    # This is the code running when you run this file directly
    gameclientMain()
