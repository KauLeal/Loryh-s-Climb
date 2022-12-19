import pygame
import random
import os
from pygame import mixer
from spritesheet import SpriteSheet
from enemy import Enemy

mixer.init()
pygame.init()

tela_largura = 400
tela_altura = 600

tela = pygame.display.set_mode((tela_largura, tela_altura))
pygame.display.set_caption("Loryh's Climb")

#definir frame rate
relogio = pygame.time.Clock()
FPS = 60

#carregar música e sons
musica_menu = pygame.mixer.Sound('som/SDTK1.mp3')
musica_menu.set_volume(0.4)
musica_jogo = pygame.mixer.Sound('som/SDTK2.mp3')
musica_jogo.set_volume(0.4)
som_pulo = pygame.mixer.Sound('som/pulo.mp3')

#game variables
limite_rolagem = 200
gravidade = 1
plataformas_maximo = 10
rolagem = 0
fundo_rolagem = 0
fundo_rolagem_titulo = 0
fim_jogo = False
pontos = 0
contador_fade = 0
pulo = False

if os.path.exists('score.txt'):
    with open('score.txt', 'r') as file:
        high_score = int(file.read())
else:
    high_score = 0

#colors
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (81, 183, 226)

#define font
fonte_pequena = pygame.font.SysFont('Lucida Sans', 20)
font_big = pygame.font.SysFont('Lucida Sans', 24)
 
#load images
imagem_lory = pygame.image.load('assets/lory.png').convert_alpha()
imagem_montanha_subir = pygame.image.load('assets/BG2.png').convert_alpha()
imagem_montanha = pygame.image.load('assets/BG1.png').convert_alpha()
imagem_plataforma = pygame.image.load('assets/platform1.png').convert_alpha()
imagem_titulo = pygame.image.load('assets/Titulo.png')

#jonnie spritesheet
jonnie_sheet_imagem = pygame.image.load('assets/Jonnie-Spritesheet.png').convert_alpha()
jonnie_sheet = SpriteSheet(jonnie_sheet_imagem)

#function for outputting text onto the tela
def escrever_texto(text, font, text_col, x, y):
    imagem = font.render(text, True, text_col)
    tela.blit(imagem, (x, y))

def desenhar_painel_pontos():
    # Create a surface for the panel
    superficie_painel = pygame.Surface((tela_largura, 30))
    superficie_painel.fill(PRETO)

    # Set the alpha value of the panel surface
    alpha = 128  # Set the alpha value to 128 (out of 255)
    superficie_painel.set_alpha(alpha)

    # Draw the panel surface on the tela
    tela.blit(superficie_painel, (0, 0))

    # Draw the line on the tela
    pygame.draw.line(tela, BRANCO, (0, 30), (tela_largura, 30), 2)
    escrever_texto('PONTOS: ' + str(pontos), fonte_pequena, BRANCO, 10, 0)

def draw_title_bg(fundo_rolagem_titulo):
    tela.blit(imagem_montanha, (0, 195 + fundo_rolagem_titulo))

#function for drawing the background
def desenhar_fundo(fundo_rolagem):
    tela.blit(imagem_montanha_subir, (0, 0 + fundo_rolagem))
    tela.blit(imagem_montanha_subir, (0, -600 + fundo_rolagem))

#class Jogador
class Jogador():
    def __init__(self, x, y): # x and y are init cordenates of Jogador
        self.image = pygame.transform.scale(imagem_lory, (35, 45)) #add image in the Jogador and resize
        self.width = 25 # width of rect
        self.height = 40 # height of rect
        self.rect = pygame.Rect(0, 0, self.width, self.height) #create a rect around of the Jogador     
        self.rect.center = (x, y) # posicion the rect
        self.vel_y = 0
        self.flip = False #start fliped to right 

    def desenhar(self):
        tela.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 10, self.rect.y - 5)) #move some pixels to adjust the rect
        # pygame.draw.rect(tela, BRANCO, self.rect, 2)

    def mover(self):
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
        


        #ensure Jogador doesn't go off the edge of the tela
        if self.rect.left + dx < 0:
            dx = 0 -self.rect.left

        if self.rect.right + dx > tela_largura:
            dx =  tela_largura - self.rect.right

        #check collision with platforms
        for plataforma in grupo_plataforma:
            #collision in the y direction
            if plataforma.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if above the platform
                if self.rect.bottom < plataforma.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = plataforma.rect.top
                        dy = 0
                        self.vel_y = -20
                        som_pulo.play()

        #check if the Jogador has bounced to the top of the tela
        if self.rect.top <= limite_rolagem:
            #if Jogador is pulo
            if self.vel_y < 0:
                rolagem = -dy

        #update rectangule position
        self.rect.x += dx
        self.rect.y += dy + rolagem

        #update mask
        self.mask = pygame.mask.from_surface(self.image)

        return rolagem

