#Riley Shaw
#For use at codeskulptor.org
import simplegui
#Establish Initial Conditions. Width of the window, height of the window.
#Left and right are assigne to integers for easier data manipulation.
#Game is the condition that makes it all run.
width = 750
height = 500
left = 0
right = 1
game = False

class Ball():
    def __init__(self):
        global width, height, go
        #Init initializes these variables for each separate object
        #Position is a function of width and height, so it starts in the center
        self.size = 5
        self.vel = [0,0]
        self.pos = [width/2-self.size,height/2-self.size]
        
    def collision(self):
        #Honestly, this function is convoluted and repititive. It might work better in the paddle class.
        #Functions are repeated, which goes against DRY programming methods.
        
        #This if elif else statement tests for collisions between the ball vertices and the paddles
        if self.points[2][1]>=height or self.points[1][1]<=0:
            b.vel[1] = -(b.vel[1])
            #If the y position of the top or bottom points exceed the vertical boundaries, velocity is negated.
        
        elif self.points[0][0]<=left_paddle.points[1][0] and (self.points[0][1]+self.size>=left_paddle.points[1][1] and self.points[0][1]+self.size<=left_paddle.points[2][1]):
            b.vel[0] = -(b.vel[0]-abs(left_paddle.vel)/10)
            b.vel[1] = ((self.points[0][1]+self.size)-(left_paddle.points[1][1]+left_paddle.size[1]))/7
            #If the x and y of the ball are between the x and y of the paddle
            #negate the x velocity and add a tenth of the paddle's velocity.
            #The y velocity depends on the distance from the center of the paddle.
            
        elif self.points[1][0]>=right_paddle.points[1][0] and (self.points[1][1]+self.size>=right_paddle.points[1][1] and self.points[1][1]+self.size<=right_paddle.points[2][1]):
            b.vel[0] = -(b.vel[0]+abs(right_paddle.vel)/10)
            b.vel[1] = ((self.points[1][1]+self.size)-(right_paddle.points[1][1]+right_paddle.size[1]))/7
            #Rinse and repeat for the right paddle. It's essentially an exact copy of the above conditional.
            #Again, violating DRY principles of software development.
            
        elif self.points[1][0]<=left_paddle.points[1][0] and not (self.points[0][1]+self.size>=left_paddle.points[1][1] and self.points[0][1]+self.size<=left_paddle.points[2][1]):
            right_paddle.score += 1
            right_paddle.scored = True
            self.pos = [width/2-self.size,height/2-self.size]
            go()
            #If the paddle misses then increase it's score and reset the ball and call the go() function.
            #Go function acts as the intermediate reset.
            
        elif self.points[0][0]>=right_paddle.points[1][0] and not (self.points[1][1]+self.size>=right_paddle.points[1][1] and self.points[1][1]+self.size<=right_paddle.points[2][1]):
            left_paddle.score += 1
            left_paddle.scored = True
            self.pos = [width/2-self.size,height/2-self.size]
            go()
            #A copy of the above conditional, adjusted for the right paddle.
            #Again a repeat, inefficient and wasteful.
        else:
            pass #If none of the above conditions are met then do nothing because there is no collision.
            
    
    #This function is called inside of the main loop. The points list has to be created and updated in its entirety.
    def update(self):
        self.points = [self.pos,[self.pos[0]+2*self.size, self.pos[1]],[self.pos[0]+2*self.size, self.pos[1]+2*self.size],[self.pos[0], self.pos[1]+2*self.size]]
        self.collision()
        
#Create the Ball object, assign it to variable b
b = Ball()


def go():
    #This function is called to start the SERVE not the game.
    #This differs from starting the game, which is handled when spacebar is pressed while the game is over
    global game
    b.vel = [0,0] #Stop the ball

    if right_paddle.scored:
        #Right scored, send the serve right and reset the scorer variable.
        b.vel = [7, 0]
        right_paddle.scored = False
        #If right score is ten then set win to true, reset the ball, and stop the game.
        if right_paddle.score == 10:
            right_paddle.win = True
            b.pos = [width/2-b.size,height/2-b.size]
            b.vel = [0,0]
            game = False
    elif left_paddle.scored:
        #Hey look I repeat myself again.
        b.vel = [-7, 0]
        left_paddle.scored = False
        if left_paddle.score == 10:
            left_paddle.win = True
            b.pos = [width/2-b.size,height/2-b.size]
            b.vel = [0,0]
            game = False
        
    else:
        b.vel = [7, 0] #Send it right on first throw
