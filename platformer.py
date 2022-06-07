from os import times
from sqlite3 import Time
import sys
import pygame
import math
import random
import time

pygame.init()
pygame.display.set_caption("Platformer")
clock=pygame.time.Clock()

screen=pygame.display.set_mode((1200, 800))

background=pygame.image.load("tégla_háttér.png")
checkpoint=pygame.image.load("checkpoint.png")
endtexture=pygame.image.load("end.png")

GRAVITY=1

FONT=pygame.font.Font("freesansbold.ttf", 72)
FONT2=pygame.font.Font("freesansbold.ttf", 24)

BLACK=(0, 0, 0)
WHITE=(255, 255, 255)
GREEN=(0, 255, 0)
BRICK=(142, 136, 122)
RED=(255, 0, 0)
BLUE=(0, 0, 255)

a=True
halal=0
current_level=1
spawn_x=600
spawn_y=500

def win(x, y):
    score=FONT.render("Nyertél", True, WHITE)
    screen.blit(score, (x, y))

def tutorial(x, y):
    score=FONT2.render("Szürke: talaj/fal        Piros: Csabda        Világos-zöld: karakter        Zászló: checkpoint        Ajtó: cél", True, WHITE)
    screen.blit(score, (x, y))

def halalok(x, y):
    score=FONT2.render(f"Halálok száma: {halal}", True, WHITE)
    screen.blit(score, (x, y))

class Check_point():
    def __init__(self, x, y, width, height):
        self.x=x
        self.y=y
        self.dx=0
        self.dy=0
        self.width=width
        self.height=height
        self.color=(0, 100, 0)
        self.friction=0.8

    def goto(self, x, y):
        self.x=x
        self.y=y
    
    def render(self):
        screen.blit(checkpoint, [self.x, self.y])

    def is_aabb_collision(self, other):
        x_collision=(math.fabs(self.x-other.x)*2)<(self.width+other.width)
        y_collision=(math.fabs(self.y-other.y)*2)<(self.height+other.height)
        return(x_collision and y_collision)

class Dedth():
    def __init__(self, x, y, width, height):
        self.x=x
        self.y=y
        self.dx=0
        self.dy=0
        self.width=width
        self.height=height
        self.color=RED
        self.friction=0.8

    def goto(self, x, y):
        self.x=x
        self.y=y
    
    def render(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(int(self.x-self.width/2.0), int(self.y-self.height/2.0), self.width, self.height))

    def is_aabb_collision(self, other):
        x_collision=(math.fabs(self.x-other.x)*2)<(self.width+other.width)
        y_collision=(math.fabs(self.y-other.y)*2)<(self.height+other.height)
        return(x_collision and y_collision)

class End():
    def __init__(self, x, y, width, height):
        self.x=x
        self.y=y
        self.dx=0
        self.dy=0
        self.width=width
        self.height=height
        self.color=BLUE
        self.friction=0.8
    
    def goto(self, x, y):
        self.x=x
        self.y=y

    def render(self):
        screen.blit(endtexture, [self.x, self.y])

    def is_aabb_collision(self, other):
        x_collision=(math.fabs(self.x-other.x)*2)<(self.width+other.width)
        y_collision=(math.fabs(self.y-other.y)*2)<(self.height+other.height)
        return(x_collision and y_collision)

class Sprite():
    def __init__(self, x, y, width, height):
        self.x=x
        self.y=y
        self.dx=6
        self.dy=0
        self.width=width
        self.height=height
        self.color=BRICK
        self.friction=0.8

    def goto(self, x, y):
        self.x=x
        self.y=y

    def render(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(int(self.x-self.width/2.0), int(self.y-self.height/2.0), self.width, self.height))

    def is_aabb_collision(self, other):
        x_collision=(math.fabs(self.x-other.x)*2)<(self.width+other.width)
        y_collision=(math.fabs(self.y-other.y)*2)<(self.height+other.height)
        return(x_collision and y_collision)

class Player(Sprite):
    def __init__(self, x, y, width, height):
        Sprite.__init__(self, x, y, width, height)
        self.color=GREEN
    
    def move(self):
       self.x=self.x+self.dx 
       self.y=self.y+self.dy 
       self.dy=self.dy+GRAVITY

    def jump(self):
        self.dy=self.dy-24

    def left(self):
        self.dx=self.dx-6
    
    def right(self):
        self.dx=self.dx+6

spawn_x=250
spawn_y=640
player=Player(350, 650, 20, 40)
blocks=[]
blocks.append(Sprite(300, 700, 600, 30))
blocks.append(Sprite(800, 700, 200, 30))
end=[]
end.append(End(800, 645, 20, 40))
dedth=[]
dedth.append(Dedth(600, 700, 200, 30))
check_point=[]

