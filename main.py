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
scroll_thresh = 200
gravity = 1
max_platforms = 10
scroll = 0
bg_scroll = 0
game_over = False
score = 0

#colors
WHITE = (255, 255, 255)

#define font
font_small = pygame.font.SysFont('Lucida Sans', 20)
font_big = pygame.font.SysFont('Lucida Sans', 24)

#load images
lory_image = pygame.image.load('assets/lory.png').convert_alpha()
bg_image = pygame.image.load('assets/sky.png').convert_alpha()
platform_image = pygame.image.load('assets/platform.png').convert_alpha()

#function for outputting text onto the screen
def draw_test(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


#function for drawing the background
def draw_bg(bg_scroll):
    screen.blit(bg_image, (0, 0 + bg_scroll))
    screen.blit(bg_image, (0, -600 + bg_scroll))

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
        scroll = 0
        dx = 0
        dy = 0

        #process keypresses
        key = pygame.key.get_pressed()
        
        if key[pygame.K_a]: #move to left
            dx = -10
            self.flip = True
        if key[pygame.K_LEFT]: #move to left
            dx = -10
            self.flip = True
        if key[pygame.K_d]: #move to right
            dx = 10
            self.flip = False
        if key[pygame.K_RIGHT]: #move to right
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

        #check if the player has bounced to the top of the screen
        if self.rect.top <= scroll_thresh:
            #if player is jumping
            if self.vel_y < 0:
                scroll = -dy

        #update rectangule position
        self.rect.x += dx
        self.rect.y += dy + scroll

        return scroll

#platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image, (width, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self, scroll):

        #update platform's vertical position
        self.rect.y += scroll

        #check if platform's has gone off the screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

#player instance
lory = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)

#create sprite groups
platform_group = pygame.sprite.Group()

#create starting platforms
platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100)
platform_group.add(platform)

#game loop
run = True
while run: 

    #slow down 
    clock.tick(FPS)

    if game_over == False:
        #move player
        scroll = lory.move()

        #draw background
        bg_scroll += scroll
        if bg_scroll >= 600:
            bg_scroll = 0
        draw_bg(bg_scroll)

        #generate platforms
        if len(platform_group) < max_platforms:
            p_w = random.randint(40, 60)
            p_x = random.randint(0, SCREEN_WIDTH - p_w)
            p_y = platform.rect.y - random.randint(80, 120)
            platform = Platform(p_x, p_y, p_w)
            platform_group.add(platform)

        #update platforms
        platform_group.update(scroll)

        #draw sprites
        platform_group.draw(screen)
        lory.draw()

        #check game over
        if lory.rect.top > SCREEN_HEIGHT:
            game_over = True
        
    else:
        draw_test('GAME OVER!', font_big, WHITE, 130, 200)
        draw_test('SCORE: ' + str(score), font_big, WHITE, 130, 250)
        draw_test('PRESS SPACE TO PLAY AGAIN', font_big, WHITE, 40, 300)
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            #reset variables
            game_over = False
            score = 0
            scroll = 0
            #reposition loryh
            lory.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
            #reset platforms
            platform_group.empty()
            #create starting platforms
            platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100)
            platform_group.add(platform)

    #event handler
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False


    #update display pygame
    pygame.display.update()

pygame.quit()