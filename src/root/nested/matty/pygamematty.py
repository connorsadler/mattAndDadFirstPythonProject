import pygame
import time

pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))

pygame.display.set_caption('Matthew S stunt cars')
black = (0,0,0)
red = (150,10,15)

clock=pygame.time.Clock()


carImg = pygame.image.load('racecar.png')

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

    
    

def crash(x,y):
    message_display('You Crashed', 115)
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
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                    
        x = x + x_change
        
        gameDisplay.fill(red)
        car(x,y)
        if x > display_width - car_width or x < 0:
            crash(x,y)
        
    #     if y > 0:
    #         y = y - 10
    #         x = x - 5
        
        pygame.display.update()
        clock.tick(60)

game_loop()
pygame.quit()
quit()
