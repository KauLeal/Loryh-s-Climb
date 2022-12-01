import pygame
import random

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Loryh's Climb")

#set frame rate
clock = pygame.time.Clock()
FPS = 60

#game variables
gravity = 1
max_platforms = 10

#colors
WHITE = (255, 255, 255)

#load images
lory_image = pygame.image.load('assets/lory.png').convert_alpha()
bg_image = pygame.image.load('assets/bg.jpg').convert_alpha()
platform_image = pygame.image.load('assets/platform.png').convert_alpha()

#class player
class Player:
    def __init__(self, x, y): # x and y are init cordenates of player
        self.image = pygame.transform.scale(lory_image, (45, 45)) #add image in the player and resize
        self.width = 25 # width of rect
        self.height = 40 # height of rect
        self.rect = pygame.Rect(0, 0, self.width, self.height) #create a rect around of the player     
        self.rect.center = (x, y) # posicion the rect
        self.vel_y = 0
        self.flip = False #start fliped to right 

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 10, self.rect.y - 5)) #move some pixels to adjust the rect
        pygame.draw.rect(screen, WHITE, self.rect, 2)

    def move(self):
        #reset variables
        dx = 0
        dy = 0

        #process keypresses
        key = pygame.key.get_pressed()
        
        if key[pygame.K_a]: #move to left
            dx = -10
            self.flip = True
        if key[pygame.K_d]: #move to right
            dx = 10
            self.flip = False

        #gravity
        self.vel_y += gravity
        dy += self.vel_y

        #ensure player doesn't go off the edge of the screen
        if self.rect.left + dx < 0:
            dx = 0 -self.rect.left

        if self.rect.right + dx > SCREEN_WIDTH:
            dx =  SCREEN_WIDTH - self.rect.right

        #check collision with platforms
        for platform in platform_group:
            #collision in the y direction
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if above the platform
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = -20

        #check collision with ground
        if self.rect.bottom + dy > SCREEN_HEIGHT:
            dy = 0
            self.vel_y = -20

        #update rectangule position
        self.rect.x += dx
        self.rect.y += dy

#platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image, (width, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#player instance
lory = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150) 

#create sprite groups
platform_group = pygame.sprite.Group()

#create temporary platforms
for p in range (max_platforms):
    p_w = random.randint(40, 60)
    p_x = random.randint(0, SCREEN_WIDTH - p_w)
    p_y = p * random.randint(80, 120)
    platform = Platform(p_x, p_y, p_w)
    platform_group.add(platform)


#game loop
run = True
while run: 

    #slow down 
    clock.tick(FPS)

    #move player
    lory.move()

    #draw bg
    screen.blit(bg_image, (0,0))
    
    #draw sprites
    platform_group.draw(screen)
    lory.draw()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False


    #update display pygame
    pygame.display.update()

pygame.quit()