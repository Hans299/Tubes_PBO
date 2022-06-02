import math
import pygame, sys
import random
import image
import sound
from helper import draw_text

FPS=60
WIDTH=500
HEIGHT=600
GREEN = (0, 255, 0)
#class pygame (Class Utama/Parent)
pygame.init()
layar = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("WATCHOUT!")
fps = pygame.time.Clock()

#Class Player(Class Child)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(image.player,(60,65))
        self.rect=self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom=HEIGHT - 20
        self.speedx = 8
        self.score_val = 0
        self.life = 5
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 250
    #artibuted movement
    def update(self):
        
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > 5000:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
            
        key_pressed = pygame.key.get_pressed()
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

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(pygame.Vector2(self.rect.centerx,self.rect.top))
                all_sprites.add(bullet)
                bullets.add(bullet)
                sound.missile.play()
            elif self.power >= 2:
                bullet1 = Bullet(pygame.Vector2(self.rect.centerx-20,self.rect.top))
                all_sprites.add(bullet1)
                bullets.add(bullet1)
                bullet2 = Bullet(pygame.Vector2(self.rect.centerx+20,self.rect.top))
                all_sprites.add(bullet2)
                bullets.add(bullet2)
                sound.missile.play()  
    
    def show_lifepoints(self):
        draw_text(layar, f"life points -> {self.life}", 24, WIDTH-70, HEIGHT-590)

    def show_score(self):
        draw_text(layar, f"Score -> {self.score_val}", 24, WIDTH-450, HEIGHT-590)

#Class Bullet(Class Child)
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(image.rock,(43,42))
        self.rect=self.image.get_rect()
        self.radius=self.rect.width*0.1/2
        self.rect.x=random.randrange(0,WIDTH-self.rect.width)
        self.rect.y=random.randrange(-50,-10)
        self.speedx=random.randrange(-1,2)
        self.speedy=random.randrange(1,2)
#Atributed movement
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT or self.rect.left>WIDTH or self.rect.right<0:
            self.rect.x=random.randrange(0,WIDTH-self.rect.width)
            self.rect.y=random.randrange(-100,-40)
            self.speedx=random.randrange(-3,3)
            self.speedy=random.randrange(2,8)
#Class Powerup(Class Child)
class Power(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image.power,(20,20))
        self.rect = self.image.get_rect()
        self.radius=self.rect.width*0.1/2
        self.rect.x=random.randrange(0,WIDTH-self.rect.width)
        self.speedy = 5
#Atributed movement
    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.top > HEIGHT:
            self.kill()
#Class Bullet(Class Child)
class Bullet(pygame.sprite.Sprite):
    def __init__(self,position:pygame.Vector2,angle:float=-90):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.rotate(pygame.transform.scale(image.bullet,(10,50)),-angle+180+90)
        self.rect=self.image.get_rect()
        self.rect.midbottom=position
        speedy = 10
        self.velocity = pygame.math.Vector2(math.cos(math.radians(angle))*speedy,math.sin(math.radians(angle))*speedy)

    def update(self):
        self.rect.midbottom += self.velocity
        if self.rect.bottom < 0 or self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.kill()
