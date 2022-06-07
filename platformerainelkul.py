import sys
import pygame
import math
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
current_level=1
spawn_x=600
spawn_y=500

def win(x, y):
    score=FONT.render("Nyertél", True, WHITE)
    screen.blit(score, (x, y))

def tutorial(x, y):
    score=FONT2.render("Szürke: talaj/fal        Piros: Csabda        Világos-zöld: karakter        Zászló: checkpoint        Ajtó: cél", True, WHITE)
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
        self.dx=0
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

player=Player(600, 500, 20, 40)
blocks=[]
blocks.append(Sprite(600, 200, 900, 20))
blocks.append(Sprite(300, 400, 300, 20))
blocks.append(Sprite(600, 400, 100, 20))
blocks.append(Sprite(900, 400, 300, 20))
blocks.append(Sprite(600, 600, 1000, 20))
blocks.append(Sprite(1000, 500, 100, 200))
blocks.append(Sprite(200, 500, 100, 200))
end=[]
end.append(End(600, 150, 20, 40))
dedth=[]
dedth.append(Dedth(720, 401, 60, 21))
dedth.append(Dedth(480, 401, 60, 21))
dedth.append(Dedth(125, 401, 50, 21))
dedth.append(Dedth(1075, 401, 50, 21))
check_point=[]
check_point.append(Check_point(595, 350, 20, 40))

while a==True:
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

    if current_level==1:
        tutorial(12, 20)

    for block in end:
        if player.is_aabb_collision(block):
            if current_level==1:
                spawn_x=50
                spawn_y=541
                player.goto(spawn_x, spawn_y)
                blocks=[]
                blocks.append(Sprite(600, 600, 1200, 20))
                blocks.append(Sprite(200, 490, 20, 200))
                blocks.append(Sprite(800, 305, 200, 20))
                blocks.append(Sprite(750, 240, 200, 20))
                blocks.append(Sprite(500, 240, 200, 20))
                end=[]
                end.append(End(500, 190, 20, 40))
                dedth=[]
                dedth.append(Dedth(200, 380, 120, 20))
                dedth.append(Dedth(500, 445, 20, 290))
                dedth.append(Dedth(590, 240, 20, 400))
                check_point=[]
                check_point.append(Check_point(595, 550, 20, 40))
                current_level=current_level+1
            elif current_level==2:
                spawn_x=50
                spawn_y=541
                player.goto(spawn_x, spawn_y)
                blocks=[]
                blocks.append(Sprite(50, 600, 100, 20))
                blocks.append(Sprite(250, 320, 100, 20))
                blocks.append(Sprite(390, 500, 180, 20))
                blocks.append(Sprite(700, 700, 100, 20))
                blocks.append(Sprite(700, 230, 100, 20))
                blocks.append(Sprite(1050, 100, 100, 20))
                end=[]
                end.append(End(1050, 50, 20, 40))
                dedth=[]
                dedth.append(Dedth(390, 400, 170, 20))
                check_point=[]
                check_point.append(Check_point(315, 450, 20, 40))
                current_level=current_level+1
            elif current_level==3:
                spawn_x=50
                spawn_y=541
                player.goto(spawn_x, spawn_y)
                blocks=[]
                blocks.append(Sprite(600, 600, 1200, 20))
                end=[]
                end.append(End(1100, 550, 20, 40))
                dedth=[]
                dedth.append(Dedth(200, 515, 20, 150))
                dedth.append(Dedth(245, 400, 20, 300))
                dedth.append(Dedth(300, 515, 20, 150))
                dedth.append(Dedth(345, 400, 20, 300))
                dedth.append(Dedth(400, 515, 20, 150))
                dedth.append(Dedth(445, 400, 20, 300))
                dedth.append(Dedth(500, 515, 20, 150))
                dedth.append(Dedth(545, 400, 20, 300))
                dedth.append(Dedth(600, 515, 20, 150))
                dedth.append(Dedth(645, 400, 20, 300))
                dedth.append(Dedth(700, 515, 20, 150))
                dedth.append(Dedth(745, 400, 20, 300))
                dedth.append(Dedth(800, 515, 20, 150))
                dedth.append(Dedth(845, 400, 20, 300))
                dedth.append(Dedth(900, 515, 20, 150))
                dedth.append(Dedth(945, 400, 20, 300))
                dedth.append(Dedth(1000, 515, 20, 150))
                dedth.append(Dedth(1045, 400, 20, 300))
                check_point=[]
                current_level=current_level+1
            elif current_level==4:
                spawn_x=50
                spawn_y=541
                player.goto(spawn_x, spawn_y)
                blocks=[]
                blocks.append(Sprite(600, 600, 1200, 20))
                end=[]
                end.append(End(1100, 550, 20, 40))
                dedth=[]
                dedth.append(Dedth(390, 400, 170, 20))
                check_point=[]
                check_point.append(Check_point(1100, 470, 20, 40))
                current_level=current_level+1
            elif current_level==5:
                blocks=[]
                end=[]
                dedth=[]
                check_point=[]
                pygame.draw.rect(screen, BLACK, pygame.Rect(0, 0, 10000, 10000))
                player=Player(0, 0, 0, 0)
                win(474, 350)
                a=False
    pygame.display.flip()

    clock.tick(30)
    if a==False:
        time.sleep(5)