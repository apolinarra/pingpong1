from pygame import *
from random import choice

class GameSprite(sprite.Sprite):
    def __init__(self, img, x,y,w,h, speed):
        super().__init__()
        self. image = transform.scale(image.load(img), (w,h))
        self.rect= self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.rect.h = h
        self.rect.w = w
    def reset(self):
        win.blit(self.image,(self.rect.x, self.rect.y))
    def collidepoint(self, x, y):
        return self.rect.collidepoint(x,y)

class Player_l(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y>5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_w-5-self.rect.width:
            self.rect.y += self.speed
    
class Player_r(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y>5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_w-5-self.rect.width:
            self.rect.y += self.speed
    

class Ball(GameSprite):
    def __init__(self, img,x,y,w,h,speed):
        super().__init__(img,x,y,w,h,speed)
        self.speed_x = 0
        self.speed_y = 0

    def set_derection(self, speed_x,speed_y):
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self):
        self.rect.x += self.speed_x*self.speed
        self.rect.y += self.speed_y*self.speed

    def check_direction(self, pl1, pl2):
        global point_l,point_r
        if self.rect.y<=0:
            self.speed_y*=-1
        elif self.rect.y>=768-self.rect.h:
            self.speed_y*=-1
        elif self.rect.colliderect(pl1.rect):
            self.speed_x*=-1
        elif self.rect.colliderect(pl2.rect):
            self.speed_x*=-1

        elif self.rect.x<=0:
            point_r +=1
            self.rect.x = 1366/2-self.rect.w/2
            self.rect.y = 768/2-self.rect.h/2
            self.set_derection(choice([-1,1]), choice([-1,1]))
        
        elif self.rect.x>=1366-self.rect.w:
            point_l +=1
            self.rect.x = 1366/2-self.rect.w/2
            self.rect.y = 768/2-self.rect.h/2
            self.set_derection(choice([-1,1]), choice([-1,1]))

        
#создай окно игры
win_h = 768
win_w = 1366
win = display.set_mode((win_w,win_h),FULLSCREEN)
display.set_caption('Пинг понг')

#задай фон сцены
background = transform.scale(image.load('pore.png'),(win_w,win_h))
player_l = Player_l('vilka.png',10,100,50,400,15,)
player_r = Player_r('vilka.png',1300,10,50,400,15,)
direction = [-1,1]
ball = Ball('kart.png',1366/2-170/2, 768/2-140/2,170,140,30)
ball.set_derection(choice(direction),choice(direction))


font.init()
font1 = font.SysFont('Arial', 36)

point_l = 0
point_r = 0 
game = True
finish= False
font_lose = font1.render('ТЫ ЛОООХ', 1, (255,255,255))
font_win = font1.render('ЙОУ ТЫ БРО',  1, (255,255,255))


clock = time.Clock()
FPS = 60

while game:
    # поверка нажатия на кнопку выход
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish == False:
        win.blit(background,(0,0))
        player_l.update()
        player_r.update()
        ball.update()

        ball.check_direction(player_l,player_r)

        player_l.reset()
        player_r.reset()
        ball.reset()

        font_l = font1.render('Пропущенно левой:'+ str(point_r), 1, (0,0,0))
        win.blit(font_l,(10,50))
        font_r = font1.render('Пропущенно правой:'+ str(point_l), 1, (0,0,0))
        win.blit(font_r,(1000,50))

        if point_l ==5:
            finish = True
            font_lose = font1.render('ПРАВЫЙ ЛОООХ ЛЕВЫЙ ВЫЙГРАЛ', 1, (0,0,0))
            win.blit(font_lose,(440, 768/2))
        if point_r ==5:
            finish = True
            font_lose = font1.render('ЛЕВЫЙ ЛОООХ ПРАВЫЙ ВЫЙГРАЛ', 1, (0,0,0))
            win.blit(font_lose,(440, 768/2))



    display.update()
    clock.tick(FPS)