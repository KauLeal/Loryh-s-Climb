import pygame
import random

class Enemy(pygame.sprite.Sprite): 
    def __init__(self, SCREEN_WIDTH, y, sprite_sheet, scale):
        pygame.sprite.Sprite.__init__(self)

        #define variables
        self.direction = random.choice([-1, 1]) # -1 -> left, 1 -> right
        if self.direction == 1:
            self.flip = True
        else: 
            self.flip = False

        #load images from spritesheets
        image = sprite_sheet.get_image(0, 32, 32, scale, (0, 0, 0))
        image = pygame.transform.flip(image, self.flip, False)
        image.set_colorkey((0, 0, 0))
        self.image = image
        self.rect = self.image.get_rect()

        if self.direction ==  1: #if starter in right, go to left
            self.rect.x = 0
        else:
            self.rect.x = SCREEN_WIDTH

        self.rect.y = y
    
    def update(self, scroll,SCREEN_WIDTH):

        #move enemy
        self.rect.x += self.direction * 2
        self.rect.y += scroll

        #check if gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()