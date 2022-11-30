import pygame

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("L'oryhs Climb")

#colors
WHITE = (255, 255, 255)

#load image
lory_image = pygame.image.load('assets/lory.png').convert_alpha()
bg_image = pygame.image.load('assets/bg.jpg').convert_alpha()

#class player
class Player:
    def __init__(self, x, y): # x and y are init cordenates of player
        self.image = pygame.transform.scale(lory_image, (45, 45)) #add image in the player and resize
        self.width = 25 # width of rect
        self.height = 40 # height of rect
        self.rect = pygame.Rect(0, 0, self.width, self.height) #create a rect around of the player     
        self.rect.center = (x, y) # posicion the rect

    def draw(self):
        screen.blit(self.image, (self.rect.x - 10, self.rect.y - 5)) #move some pixels to adjust the rect
        pygame.draw.rect(screen, WHITE, self.rect, 2)

lory = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150) 

#game loop
run = True
while run: 

    #draw bg
    screen.blit(bg_image, (0,0))
    
    #draw player
    lory.draw()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False


    #update display pygame
    pygame.display.update()

pygame.quit()