#Class Healthbar(Class Child)
#Implementasi Polymorphism
class Healthbar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((WIDTH*4/5, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = 80
#Class Boss(Class Child)
class Boss(pygame.sprite.Sprite):
    def __init__(self, max_health:int, attack_speed:int = 50):
        pygame.sprite.Sprite.__init__(self)
        self.source_image = pygame.transform.rotate(pygame.transform.scale(image.boss,(120,130)),90)
        self._angle = 180
        self.image = pygame.transform.rotate(self.source_image, self.angle)
        self.rect=self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom  = 0

        self.max_health = max_health
        self._health = 0
        self.healthbar = Healthbar()
        self.health = self.max_health
        self.move_in = pygame.Vector2(0,15)
        all_sprites.add(self.healthbar)
        self.tick = 0
        self.alt = False
        self.attack_speed = attack_speed
#Static Method
    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = value
        self.healthbar.image.fill((255,0 , 0))
        self.healthbar.image.fill((0, 255, 0), (0, 0, self.healthbar.image.get_width()*self.health/self.max_health, self.healthbar.image.get_height()))

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        if value != self._angle:
            self._angle = value
            self.on_angle_change()

    def on_angle_change(self):
        self.image = pygame.transform.rotate(self.source_image, self.angle)

    def hurt(self, value:int = 10):
        self.health -= value
        if self.health <= 0:
            self.kill()
            self.healthbar.kill()


    def shoot(self):
        self.alt = not self.alt
        if self.alt:
            bullet = Bullet(pygame.Vector2(self.rect.centerx-30,self.rect.bottom), -self.angle)
        else :
            bullet = Bullet(pygame.Vector2(self.rect.centerx+30,self.rect.bottom), -self.angle)
        all_sprites.add(bullet)
        hazard.add(bullet)
        

    def update(self):
        self.rect.y += self.move_in.y
        if self.move_in.y > 0:
            self.move_in.y *= 0.95

        self.tick += 1

        p_center = player.rect.center
        s_center = self.rect.center
        angle_in_rads = math.atan2(p_center[1] - s_center[1], p_center[0] - s_center[0])

        self.angle = -math.degrees(angle_in_rads)
        if self.tick > self.attack_speed:
            self.tick = 0
            self.shoot()

    def kill(self):
        self.healthbar.kill()
        return super().kill()
        

#Tampilan kedua setelah menu()
def waiting_screen():
    layar.blit(pygame.transform.scale(image.background,(500,700)),(0,0))
    draw_text(layar, "WATCHOUT!", 70, WIDTH/2, HEIGHT/4)
    draw_text(layar, "Arrow keys to move, Space key to fire", 20, WIDTH/2, HEIGHT/2)
    draw_text(layar, "Press any key to play", 22, WIDTH/2, HEIGHT*3/4)
    pygame.display.flip()
    waiting = True
    while waiting:
        fps.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False
#Tampilan awal
def menu():
    layar.blit(pygame.transform.scale(image.background,(500,700)),(0,0))
    draw_text(layar, "WATCHOUT!", 70, WIDTH/2, HEIGHT/4)    
    pygame.display.flip()
    yvar=350
    xvar=250
    draw_text(layar, "START", 60, WIDTH/2, yvar-30) 
    draw_text(layar, "QUIT",40, WIDTH/2, 500)  
    pygame.draw.circle(layar, (GREEN), (xvar,yvar), 70,6)
    
    waiting = True
    while waiting:
        fps.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                xpos, ypos = pygame.mouse.get_pos()
                cek = math.sqrt((xvar - xpos)**2 + (yvar - ypos)**2)
                if cek <= 70:
                    waiting = False
                    waiting_screen()
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                xpos, ypos = pygame.mouse.get_pos()
                cek = math.sqrt((xvar - xpos)**2 + (520 - ypos)**2)
                if cek <= 25:
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

#Tampilan ketika GameOver
def menuGameOver():
    layar.blit(pygame.transform.scale(image.background,(500,700)),(0,0))
    draw_text(layar, "Game Over", 70, WIDTH/2, HEIGHT/4)    

    yvar=350
    xvar=250
    
    draw_text(layar, "START", 60, WIDTH/2, yvar-30)
    draw_text(layar, f"Your score : {player.score_val}", 30, WIDTH/2, 223)
    draw_text(layar, "QUIT",40, WIDTH/2, 500) 
    pygame.draw.circle(layar, (GREEN), (xvar,yvar), 70,6)
    
    waiting = True
    while waiting:
        fps.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                xpos, ypos = pygame.mouse.get_pos()
                cek = math.sqrt((xvar - xpos)**2 + (yvar - ypos)**2)
                if cek <= 70:
                    player.score_val = 0
                    waiting = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                xpos, ypos = pygame.mouse.get_pos()
                cek = math.sqrt((xvar - xpos)**2 + (520 - ypos)**2)
                if cek <= 25:
                    pygame.quit()
                    sys.exit()
                    
        pygame.display.update()
        

game_over = True
running=True
menu()
hp = 0
sound.bgmusic.play(loops=-1)        
while running:
    fps.tick(FPS)
    # waiting screen ketika gameover dan akan memulai game
    if game_over:
        game_over = False
        all_sprites = pygame.sprite.Group()
        hazard = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player = Player()
        level = 1

        all_sprites.add(player)

        for i in range(4):
            rock=Rock()
            all_sprites.add(rock)
            hazard.add(rock)
        player.score_val = 0
        # Test boss
        # if player.score_val % 100 == 0:
        #     test = Boss(100)
        #     all_sprites.add(test)
        #     hazard.add(test)
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
            pygame.quit()
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE: # keyboard spasi untuk menembak
                player.shoot()
            elif event.key==pygame.K_1: #cheat menambah skor dengan keyboard angka 1
                player.score_val +=1
            elif event.key==pygame.K_2: #shorcut untuk langsung game over dengan keyboard angka 2
                menuGameOver()  
                game_over = True
            elif event.key==pygame.K_3: #cheat menambah peluru menjadi 2 dengan keyboard angka 3
                player.power=2
                player.shoot()
            elif event.key==pygame.K_4: #cheat menambah skor +25 dengan keyboard angka 4
                player.score_val +=25
                
        
                

    all_sprites.update()
    hits=pygame.sprite.groupcollide(hazard,bullets,False,True)

    for hit in hits:
        # cek apakah peluru mengenai batu
        if isinstance(hit, Rock):
            sound.exlp2.play()
            hit.kill()
            rock=Rock()
            all_sprites.add(rock)
            hazard.add(rock)
            player.score_val +=1
            
            if player.score_val % 30 == 0:
                hp += 50 #setiap skor kelipatan 30 HP Boss bertambah 50
                boss = Boss(hp)
                all_sprites.add(boss)
                hazard.add(boss)
                player.powerup()
                level += 1
                player.life += 1
            elif player.score_val % 10 == 0:
                power=Power()
                all_sprites.add(power)
                hazard.add(power)
            
        # cek apakah peluru mengenai Boss        
        elif isinstance(hit, Boss): 
            sound.exlp2.play()
            hit.hurt()
            
        
    # ketika level levih dari 2 rock meluncur lebih cepat
    if level >= 2:
        rock.speedx=random.randrange(-5,1)
        rock.speedy=random.randrange(5,10)
        
    layar.blit(pygame.transform.scale(image.background,(500,700)),(0,0))
    draw_text(layar, f"Level {level}", 24, WIDTH/2, HEIGHT-590)
    all_sprites.draw(layar)
    player.show_score()
    player.show_lifepoints()
    pygame.display.update()

    hits = pygame.sprite.spritecollide(player,hazard,False,pygame.sprite.collide_circle)
    # jika pesawat terkena hit, life akan berkurang
    for hit in hits:
        if isinstance(hit, Rock):
            sound.expl.play()
            hit.kill()
            rock=Rock()
            all_sprites.add(rock)
            hazard.add(rock)
            player.life -= 1
        elif isinstance(hit, Bullet):
            sound.expl.play()
            hit.kill()
            player.life -= 1
        else:
            hit.kill()
            sound.powerup.play()
            player.powerup()
             
        if player.life < 0:
            game_over = True
            menuGameOver() 
        
        
pygame.quit()