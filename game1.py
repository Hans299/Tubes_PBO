import pygame
import random
import os
from pygame import mixer


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


font = pygame.font.Font("freesansbold.ttf", 24)
text_x = 10
text_y = 10


background_img=pygame.image.load(os.path.join("pygame","image","background.jpg"))
bullet_img=pygame.image.load(os.path.join("pygame","image","bullet.png"))
player_img=pygame.image.load(os.path.join("pygame","image","player.png"))
rock_img=pygame.image.load(os.path.join("pygame","image","rock.png"))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.image=pygame.transform.scale(player_img,(50,50))
        self.rect=self.image.get_rect()
        self.rect.centerx=WIDTH/2
        self.rect.bottom=HEIGHT-10
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
        if self.rect.left <0:
            self.rect.left=0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top <0:
            self.rect.top  = 0 

    def shoot(self):
        bullet = Bullet(self.rect.centerx,self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        
    def show_score(self):
        score = font.render(f"Score: {self.score_val}", True, (255, 255, 255))
        screen.blit(score, (text_x, text_y))


class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(rock_img,(43,42))
        
        self.rect=self.image.get_rect()
        self.speedx=random.randrange(-1,2)
        self.speedy=random.randrange(1,2)
        

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT or self.rect.left>WIDTH or self.rect.right<0:
            self.speedx=random.randrange(-3,3)
            self.speedy=random.randrange(2,10)


class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(bullet_img,(28,42.5))
        self.rect=self.image.get_rect()
        self.rect.centerx=x
        self.rect.bottom=y
        self.speedy=-10
        

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
           self.kill()


all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(4):
    rock = Rock()
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
                missile_sound = mixer.Sound("./pygame/audio/missile.wav")
                missile_sound.play()
                player.shoot()
                
    
    all_sprites.update()
    
    hits=pygame.sprite.groupcollide(rocks,bullets,True,True)
    
    for hit in hits:
        rock=Rock()
        all_sprites.add(rock)
        rocks.add(rock)
        player.score_val +=1

    
    
    screen.blit(pygame.transform.scale(background_img,(500,600)),(0,0))
    all_sprites.draw(screen)
    player.show_score()
    pygame.display.update()

pygame.quit()