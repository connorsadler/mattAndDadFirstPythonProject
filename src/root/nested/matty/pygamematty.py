import pygame
import time
import random

pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))

pygame.display.set_caption('Matthew S stunt cars')
black = (0,0,0)
red = (150,10,15)

clock=pygame.time.Clock()


carImg = pygame.image.load('racecar.png')

def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: "+str(count), True, black)
    gameDisplay.blit(text,(0,0))
    
def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])
    
def car(x,y):
    gameDisplay.blit(carImg, (x,y))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text, fontsize):
    largeText = pygame.font.Font('freesansbold.ttf',fontsize)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    
    

def crash(x,y, dodged):
    message_display('You Crashed', 115)
    time.sleep(2)
    gameDisplay.fill(red)
    message_display('You Scored: ' + str(dodged), 90)
    time.sleep(2)
    gameDisplay.fill(red)
    car(x,y)
    message_display('Prepare to Quit!!!', 80)
    time.sleep(2)
#     game_loop()
    pygame.quit()
    quit()
    
def game_loop():
    x =  (display_width * 0.45)
    y = (display_height * 0.8)
    x_change = 0
    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 7
    thing_width = 100
    thing_height = 100
    dodged = 0
    
    car_speed = 0
    car_width = 73
    gameExit=False
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5 - dodged
                elif event.key == pygame.K_RIGHT:
                    x_change = 5 + dodged
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                    
        x = x + x_change
        
        gameDisplay.fill(red)
        
        things(thing_startx, thing_starty, thing_width, thing_height, black)
        thing_starty += thing_speed
        
        car(x,y)
        things_dodged(dodged)
        if x > display_width - car_width or x < 0:
            crash(x,y, dodged)
    
            
        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, display_width )
            dodged += 1
            thing_speed += 1
            thing_width += (dodged * 1.2)

        if y < thing_starty+thing_height:
            print('y crossover')
            if x > thing_startx and x < thing_startx + thing_width or x+car_width > thing_startx and x + car_width < thing_startx+thing_width:
                print('x crossover')
                crash(x,y, dodged)
        
        pygame.display.update()
        clock.tick(60)

game_loop()
pygame.quit()
quit()
