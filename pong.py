import simplegui
width = 750
height = 500
left = 0
right = 1
game = False

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

def key_handler(key):
    global game
    if key == simplegui.KEY_MAP['up']:
        right_paddle.vel = -7
    if key == simplegui.KEY_MAP['down']:
        right_paddle.vel = 7
    if key == simplegui.KEY_MAP['w']:
        left_paddle.vel = -7
    if key == simplegui.KEY_MAP['s']:
        left_paddle.vel = 7
    if key == simplegui.KEY_MAP['space'] and not game:
        go()
        right_paddle.score = 0
        left_paddle.score = 0
        right_paddle.win = False
        left_paddle.win = False
        game = True
def key_up(key):
    if key == simplegui.KEY_MAP['up']:
        right_paddle.vel = 0
    if key == simplegui.KEY_MAP['down']:
        right_paddle.vel = 0
    if key == simplegui.KEY_MAP['w']:
        left_paddle.vel = 0
    if key == simplegui.KEY_MAP['s']:
        left_paddle.vel = 0
def draw(canvas):
    left_paddle.pos[1] += left_paddle.vel
    left_paddle.update()
    
    right_paddle.pos[1] += right_paddle.vel
    right_paddle.update()
    #print right_paddle.points
    
    b.pos[0] += b.vel[0]
    b.pos[1] += b.vel[1]
    b.update()
    #print b.points
    canvas.draw_line((width/2, 0), (width/2, height), 3, "White")    
    if right_paddle.win:
        canvas.draw_text("Winner!",(width/2+30,150),40,"Green","monospace")
    elif left_paddle.win:
        canvas.draw_text("Winner!",(width/2-200,150),40,"Green","monospace")
    if not game:
        canvas.draw_text("w - /\\",(width/2-300,50),30,"White","monospace")
        canvas.draw_text("s - \\/",(width/2-300,100),30,"White","monospace")
        canvas.draw_text("up arrow - /\\",(width/2+75,350),30,"White","monospace")
        canvas.draw_text("down arrow - \\/",(width/2+40,400),30,"White","monospace")
        canvas.draw_text("Press (spacebar) to start!",(width/2-340,height-40),45,"Green","monospace")

    canvas.draw_text(str(left_paddle.score),(width/2-50, 50),30,"White","monospace")
    canvas.draw_text(str(right_paddle.score),(width/2+30, 50),30,"White","monospace")    
    
    canvas.draw_polygon(left_paddle.points,1,"White", "White")
    canvas.draw_polygon(right_paddle.points,1,"White", "White")
    canvas.draw_polygon(b.points,1,"White","White")
f = simplegui.create_frame("Pong", width, height)
f.set_keydown_handler(key_handler)
f.set_keyup_handler(key_up)
f.set_draw_handler(draw)
f.start()
