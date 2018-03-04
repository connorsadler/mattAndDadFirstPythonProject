import pygame

pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))

pygame.display.set_caption('Matthew S stunt cars')
black = (0,0,0)
red = (150,10,15)

clock=pygame.time.Clock()

crashed=False
carImg = pygame.image.load('racecar.png')

def car(x,y):
    gameDisplay.blit(carImg, (x,y))

x =  (display_width * 0.45)
y = (display_height * 0.8)

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    gameDisplay.fill(red)
    car(x,y)
    
    if y > 0:
        y = y - 10
        x = x - 5
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
