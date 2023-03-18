import pygame
from random import randint
pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((700,500))
FPS = 60
pygame.display.set_caption('Shooter')
rocket = pygame.image.load('rocket.png')
enemy_img = pygame.image.load('ufo.png')
asteroid_img = pygame.image.load('asteroid.png')
bullet_img = pygame.image.load('Bullet2.png')
background = pygame.transform.scale(pygame.image.load('galaxy.jpg'),(700,500))
pygame.mixer.music.load('john-williams-cantina-band.mp3')
pygame.mixer.music.play(-1)
a = pygame.mixer.Sound('shoot1.ogg')

f1 = pygame.font.Font(None, 20)
ufo = 0
ufo1 = 0



class  GameSprite(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,image):
        super().__init__()
        self.image = pygame.transform.scale(image,(width,height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class Player(GameSprite):
    def __init__(self,x,y,width,height,image,speed):
        super().__init__(x,y,width,height,image)
        self.speed = speed
    def move(self):
        k = pygame.key.get_pressed()
        if k[pygame.K_d] and self.rect.x!=650:
            self.rect.x+=self.speed
        if k[pygame.K_a] and self.rect.x!=0:
            self.rect.x-=self.speed
        if k[pygame.K_w] and self.rect.y!=0:
            self.rect.y-=self.speed
        if k[pygame.K_s] and self.rect.y!=450:
            self.rect.y+=self.speed
    def shoot(self):
        bullet = Bullet(self.rect.x+18,self.rect.y-8,8,8,bullet_img,5)
        bullets.add(bullet)
        a.play()


class Enemy(GameSprite):
    def __init__(self,x,y,width,height,image,speed):
        super().__init__(x,y,width,height,image)
        self.speed = speed
    def update(self):
        if self.rect.y < 450:
            self.rect.y+=self.speed
        if self.rect.y>= 450:
            self.rect.y=randint(-150,-50)
            self.rect.x=randint(0,650)
            rocket1.lost+=1
class Bullet(GameSprite):
    def __init__(self,x,y,width,height,image,speed):
        super().__init__(x,y,width,height,image)
        self.speed = speed
    def update(self):
        self.rect.y-=self.speed
        if self.rect.bottom<=0:
            self.kill()
asteroids = pygame.sprite.Group()
ufos = pygame.sprite.Group()
bullets = pygame.sprite.Group()
rocket1 = Player(250,400,50,50,rocket,5)
font1 = pygame.font.SysFont("Tahoma", 50)

lose = font1.render("ТЫ ПРОИГРАЛ",True,(255,0,0))
win = font1.render("ТЫ ВЫИГРАЛ",True,(0,255,0))
rocket1.lost = 0
rocket1.score = 0
for i in range(5):
    enemy = Enemy(randint(0,650),randint(-150,-50),75,50,enemy_img,2)
    ufos.add(enemy)
for i in range(5):
    enemy1 = Enemy(randint(0,650),randint(-400,-300),75,50,asteroid_img,2)
    asteroids.add(enemy1)

game = True
finish = False
pause = False
while game:


    if not finish:
        window.blit(background,(0,0))
        text1 = f1.render(f'Сбито пришельцев:{rocket1.score}', True,(180, 0, 0))
        text2 = f1.render(f'Пропущено пришельцев:{rocket1.lost}', True,(180, 0, 0))
        rocket1.reset()
        rocket1.move()
        ufos.draw(window)
        bullets.draw(window)
        bullets.update()
        ufos.update()
        asteroids.draw(window)
        asteroids.update()
        window.blit(text1,(10,50))
        window.blit(text2,(500,50))
        for en in pygame.sprite.groupcollide(ufos,bullets,True,True):
            enemy = Enemy(randint(0,650),randint(-150,-50),75,50,enemy_img,2)
            ufos.add(enemy)
            rocket1.score+=1
        for en in pygame.sprite.groupcollide(asteroids,bullets,True,True):
            enemy1 = Enemy(randint(0,650),randint(-400,-300),75,50,asteroid_img,2)
            asteroids.add(enemy1)
        
        if rocket1.lost == 3:
            rocket1.lost=3
            lose = font1.render("ТЫ ПРОИГРАЛ",True,(255,0,0))
            window.blit(lose,(200,200))
            finish = True
            pygame.mixer.music.pause()
        elif rocket1.score == 10:
            rocket1.score=10
            win = font1.render("ТЫ ВЫИГРАЛ",True,(0,255,0))
            window.blit(win,(200,200))
            finish = True
            pygame.mixer.music.pause()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
                game = False
        if e.type == pygame.KEYDOWN and e.key==pygame.K_SPACE and finish!=True:
            rocket1.shoot()
        if e.type == pygame.KEYDOWN and finish and e.key==pygame.K_r:
            rocket1.score=0
            rocket1.lost=0
            pygame.mixer.music.play(-1)
            text1 = f1.render(f'Сбито пришельцев:{rocket1.score}', True,(180, 0, 0))
            text2 = f1.render(f'Пропущено пришельцев:{rocket1.lost}', True,(180, 0, 0))
            finish = False
            ufos.empty()
            asteroids.empty()
            bullets.empty()
            for i in range(5):
                enemy = Enemy(randint(0,650),randint(-150,-50),75,50,enemy_img,2)
                ufos.add(enemy)
            for i in range(5):
                enemy1 = Enemy(randint(0,650),randint(-400,-300),75,50,asteroid_img,2)
                asteroids.add(enemy1)
            rocket1.rect.x=250
            rocket1.rect.y=400
        if e.type == pygame.KEYDOWN and e.key==pygame.K_p:
            if not finish:
                finish = True
                pygame.mixer.music.pause()
            elif finish:
                finish = False
                pygame.mixer.music.play(-1)


    pygame.display.update()
    clock.tick(FPS)
 