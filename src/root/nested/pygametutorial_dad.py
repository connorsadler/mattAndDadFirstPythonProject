import pygame

pygame.init()

gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('A bit Racey')
DISPLAY=pygame.display.set_mode((500,400),0,32)
blue=(0,0,255)
extrawidth = 0

clock = pygame.time.Clock()

crashed = False

while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.MOUSEMOTION:
            print('mouse at ({}, {})'.format(event.pos[0], event.pos[1]))
            extrawidth = extrawidth + 1

        print(event)

    pygame.draw.rect(DISPLAY,blue,(200,150,100 + extrawidth,50))

    pygame.display.update()
    clock.tick(60)
    
pygame.quit()
quit()