class Paddle:
    #Left and right paddle objects
    def __init__(self, side):
        #Class takes argument that determines which side the paddle is on
        global width, height
        self.score = 9 #starts at 9 but is reset when the spacebar is pressed
        self.side = side
        self.size = [10,height/10] #height is a tenth of the total height of the board
        self.vel = 0 #not moving at start
        self.pos = [self.size[0]*2-self.side*width,(height/2-self.size[1])] #starts in the center
        self.scored = False
        self.win = False
        #Initial conditions. Self explanatory variables. 
    def update(self):
        global height
        #Points list is a complex list of vertices. Each is relative to the pos coordinates, the top left corner.
        self.points = [[abs(self.pos[0]),self.pos[1]],[abs(self.pos[0]+self.size[0]),self.pos[1]],[abs(self.pos[0]+self.size[0]),(self.pos[1]+2*self.size[1])],[abs(self.pos[0]),(self.pos[1]+2*self.size[1])]]
        
        if self.pos[1]<=0:
            #If it reaches the top and attempts to go further, reset it to the top.
            self.vel = 0
            self.pos[1] = 0
            
        if self.points[2][1]>=height:
            #Same thing for the bottom part of the screen, using the bottom vertex.(Repeating myself again?)
            self.vel = 0
            self.pos[1]=height-self.size[1]*2
            
            
#Create paddle objects
left_paddle = Paddle(left)
right_paddle = Paddle(right)

def key_handler(key):
    global game
    #create up down and w s key handlers that affect paddle velocity
    if key == simplegui.KEY_MAP['up']:
        right_paddle.vel = -7
    if key == simplegui.KEY_MAP['down']:
        right_paddle.vel = 7
    if key == simplegui.KEY_MAP['w']:
        left_paddle.vel = -7
    if key == simplegui.KEY_MAP['s']:
        left_paddle.vel = 7
    
    if key == simplegui.KEY_MAP['space'] and not game:
        #Start the game if it isn't already
        go()
        right_paddle.score = 0
        left_paddle.score = 0
        right_paddle.win = False
        left_paddle.win = False
        game = True
        
        
def key_up(key):
    #Stop the paddles from moving when the key is lifted
    if key == simplegui.KEY_MAP['up']:
        right_paddle.vel = 0
    elif key == simplegui.KEY_MAP['down']:
        right_paddle.vel = 0
    elif key == simplegui.KEY_MAP['w']:
        left_paddle.vel = 0
    elif key == simplegui.KEY_MAP['s']:
        left_paddle.vel = 0


def draw(canvas):
    #Move things and run the update function
    left_paddle.pos[1] += left_paddle.vel
    left_paddle.update()
    
    right_paddle.pos[1] += right_paddle.vel
    right_paddle.update()
    
    b.pos[0] += b.vel[0]
    b.pos[1] += b.vel[1]
    b.update()
    
    #Center Line
    canvas.draw_line((width/2, 0), (width/2, height), 3, "White")    
    
    #Conditional Text
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
    
    #always draw scores
    canvas.draw_text(str(left_paddle.score),(width/2-50, 50),30,"White","monospace")
    canvas.draw_text(str(right_paddle.score),(width/2+30, 50),30,"White","monospace")    
    
    #Draw the ball and paddles
    canvas.draw_polygon(left_paddle.points,1,"White", "White")
    canvas.draw_polygon(right_paddle.points,1,"White", "White")
    canvas.draw_polygon(b.points,1,"White","White")


#Standard simplegui init
f = simplegui.create_frame("Pong", width, height)
f.set_keydown_handler(key_handler)
f.set_keyup_handler(key_up)
f.set_draw_handler(draw)
f.start()
