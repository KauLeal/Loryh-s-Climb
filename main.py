import pygame
import random
import os
from spritesheet import SpriteSheet
from enemy import Enemy

pygame.init()

tela_largura = 400
tela_altura = 600

tela = pygame.display.set_mode((tela_largura, tela_altura))
pygame.display.set_caption("Loryh's Climb")

#definir frame rate
relogio = pygame.time.Clock()
FPS = 60

# etapas 
# 1 - adicionar 'SDTK1' com loop no menu 
# 2 - mudar a musica 'SDTK1' para 'SDTK2' com loop quando apertar ESPAÇO
# 3 - mudar a musica 'SDTK2' para 'game-over' quando o player colodir com o monstro
# 4 - quando apertar ESPAÇO para voltar ao menu iniciar novamente  'STDK1

# carregar musicas a sons

#game variables
limite_rolagem = 200
gravidade = 1
plataformas_maximo = 10
rolagem = 0
fundo_rolagem = 0
fundo_rolagem_titulo = 0
game_over = False
score = 0
contador_fade = 0
pulo = False

if os.path.exists('score.txt'):
    with open('score.txt', 'r') as file:
        high_score = int(file.read())
else:
    high_score = 0

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
MARROON = ((115,0,0))
BROWN = (124, 80, 66)
BROWN2 = (169, 110, 93)
BLUE = (115, 221, 228)
BLUE2 = (81, 183, 226)
PANEL = (220, 220, 220)

#define font
font_small = pygame.font.SysFont('Lucida Sans', 20)
font_big = pygame.font.SysFont('Lucida Sans', 24)

#load images
lory_image = pygame.image.load('assets/lory.png').convert_alpha()
bg_image2 = pygame.image.load('assets/BG2.png').convert_alpha()
bg_image1 = pygame.image.load('assets/BG1.png').convert_alpha()
platform_image = pygame.image.load('assets/platform1.png').convert_alpha()
title_image = pygame.image.load('assets/Titulo.png')
#bat spritesheet
bat_sheet_img = pygame.image.load('assets/Jonnie-Spritesheet.png').convert_alpha()
bat_sheet = SpriteSheet(bat_sheet_img)

#function for outputting text onto the tela
def draw_test(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    tela.blit(img, (x, y))

def draw_panel():
    # Create a surface for the panel
    panel_surface = pygame.Surface((tela_largura, 30))
    panel_surface.fill(BLACK)

    # Set the alpha value of the panel surface
    alpha = 128  # Set the alpha value to 128 (out of 255)
    panel_surface.set_alpha(alpha)

    # Draw the panel surface on the tela
    tela.blit(panel_surface, (0, 0))

    # Draw the line on the tela
    pygame.draw.line(tela, WHITE, (0, 30), (tela_largura, 30), 2)
    draw_test('PONTOS: ' + str(score), font_small, WHITE, 10, 0)

def draw_title_bg(fundo_rolagem_titulo):
    tela.blit(bg_image1, (0, 195 + fundo_rolagem_titulo))

#function for drawing the background
def draw_bg(fundo_rolagem):
    tela.blit(bg_image2, (0, 0 + fundo_rolagem))
    tela.blit(bg_image2, (0, -600 + fundo_rolagem))

#class player
class Player():
    def __init__(self, x, y): # x and y are init cordenates of player
        self.image = pygame.transform.scale(lory_image, (35, 45)) #add image in the player and resize
        self.width = 25 # width of rect
        self.height = 40 # height of rect
        self.rect = pygame.Rect(0, 0, self.width, self.height) #create a rect around of the player     
        self.rect.center = (x, y) # posicion the rect
        self.vel_y = 0
        self.flip = False #start fliped to right 

    def draw(self):
        tela.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 10, self.rect.y - 5)) #move some pixels to adjust the rect
        # pygame.draw.rect(tela, WHITE, self.rect, 2)

    def move(self):
        #reset variables
        rolagem = 0
        dx = 0
        dy = 0

        #process keypresses
        key = pygame.key.get_pressed()

        if pulo == True:
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
            if key[pygame.K_SPACE]:
                self.vel_y = 10
        
            #gravidade    
            self.vel_y += gravidade
            dy += self.vel_y
        


        #ensure player doesn't go off the edge of the tela
        if self.rect.left + dx < 0:
            dx = 0 -self.rect.left

        if self.rect.right + dx > tela_largura:
            dx =  tela_largura - self.rect.right

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

        #check if the player has bounced to the top of the tela
        if self.rect.top <= limite_rolagem:
            #if player is pulo
            if self.vel_y < 0:
                rolagem = -dy

        #update rectangule position
        self.rect.x += dx
        self.rect.y += dy + rolagem

        #update mask
        self.mask = pygame.mask.from_surface(self.image)

        return rolagem

#platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, moving):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image, (width, 40))
        self.moving = moving
        self.move_counter = random.randint(0, 50)
        self.direction = random.choice([-1, 1])
        self.speed = random.randint(1, 2)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self, rolagem):
        #moving platform side to side if it is a moving platform
        if self.moving == True:
            self.move_counter += 1
            if score >= 3000:
                self.rect.x += self.direction * self.speed
            else:
                self.rect.x += self.direction

        # change platform direction if it has moved fully or hit a wall
        if self.move_counter >= 100 or self.rect.left < 0 or self.rect.right > tela_largura:
            self.direction *= -1
            self.move_counter = 0

        #update platform's vertical position
        self.rect.y += rolagem

        #check if platform's has gone off the tela
        if self.rect.top > tela_altura:
            self.kill()

#player instance
lory = Player(tela_largura // 2, tela_altura - 75)

#create sprite groups
platform_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

#create starting platforms
platform = Platform(tela_largura // 2 - 50, tela_altura - 50, 100, False)
platform_group.add(platform)

#game loop
run = True
while run: 

    #slow down 
    relogio.tick(FPS)

    if game_over == False:
        #move player
        rolagem = lory.move()

        #draw background
        fundo_rolagem += rolagem
        fundo_rolagem_titulo += rolagem
        if fundo_rolagem >= 600:
            fundo_rolagem = 0
        draw_bg(fundo_rolagem)
        draw_title_bg(fundo_rolagem_titulo)


        #generate platforms
        if len(platform_group) < plataformas_maximo:
            p_w = random.randint(40, 60)
            p_x = random.randint(0, tela_largura - p_w)
            p_y = platform.rect.y - random.randint(80, 120)
            p_type = random.randint(1, 2)
            if p_type == 1 and score > 1500:
                p_moving = True
            else:
                p_moving = False
            platform = Platform(p_x, p_y, p_w, p_moving)
            platform_group.add(platform)

        #update platforms
        platform_group.update(rolagem)


        #generate enemies
        if len(enemy_group) == 0 and score > 1500:
            enemy = Enemy(tela_largura, 30, bat_sheet, 1.5)
            enemy_group.add(enemy )

        #update enemies
        enemy_group.update(rolagem, tela_largura)

        #update score
        if rolagem > 0:
            score += rolagem

        #draw line at previous high score
        pygame.draw.line(tela, WHITE, (0, score - high_score + limite_rolagem), (tela_largura, score - high_score + limite_rolagem), 3)
        draw_test('HIGH SCORE', font_small, WHITE, tela_largura - 130, score - high_score + limite_rolagem)

        #draw sprites
        platform_group.draw(tela)
        enemy_group.draw(tela)
        lory.draw()

        if pulo == False:
            draw_test('PRESSIONE ESPAÇO', font_small, WHITE, 100, 360)
            draw_test('PARA COMEÇAR O JOGO', font_small, WHITE, 80, 390)
            tela.blit(title_image, (75, 20))
        else:
             #draw panel
            draw_panel()

        #check game over
        if lory.rect.top > tela_altura:
            game_over = True
        #check for collision with enemies
        if pygame.sprite.spritecollide(lory, enemy_group, False):
            if pygame.sprite.spritecollide(lory, enemy_group, False, pygame.sprite.collide_mask):
                game_over = True
    else:
        if contador_fade < tela_largura:
            contador_fade += 5
            for y in range(0, 6, 2):
                pygame.draw.rect(tela, BLUE2, (0, y * 100, contador_fade, 100))
                pygame.draw.rect(tela, BLUE2, (tela_largura - contador_fade, (y + 1) * 100, tela_largura, 100))
        else:  
            draw_test('GAME OVER!', font_big, WHITE, 130, 200)
            draw_test('PONTOS: ' + str(score), font_big, WHITE, 120, 250)
            draw_test('APERTE ESPAÇO PARA', font_small, WHITE, 90, 500)
            draw_test('VOLTAR AO MENU', font_small, WHITE, 110, 530)
            #update high score
            if score > high_score:
                high_score = score
                with open('score.txt', 'w') as file:
                    file.write(str(high_score))
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                #reset variables
                game_over = False
                score = 0
                rolagem = 0
                contador_fade = 0
                pulo = False
                fundo_rolagem_titulo = 0
                #reposition loryh
                lory.rect.center = (tela_largura // 2, tela_altura - 75)
                #reset enemies
                enemy_group.empty()
                #reset platforms
                platform_group.empty()
                #create starting platforms
                platform = Platform(tela_largura // 2 - 50, tela_altura - 50, 100, False)
                platform_group.add(platform)


    #event handler
    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE and pulo == False:
                pulo = True
        if e.type == pygame.QUIT:
            #update high score
            if score > high_score:
                high_score = score
                with open('score.txt', 'w') as file:
                    file.write(str(high_score))
            run = False


    #update display pygame
    pygame.display.update()

pygame.quit()