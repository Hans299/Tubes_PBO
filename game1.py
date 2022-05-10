import pygame
import random
import os
from pygame import mixer


FPS=60
WIDTH=500
HEIGHT=600
GREEN = (0, 255, 0)



pygame.init()
layar = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("WATCHOUT!")
fps = pygame.time.Clock()


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font('jupiterc.ttf', size)
    text_surface = font.render(text, True, GREEN)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

background_img=pygame.image.load(os.path.join("image","background.jpg"))
bullet_img=pygame.image.load(os.path.join("image","bullet.PNG"))
player_img=pygame.image.load(os.path.join("image","player.PNG"))
rock_img=pygame.image.load(os.path.join("image","rock.PNG"))


class Player(pygame.sprite.Sprite):
    def _init_(self):
        pygame.sprite.Sprite._init_(self) 
        self.image=pygame.transform.scale(player_img,(50,50))
        self.rect=self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom=HEIGHT - 20
        self.speedx = 8
        self.score_val = 0

    def update(self):
        key_pressed=pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]: 
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        if key_pressed[pygame.K_UP]:
            self.rect.y -= self.speedx
        if key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speedx

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top  = 0 

    def shoot(self):
        bullet = Bullet(self.rect.centerx,self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        
    def show_score(self):
        draw_text(layar, f"Score -> {self.score_val}", 24, WIDTH-450, HEIGHT-590)
        


class Rock(pygame.sprite.Sprite):
    def _init_(self):
        pygame.sprite.Sprite._init_(self)
        self.image=pygame.transform.scale(rock_img,(43,42))
        
        self.rect=self.image.get_rect()
        self.radius=self.rect.width*0.9/2
        self.rect.x=random.randrange(0,WIDTH-self.rect.width)
        self.rect.y=random.randrange(-50,-10)
        self.speedx=random.randrange(-1,2)
        self.speedy=random.randrange(1,2)
        

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT or self.rect.left>WIDTH or self.rect.right<0:
            self.rect.x=random.randrange(0,WIDTH-self.rect.width)
            self.rect.y=random.randrange(-100,-40)
            self.speedx=random.randrange(-3,3)
            self.speedy=random.randrange(2,8)


class Bullet(pygame.sprite.Sprite):
    def _init_(self,x,y):
        pygame.sprite.Sprite._init_(self)
        self.image=pygame.transform.scale(bullet_img,(28,42))
        self.rect=self.image.get_rect()
        self.rect.centerx=x
        self.rect.bottom=y
        self.speedy = -10 

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
           self.kill()

def show_go_screen():
    layar.blit(pygame.transform.scale(background_img,(500,700)),(0,0))
    draw_text(layar, "WATCHOUT!", 70, WIDTH / 2, HEIGHT / 4)
    draw_text(layar, "Arrow keys to move, Space key to fire", 20, WIDTH / 2, HEIGHT / 2)
    draw_text(layar, "Press any key to play", 22, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        fps.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


'''all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()

all_sprites.add(player)

for i in range(8):
    rock=Rock()
    all_sprites.add(rock)
    rocks.add(rock)'''

game_over = True
running=True
while running:
    fps.tick(FPS)
    
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player = Player()

        all_sprites.add(player)

        for i in range(8):
            rock=Rock()
            all_sprites.add(rock)
            rocks.add(rock)
        player.score_val = 0
     
     
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE: #keyboard spasi untuk menembak
                missile_sound = mixer.Sound("./audio/missile.wav")
                missile_sound.play()
                player.shoot()
            elif event.key==pygame.K_1: #cheat menambah skor dengan keyboard angka 1
                player.score_val +=1
        elif event.type==pygame.KEYUP: #shortcut untuk langsung gameover
            if event.key==pygame.K_2:
                game_over = True
                    
            
    
    all_sprites.update()
    hits=pygame.sprite.groupcollide(rocks,bullets,True,True)
    

    for hit in hits:
        rock=Rock()
        all_sprites.add(rock)
        rocks.add(rock)
        player.score_val +=1

                
    hits = pygame.sprite.spritecollide(player,rocks,False,pygame.sprite.collide_circle)
    #jika pesawat terkena meteor 
    if hits:
        game_over=True        
        
    
    
    layar.blit(pygame.transform.scale(background_img,(500,700)),(0,0))
    all_sprites.draw(layar)
    player.show_score()
    pygame.display.update()

pygame.quit()