veletlen=0
veletlen2=0
veletlen3=0
veletlen4=0
veletlen5=0
veletlen6=0
veletlen7=0
time=0
siker=0
siker2=0
siker3=0
mestint=False
mestint2=False
mestint3=False
mestint4=False
mestint5=False
palya=1
while a==True:
    player.dx=6
    time=time+1
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_a:
                player.left()
            elif event.key==pygame.K_d:
                player.right()
            elif event.key==pygame.K_w:
                for block in blocks:
                    if player.is_aabb_collision(block):
                        player.jump()
                        break

        if event.type==pygame.KEYUP:
            if event.key==pygame.K_a and player.dx<0:
                player.dx=player.dx+6
            if event.key==pygame.K_d and player.dx>0:
                player.dx=player.dx-6

    player.move()

    for block in dedth:
        if player.is_aabb_collision(block):
            player.goto(spawn_x, spawn_y)
            player.dy=0
            time=0
            veletlen=random.randint(10, 50)
            veletlen2=random.randint(50, 100)
            veletlen3=random.randint(80, 120)
            veletlen4=random.randint(60, 90)
            veletlen5=random.randint(1, 40)
            veletlen6=random.randint(45, 60)
            veletlen7=random.randint(100, 120)
            halal=halal+1

    for block in check_point:
        if player.is_aabb_collision(block):
            spawn_x=block.x
            spawn_y=block.y-20

    for block in blocks:
        if player.is_aabb_collision(block):
            if player.x<block.x-block.width/2:
                player.dx=0
                player.x=block.x-block.width/2-player.width/2
            elif player.x>block.x+block.width/2:
                player.dx=0
                player.x=block.x+block.width/2+player.width/2
            elif player.y<block.y:
                player.dy=0
                player.y=block.y-block.height/2-player.height/2+1
            elif player.y>block.y:
                player.dy=0
                player.y=block.y+block.height/2+player.height/2

    if player.y>800:
        player.goto(spawn_x, spawn_y)
        player.dy=0
        time=0
        veletlen=random.randint(10, 50)
        veletlen2=random.randint(50, 100)
        veletlen3=random.randint(80, 120)
        veletlen4=random.randint(60, 90)
        veletlen5=random.randint(1, 40)
        veletlen6=random.randint(45, 60)
        veletlen7=random.randint(100, 120)
        halal=halal+1

    screen.blit(background, [0, 0])

    for block in check_point:
        block.render()
    player.render()
    for block in blocks:
        block.render()
    for block in end:
        block.render()
    for block in dedth:
        block.render()

    halalok(12, 50)

    if current_level<4:
        tutorial(12, 20)

    for block in end:
        if player.is_aabb_collision(block):
            if palya==1:
                siker=veletlen
                f=open("AI.txt", "w", encoding="UTF-8")
                f.write(f'{siker}')
                f.close()
                mestint=True
                player.goto(spawn_x, spawn_y)
                time=0
                current_level=current_level+1
            if palya==2:
                siker=veletlen
                mestint2=True
                siker2=veletlen2
                f=open("AI2.txt", "w", encoding="UTF-8")
                f.write(f'{siker}\n')
                f.write(f'{siker2}')
                f.close()
                player.goto(spawn_x, spawn_y)
                time=0
                current_level=current_level+1
            if palya==3:
                siker=veletlen
                mestint3=True
                siker2=veletlen3
                f=open("AI3.txt", "w", encoding="UTF-8")
                f.write(f'{siker}\n')
                f.write(f'{siker2}')
                f.close()
                player.goto(spawn_x, spawn_y)
                time=0
                current_level=current_level+1
            if palya==4:
                siker=veletlen
                mestint4=True
                siker2=veletlen4
                f=open("AI4.txt", "w", encoding="UTF-8")
                f.write(f'{siker}\n')
                f.write(f'{siker2}')
                f.close()
                player.goto(spawn_x, spawn_y)
                time=0
                current_level=current_level+1
            if palya==5:
                siker=veletlen5
                mestint5=True
                siker2=veletlen6
                siker3=veletlen7
                f=open("AI5.txt", "w", encoding="UTF-8")
                f.write(f'{siker}\n')
                f.write(f'{siker2}\n')
                f.write(f'{siker3}')
                f.close()
                player.goto(spawn_x, spawn_y)
                time=0
                current_level=current_level+1

            if current_level==4:
                palya=2
                spawn_x=125
                spawn_y=541
                player.goto(spawn_x, spawn_y)
                blocks=[]
                blocks.append(Sprite(100, 600, 450, 30))
                blocks.append(Sprite(500, 350, 200, 30))
                blocks.append(Sprite(850, 500, 300, 30))
                end=[]
                end.append(End(850, 445, 20, 40))
                dedth=[]
                dedth.append(Dedth(0, 0, 0, 0))
                dedth.append(Dedth(0, 0, 0, 0))
                check_point=[]
                current_level=current_level+1
            if current_level==7:
                palya=3
                spawn_x=100
                spawn_y=650
                player.goto(spawn_x, spawn_y)
                blocks=[]
                blocks.append(Sprite(200, 700, 250, 30))
                blocks.append(Sprite(600, 500, 500, 30))
                blocks.append(Sprite(1050, 210, 370, 30))
                end=[]
                end.append(End(1150, 155, 20, 40))
                dedth=[]
                check_point=[]
                current_level=current_level+1
            if current_level==10:
                palya=4
                spawn_x=50
                spawn_y=700
                player.goto(spawn_x, spawn_y)
                blocks=[]
                blocks.append(Sprite(100, 750, 250, 30))
                blocks.append(Sprite(400, 470, 250, 30))
                blocks.append(Sprite(700, 370, 250, 30))
                end=[]
                end.append(End(800, 315, 20, 40))
                dedth=[]
                dedth.append(Dedth(600, 270, 100, 30))
                check_point=[]
                current_level=current_level+1
            if current_level==13:
                palya=5
                spawn_x=125
                spawn_y=650
                player.goto(spawn_x, spawn_y)
                blocks=[]
                blocks.append(Sprite(100, 700, 350, 30))
                blocks.append(Sprite(400, 500, 200, 30))
                blocks.append(Sprite(700, 500, 300, 30))
                blocks.append(Sprite(1100, 250, 300, 30))
                end=[]
                end.append(End(1165, 195, 20, 40))
                dedth=[]
                dedth.append(Dedth(600, 500, 200, 30))
                check_point=[]
                current_level=current_level+1
            elif current_level==16:
                blocks=[]
                end=[]
                dedth=[]
                check_point=[]
                pygame.draw.rect(screen, BLACK, pygame.Rect(0, 0, 10000, 10000))
                player=Player(0, 0, 0, 0)
                win(474, 350)
                a=False
    if palya==1:
        if time == veletlen and mestint==False:
            player.jump()
            print("a")
        elif time == siker and mestint==True:
            player.jump()
            print("b")
    if palya==2:
        if time == veletlen and mestint2==False:
            for block in blocks:
                if player.is_aabb_collision(block):
                    player.jump()
                    break
        if time == veletlen4 and mestint2==False:
            for block in blocks:
                if player.is_aabb_collision(block):
                    player.jump()
                    break
        if time == siker and mestint2==True:
            for block in blocks:
                if player.is_aabb_collision(block):
                    player.jump()
                    break
            print("b")
        if time == siker2 and mestint2==True:
            for block in blocks:
                if player.is_aabb_collision(block):
                    player.jump()
                    break
            print("b")
    if palya==3:
        if time == veletlen and mestint3==False:
            for block in blocks:
                if player.is_aabb_collision(block):
                    player.jump()
                    break
        if time == veletlen3 and mestint3==False:
            for block in blocks:
                if player.is_aabb_collision(block):
                    player.jump()
                    break
        if time == siker and mestint3==True:
            for block in blocks:
                if player.is_aabb_collision(block):
                    player.jump()
                    break
            print("b")
        if time == siker2 and mestint3==True:
            for block in blocks:
                if player.is_aabb_collision(block):
                    player.jump()
                    break
            print("b")
    if palya==4:
        if time == veletlen and mestint4==False:
            for block in blocks:
                if player.is_aabb_collision(block):
                    player.jump()
                    break
        if time == veletlen4 and mestint4==False:
            for block in blocks:
                if player.is_aabb_collision(block):
                    player.jump()
                    break
        if time == siker and mestint4==True:
            for block in blocks:
                if player.is_aabb_collision(block):
                    player.jump()
                    break
            print("b")
        if time == siker2 and mestint4==True:
            for block in blocks:
                if player.is_aabb_collision(block):
                    player.jump()
                    break
            print("b")
    if palya==5:
        if time == veletlen5 and mestint5==False:
            for block in blocks:
                if player.is_aabb_collision(block):
                    player.jump()
                    break
        if time == veletlen6 and mestint5==False:
            for block in blocks:
                if player.is_aabb_collision(block):
                    player.jump()
                    break
        if time == veletlen7 and mestint5==False:
            for block in blocks:
                if player.is_aabb_collision(block):
                    player.jump()
                    break
        if time == siker and mestint5==True:
            for block in blocks:
                if player.is_aabb_collision(block):
                    player.jump()
                    break
            print("b")
        if time == siker2 and mestint5==True:
            for block in blocks:
                if player.is_aabb_collision(block):
                    player.jump()
                    break
            print("b")
        if time == siker3 and mestint5==True:
            for block in blocks:
                if player.is_aabb_collision(block):
                    player.jump()
                    break
            print("b")

    print(time)
    pygame.display.flip()

    clock.tick(30)