#platform class
class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, width, moving):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(imagem_plataforma, (width, 40))
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
            if pontos >= 3000:
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

#Jogador instance
lory = Jogador(tela_largura // 2, tela_altura - 75)

#create sprite groups
grupo_plataforma = pygame.sprite.Group()
grupo_inimigos = pygame.sprite.Group()

#create starting platforms
plataforma = Plataforma(tela_largura // 2 - 50, tela_altura - 50, 100, False)
grupo_plataforma.add(plataforma)

#game loop
iniciar_jogo = True
musica_menu.play(-1)
while iniciar_jogo: 

    #slow down 
    relogio.tick(FPS)

    if fim_jogo == False:
        #move Jogador
        rolagem = lory.mover()

        #draw background
        fundo_rolagem += rolagem
        fundo_rolagem_titulo += rolagem
        if fundo_rolagem >= 600:
            fundo_rolagem = 0
        desenhar_fundo(fundo_rolagem)
        draw_title_bg(fundo_rolagem_titulo)


        #generate platforms
        if len(grupo_plataforma) < plataformas_maximo:
            p_w = random.randint(40, 60)
            p_x = random.randint(0, tela_largura - p_w)
            p_y = plataforma.rect.y - random.randint(80, 120)
            p_type = random.randint(1, 2)
            if p_type == 1 and pontos > 1500:
                p_moving = True
            else:
                p_moving = False
            plataforma = Plataforma(p_x, p_y, p_w, p_moving)
            grupo_plataforma.add(plataforma)

        #update platforms
        grupo_plataforma.update(rolagem)


        #generate enemies
        if len(grupo_inimigos) == 0 and pontos > 1500:
            enemy = Enemy(tela_largura, 30, jonnie_sheet, 1.5)
            grupo_inimigos.add(enemy )

        #update enemies
        grupo_inimigos.update(rolagem, tela_largura)

        #update score
        if rolagem > 0:
            pontos += rolagem

        #draw line at previous high score
        pygame.draw.line(tela, BRANCO, (0, pontos - high_score + limite_rolagem), (tela_largura, pontos - high_score + limite_rolagem), 3)
        escrever_texto('HIGH SCORE', fonte_pequena, BRANCO, tela_largura - 130, pontos - high_score + limite_rolagem)

        #draw sprites
        grupo_plataforma.draw(tela)
        grupo_inimigos.draw(tela)
        lory.desenhar()

        if pulo == False:
            escrever_texto('PRESSIONE ESPAÇO', fonte_pequena, BRANCO, 100, 360)
            escrever_texto('PARA COMEÇAR O JOGO', fonte_pequena, BRANCO, 80, 390)
            tela.blit(imagem_titulo, (75, 20))
        else:
             #draw panel
            desenhar_painel_pontos()

        #check game over
        if lory.rect.top > tela_altura:
            fim_jogo = True
        #check for collision with enemies
        if pygame.sprite.spritecollide(lory, grupo_inimigos, False):
            if pygame.sprite.spritecollide(lory, grupo_inimigos, False, pygame.sprite.collide_mask):
                fim_jogo = True
    else:
        if contador_fade < tela_largura:
            contador_fade += 5
            for y in range(0, 6, 2):
                pygame.draw.rect(tela, AZUL, (0, y * 100, contador_fade, 100))
                pygame.draw.rect(tela, AZUL, (tela_largura - contador_fade, (y + 1) * 100, tela_largura, 100))
        else:  
            escrever_texto('GAME OVER!', font_big, BRANCO, 130, 200)
            escrever_texto('PONTOS: ' + str(pontos), font_big, BRANCO, 120, 250)
            escrever_texto('APERTE ESPAÇO PARA', fonte_pequena, BRANCO, 90, 500)
            escrever_texto('VOLTAR AO MENU', fonte_pequena, BRANCO, 110, 530)
            #update high score
            if pontos > high_score:
                high_score = pontos
                with open('score.txt', 'w') as file:
                    file.write(str(high_score))
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                #reset variables
                fim_jogo = False
                pontos = 0
                rolagem = 0
                contador_fade = 0
                pulo = False
                fundo_rolagem_titulo = 0
                #reposition loryh
                lory.rect.center = (tela_largura // 2, tela_altura - 75)
                #reset enemies
                grupo_inimigos.empty()
                #reset platforms
                grupo_plataforma.empty()
                #create starting platforms
                plataforma = Plataforma(tela_largura // 2 - 50, tela_altura - 50, 100, False)
                grupo_plataforma.add(plataforma)


    #event handler
    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE and pulo == False:
                pulo = True
                musica_menu.stop()
                musica_jogo.play(-1)
        if e.type == pygame.QUIT:
            #update high score
            if pontos > high_score:
                high_score = pontos
                with open('score.txt', 'w') as file:
                    file.write(str(high_score))
            iniciar_jogo = False


    #update display pygame
    pygame.display.update()

pygame.quit()