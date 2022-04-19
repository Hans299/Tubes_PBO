from email.mime import image
from numpy import imag
import pygame
import random
import os

FPS=60
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
WIDTH=500
HEIGHT=600


pygame.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Watchout!!")
clock=pygame.time.Clock()


background_img=pygame.image.load(os.path.join("pygame","image","background.png")).convert()
bullet_img=pygame.image.load(os.path.join("pygame","image","bullet.PNG")).convert()
player_img=pygame.image.load(os.path.join("pygame","image","player.PNG")).convert()
rock_img=pygame.image.load(os.path.join("pygame","image","rock.PNG")).convert()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(player_img,(50,50))
        
        self.rect=self.image.get_rect()
        self.radius=22
        pygame.draw.circle(self.image,GREEN,self.rect.center, self.radius)
        self.rect.centerx=WIDTH/2
        self.rect.bottom=HEIGHT-10
        self.speedx=8

    def update(self):
        key_pressed=pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]: 
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx

        if self.rect.right >WIDTH:
            self.rect.right=WIDTH
        if self.rect.left <0:
            self.rect.left=0

    def shoot(self):
        bullet=Bullet(self.rect.centerx,self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(rock_img,(43,42))
        self.image.set_colorkey(WHITE)
        self.rect=self.image.get_rect()
        self.radius=self.rect.width*0.9/2
        #pygame.draw.circle(self.image,GREEN,self.rect.center, self.radius)
        self.rect.x=random.randrange(0,WIDTH-self.rect.width)
        self.rect.y=random.randrange(-100,-40)
        self.speedx=random.randrange(-3,3)
        self.speedy=random.randrange(2,6)
        

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT or self.rect.left>WIDTH or self.rect.right<0:
            self.rect.x=random.randrange(0,WIDTH-self.rect.width)
            self.rect.y=random.randrange(-100,-40)
            self.speedx=random.randrange(-3,3)
            self.speedy=random.randrange(2,10)


class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(bullet_img,(28,42.5))
        self.image.set_colorkey(WHITE)
        self.rect=self.image.get_rect()
        self.rect.centerx=x
        self.rect.bottom=y
        self.speedy=-10
        

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom <0:
           self.kill()


all_sprites=pygame.sprite.Group()
rocks=pygame.sprite.Group()
bullets=pygame.sprite.Group()
player=Player()
all_sprites.add(player)
for i in range(8):
    rock=Rock()
    all_sprites.add(rock)
    rocks.add(rock)


running=True
while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                player.shoot()
    
    all_sprites.update()
    hits=pygame.sprite.groupcollide(rocks,bullets,True,True)
    for hit in hits:
        rock=Rock()
        all_sprites.add(rock)
        rocks.add(rock)

    hits=pygame.sprite.spritecollide(player,rocks,False,pygame.sprite.collide_circle)
    if hits:
        running=False
    
    
    screen.fill(WHITE)
    screen.blit(pygame.transform.scale(background_img,(500,700)),(0,0))
    all_sprites.draw(screen)
    pygame.display.update()

pygame.quit()