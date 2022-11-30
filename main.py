import pygame

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("L'oryhs Climb")

#load image
bg_image = pygame.image.load('assets/bg.jpg').convert_alpha()

#game loop
run = True
while run: 

    #draw bg
    screen.blit(bg_image, (0,0))
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False


    #update display pygame
    pygame.display.update()

pygame.quit()