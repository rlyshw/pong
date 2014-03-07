#This is a (quick and sloppy) pygame port of the Codeskulptor version.

import pygame
pygame.init()
black = (0,0,0)
white = (255,255,255)
green = (0,255,0)

width = 750
height = 500
left = 0
right = 1
game = False

screen = pygame.display.set_mode((width,height))

clock = pygame.time.Clock()

text = pygame.font.SysFont("default", 40)

def win_text(side):
    winner = text.render("Winner!",True,green)
    winnerrect = winner.get_rect()
    if side == 0:
        winnerrect.centerx = width/2-150
    elif side == 1:
        winnerrect.centerx = width/2+150
    winnerrect.centery = 150
    return [winner,winnerrect]

def score_text(side):
    if side == 0:
        score = text.render(str(left_paddle.score),True,white)
        scorerect = score.get_rect()
        scorerect.centerx = width/2-25
    elif side == 1:
        score = text.render(str(right_paddle.score),True,white)
        scorerect = score.get_rect()
        scorerect.centerx = width/2+25
    scorerect.centery = 50
    return [score,scorerect]

class Ball():
    def __init__(self):
        global width, height, go
        self.size = 5
        self.vel = [0,0]
        self.pos = [width/2-self.size,height/2-self.size]
    def collision(self):
        if self.points[2][1]>=height or self.points[1][1]<=0:
            b.vel[1] = -(b.vel[1])
            
        elif self.points[0][0]<=left_paddle.points[1][0] and (self.points[0][1]+self.size>=left_paddle.points[1][1] and self.points[0][1]+self.size<=left_paddle.points[2][1]):
            b.vel[0] = -(b.vel[0]-abs(left_paddle.vel)/10)
            b.vel[1] = ((self.points[0][1]+self.size)-(left_paddle.points[1][1]+left_paddle.size[1]))/7
            
        elif self.points[1][0]>=right_paddle.points[1][0] and (self.points[1][1]+self.size>=right_paddle.points[1][1] and self.points[1][1]+self.size<=right_paddle.points[2][1]):
            b.vel[0] = -(b.vel[0]+abs(right_paddle.vel)/10)
            b.vel[1] = ((self.points[1][1]+self.size)-(right_paddle.points[1][1]+right_paddle.size[1]))/7
            
        elif self.points[1][0]<=left_paddle.points[1][0] and not (self.points[0][1]+self.size>=left_paddle.points[1][1] and self.points[0][1]+self.size<=left_paddle.points[2][1]):
            right_paddle.score += 1
            right_paddle.scored = True
            self.pos = [width/2-self.size,height/2-self.size]
            go()
            
        elif self.points[0][0]>=right_paddle.points[1][0] and not (self.points[1][1]+self.size>=right_paddle.points[1][1] and self.points[1][1]+self.size<=right_paddle.points[2][1]):
            left_paddle.score += 1
            left_paddle.scored = True
            self.pos = [width/2-self.size,height/2-self.size]
            go()
            
        else:
            pass

    def update(self):
        self.points = [self.pos,[self.pos[0]+2*self.size, self.pos[1]],[self.pos[0]+2*self.size, self.pos[1]+2*self.size],[self.pos[0], self.pos[1]+2*self.size]]
        self.collision()

b = Ball()

def go():
    global game
    b.vel = [0,0]
    if right_paddle.scored:
        b.vel = [7, 0]
        right_paddle.scored = False
        if right_paddle.score == 10:
            right_paddle.win = True
            b.pos = [width/2-b.size,height/2-b.size]
            b.vel = [0,0]
            game = False

    elif left_paddle.scored:
        b.vel = [-7, 0]
        left_paddle.scored = False
        if left_paddle.score == 10:
            left_paddle.win = True
            b.pos = [width/2-b.size,height/2-b.size]
            b.vel = [0,0]
            game = False
    else:
        b.vel = [7, 0]
class Paddle:
    def __init__(self, side):
        global width, height
        self.score = 9
        self.side = side
        self.size = [10,height/10]
        self.vel = 0
        self.pos = [self.size[0]*2-self.side*width,(height/2-self.size[1])]
        self.scored = False
        self.win = False
    def update(self):
        global height
        self.points = [[abs(self.pos[0]),self.pos[1]],[abs(self.pos[0]+self.size[0]),self.pos[1]],[abs(self.pos[0]+self.size[0]),(self.pos[1]+2*self.size[1])],[abs(self.pos[0]),(self.pos[1]+2*self.size[1])]]
        if self.pos[1]<=0:
          self.vel = 0
          self.pos[1] = 0
        if self.points[2][1]>=height:
            self.vel = 0
            self.pos[1]=height-self.size[1]*2
left_paddle = Paddle(left)
right_paddle = Paddle(right)

def draw():
    left_paddle.pos[1] += left_paddle.vel
    left_paddle.update()
    
    right_paddle.pos[1] += right_paddle.vel
    right_paddle.update()
    #print right_paddle.points
    
    b.pos[0] += b.vel[0]
    b.pos[1] += b.vel[1]
    b.update()
    #print b.points
    
    pygame.draw.line(screen,white,(width/2, 0), (width/2, height), 1)
    
    if right_paddle.win:
        screen.blit(win_text(right)[0],win_text(right)[1])
    elif left_paddle.win:
        screen.blit(win_text(left)[0],win_text(left)[1])

    screen.blit(score_text(left)[0],score_text(left)[1])
    screen.blit(score_text(right)[0],score_text(right)[1])
    pygame.draw.polygon(screen, white,left_paddle.points,1)
    pygame.draw.polygon(screen, white,right_paddle.points,1)
    pygame.draw.polygon(screen, white,b.points,1)

pygame.display.set_caption("Pong")

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_UP:
                right_paddle.vel = -7
            if key == pygame.K_DOWN:
                right_paddle.vel = 7
            if key == pygame.K_w:
                left_paddle.vel = -7
            if key == pygame.K_s:
                left_paddle.vel = 7
            if key == pygame.K_SPACE and not game:
                go()
                right_paddle.score = 0
                left_paddle.score = 0
                right_paddle.win = False
                left_paddle.win = False
                game = True
            if key == pygame.K_ESCAPE:
                done = True
        elif event.type == pygame.KEYUP:
            key = event.key
            if key == pygame.K_UP:
                right_paddle.vel = 0
            if key == pygame.K_DOWN:
                right_paddle.vel = 0
            if key == pygame.K_w:
                left_paddle.vel = 0
            if key == pygame.K_s:
                left_paddle.vel = 0
    screen.fill(black)
    draw()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
