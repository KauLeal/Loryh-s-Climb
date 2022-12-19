import pygame
import random

class Enemy(pygame.sprite.Sprite): 
    def __init__(self, tela_largura, y, sprite_sheet, scale):
        pygame.sprite.Sprite.__init__(self)

        #define variables
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        self.direction = random.choice([-1, 1]) # -1 -> left, 1 -> right
        if self.direction == 1:
            self.flip = True
        else: 
            self.flip = False

        #load images from spritesheets
        animations_steps = 8
        for animation in range(animations_steps):
            image = sprite_sheet.get_image(animation, 32, 32, scale, (0, 0, 0))
            image = pygame.transform.flip(image, self.flip, False)
            image.set_colorkey((0, 0, 0))
            self.animation_list.append(image)

        #select starting image and create rectangle from it
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()

        if self.direction ==  1: #if starter in right, go to left
            self.rect.x = 0
        else:
            self.rect.x = tela_largura

        self.rect.y = y
    
    def update(self, rolagem,tela_largura):
        #update animation
        ANIMATION_COOLDOWN = 100
        #update image depending on current frame
        self.image = self.animation_list[self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if the animation has run out then reset back to the start
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

        #move enemy
        self.rect.x += self.direction * 2
        self.rect.y += rolagem

        #check if gone off tela
        if self.rect.right < 0 or self.rect.left > tela_largura:
            self.kill()