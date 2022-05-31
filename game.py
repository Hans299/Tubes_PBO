import math
import pygame
import random
import image
import sound

from pygame import mixer
from helper import draw_text

FPS=60
WIDTH=500
HEIGHT=600
GREEN = (0, 255, 0)

pygame.init()
layar = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("WATCHOUT!")
fps = pygame.time.Clock()
tittle_font = pygame.font.SysFont("dejavuserif",40)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(image.player,(60,65))
        self.rect=self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom=HEIGHT - 20
        self.speedx = 8
        self.score_val = 0

    def update(self):
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

    def shoot(self):
        bullet = Bullet(pygame.Vector2(self.rect.centerx-20,self.rect.top))
        all_sprites.add(bullet)
        bullets.add(bullet)
        sound.missile.play()

    def doubleshoot(self):
        bullet1 = Bullet(pygame.Vector2(self.rect.centerx-20,self.rect.top))
        all_sprites.add(bullet1)
        bullets.add(bullet1)
        bullet2 = Bullet(pygame.Vector2(self.rect.centerx+20,self.rect.top))
        all_sprites.add(bullet2)
        bullets.add(bullet2)

    def show_score(self):
        draw_text(layar, f"Score -> {self.score_val}", 24, WIDTH-450, HEIGHT-590)

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

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT or self.rect.left>WIDTH or self.rect.right<0:
            self.rect.x=random.randrange(0,WIDTH-self.rect.width)
            self.rect.y=random.randrange(-100,-40)
            self.speedx=random.randrange(-3,3)
            self.speedy=random.randrange(2,8)

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

class Healthbar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Create a surface with the size of the player
        self.image = pygame.Surface((WIDTH*4/5, 10))
        # Set the color of the surface
        self.image.fill((255, 0, 0))
        # Create a rectangle with the size of the surface
        self.rect = self.image.get_rect()
        # Set the position of the rectangle
        self.rect.centerx = WIDTH/2
        self.rect.bottom = 80

class Boss(pygame.sprite.Sprite):
    def __init__(self, max_health:int, attack_speed:int = 50):
        pygame.sprite.Sprite.__init__(self)
        self.source_image = pygame.transform.rotate(
            pygame.transform.scale(image.player,(120,130)),
            -90
        )
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
            # sound.explosion.play()
            # self.explosion()

    def shoot(self):
        self.alt = not self.alt
        if self.alt:
            bullet = Bullet(pygame.Vector2(self.rect.centerx-30,self.rect.bottom), -self.angle)
        else :
            bullet = Bullet(pygame.Vector2(self.rect.centerx+30,self.rect.bottom), -self.angle)
        all_sprites.add(bullet)
        hazard.add(bullet)
        print('Boss shoot angle', self.angle)

    def update(self):
        # Always face the player
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

    # Before killed
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
            if event.type == pygame.KEYUP:
                waiting = False
#Tampilan awal
def menu():
    layar.blit(pygame.transform.scale(image.background,(500,700)),(0,0))
    draw_text(layar, "WATCHOUT!", 70, WIDTH/2, HEIGHT/4)    
    pygame.display.flip()
    yvar=350
    xvar=250
    waiting = True
    while waiting:
        fps.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                xpos, ypos = pygame.mouse.get_pos()
                cek = math.sqrt((xvar - xpos)**2 + (yvar - ypos)**2)
                if cek <= 70:
                    waiting = False
                    waiting_screen()
                    return False

        draw_text(layar, "START", 60, WIDTH/2, yvar-30)
            
        pygame.draw.circle(layar, (GREEN), (xvar,yvar), 70,6)
        pygame.display.update()

#Tampilan ketika GameOver
def menuGameOver():
    layar.blit(pygame.transform.scale(image.background,(500,700)),(0,0))
    draw_text(layar, "Game Over", 70, WIDTH/2, HEIGHT/4)    
    pygame.display.flip()
    yvar=350
    xvar=250
    waiting = True
    while waiting:
        fps.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                xpos, ypos = pygame.mouse.get_pos()
                cek = math.sqrt((xvar - xpos)**2 + (yvar - ypos)**2)
                if cek <= 70:
                    player.score_val = 0
                    waiting = False

        draw_text(layar, "START", 60, WIDTH/2, yvar-30)

        score = tittle_font.render(f"Your score : {player.score_val}", 1, (GREEN))
        layar.blit(score, (WIDTH/2 - score.get_width()/2, yvar-120))
            
        pygame.draw.circle(layar, (GREEN), (xvar,yvar), 70,6)
        pygame.display.update()

game_over = True
running=True
level = 1

while running:
    fps.tick(FPS)

    # waiting screen ketika gameover dan akan memulai game
    if game_over:
        menu()
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
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE: # keyboard spasi untuk menembak
                player.shoot()
            elif event.key==pygame.K_1: #cheat menambah skor dengan keyboard angka 1
                player.score_val +=1
            elif event.key==pygame.K_4: #cheat menambah skor +30 dengan keyboard angka 2
                player.score_val +=30
            elif event.key==pygame.K_3: #cheat menambah peluru menjadi 2
                missile_sound = mixer.Sound("./audio/missile.wav")
                missile_sound.play()
                player.doubleshoot()
        elif event.type==pygame.KEYUP: #shortcut untuk langsung gameover
            if event.key==pygame.K_2:
                menuGameOver()  
                game_over = True
                running = True

    all_sprites.update()
    hits=pygame.sprite.groupcollide(hazard,bullets,False,True)

    for hit in hits:
        # Check if the hit is a rock
        if isinstance(hit, Rock):
            hit.kill()
            rock=Rock()
            all_sprites.add(rock)
            hazard.add(rock)
            player.score_val +=1
            if player.score_val % 50 == 0:
                test = Boss(100)
                all_sprites.add(test)
                hazard.add(test)
                level += 1
        elif isinstance(hit, Boss):
            hit.hurt()
        else:
            hit.kill()

    hits = pygame.sprite.spritecollide(player,hazard,False,pygame.sprite.collide_circle)
    # jika pesawat terkena meteor
    if hits:
        menuGameOver()  
        game_over = True
        running = True

    layar.blit(pygame.transform.scale(image.background,(500,700)),(0,0))
    all_sprites.draw(layar)
    player.show_score()
    draw_text(layar, f"Level {level}", 24, WIDTH/2, HEIGHT-590)
    pygame.display.update()

pygame.quit()