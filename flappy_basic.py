import pygame as pg 
import random as rnd 

class Bird:
    def __init__(self,x,y,r,y_vel,jump_vel,g,color):
        self.x=x 
        self.y=y 
        self.r=r 
        self.y_vel=y_vel
        self.g=g 
        self.color=color
        self.jump_vel=jump_vel
    
    def flap(self,t):
        self.y_vel+=self.g*t
        self.y+=self.y_vel*t
    def hit_box(self):
        return pg.Rect(self.x-self.r,self.y-self.r,self.r,self.r)
    def out_of_cage(self,scr_rect):
        return self.y-self.r<scr_rect.top or self.y+self.r>scr_rect.bottom
    def jump(self):
        self.y_vel=self.y_vel*0-self.jump_vel
    def draw(self,wnd):
        pg.draw.circle(wnd,self.color,(self.x,self.y),self.r)
    def draw(self,wnd,outline):
        pg.draw.circle(wnd,self.color,(self.x,self.y),self.r)
        if outline:
            pg.draw.rect(wnd,pg.Color.black,self.hit_box(self),1)

class Pipe_pair:
    def __init__(self,rect1,rect2):
        self.top=rect1
        self.bot=rect2 
        self.color=(30,200,80)
    def __init__(self,rect1,rect2,color):
        self.top=rect1
        self.bot=rect2 
        self.color=color
    def __init__(self,scr_rect):#yikes
        
        margin_per=0.15
        hole_height=scr_rect.height*0.33
        pipe_width=hole_height*0.3

        min_bot_top=(1-margin_per)*scr_rect.height
        max_bot_top=margin_per*scr_rect.height+hole_height
        top_of_bot_pipe=rnd.randint(max_bot_top,min_bot_top)
        
        self.bot=pg.Rect(scr_rect.width,top_of_bot_pipe,pipe_width,scr_rect.height-top_of_bot_pipe)
        self.top=pg.Rect(scr_rect.width,0,pipe_width,top_of_bot_pipe-hole_height)

        self.color=(30,200,80)

    def draw(self,wnd):
        pg.draw.rect(wnd,self.color,self.top)                
        pg.draw.rect(wnd,self.color,self.bot)                
    def collision(self,rect):
        return self.top.colliderect(rect) or self.bot.colliderect(rect)
    def move(self,px):
        self.top.x+=px
        self.bot.x+=px
    def out_of_screen(self,scr_rect):
        return self.bot.right<scr_rect.left

class Game:
    def __init__(self,scr_rect):
        init_speed=300
        self.game_rect=scr_rect
        self.bird=Bird(scr_rect.width/6,scr_rect.height/2,25,0,550,800,(230,200,80))
        self.speed=init_speed
        self.pipes=[]
        self.points=0
        self.new_pipe()
        self.over=False
    def new_pipe(self):
        self.points+=1
        self.speed+=10+(100/(40+self.points))

        self.distance_to_next=rnd.randint(round(w*0.3),round(w*0.6))
        self.pipes.append(Pipe_pair(self.game_rect))
    def draw(self,wnd):
        for pipe in self.pipes:
            pipe.draw(wnd) 
        self.bird.draw(wnd,False)

        font = pg.font.SysFont(None, self.bird.r)
        score = font.render("Speed: " + str(round(self.speed)), True, (255,255,255))
        wnd.blit(score,(self.bird.r,self.bird.r))

    def update(self,t):
        step=-t*self.speed
        
        i=0
        n=len(self.pipes)
        while(i<n):
            pipe=self.pipes[i]
            pipe.move(step)
            i+=1
            if(pipe.collision(self.bird.hit_box())):
                self.over=True 
            if(pipe.out_of_screen(self.game_rect)):
                self.pipes.remove(pipe)
                i-=1
                n-=1
               

        self.distance_to_next+=step 
        if(self.distance_to_next<0):
            self.new_pipe()

        self.bird.flap(t)
        if(self.bird.out_of_cage(self.game_rect)):
            self.over=True
    def jump_clicked(self):
        self.bird.jump()
        

pg.init()

window=pg.display.set_mode((1200,800))

w, h = pg.display.get_surface().get_size()
scr_rect=pg.Rect(0,0,w,h)
end = False

fps=60
calcps=120


COMPUTE=pg.USEREVENT+3

pg.time.set_timer(COMPUTE,round(1000/calcps))

DRAW=pg.USEREVENT+1
pg.time.set_timer(DRAW,round(1000/fps))

game1=None

while not end:
    if(game1 is None):
        game1=Game(pg.Rect(0,0,w,h))

    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            end=True
        elif event.type == pg.KEYDOWN:
            keys = pg.key.get_pressed()
            if keys[pg.K_SPACE]:
                game1.bird.jump()
        elif event.type == DRAW:
            window.fill((0,0,0))
            game1.draw(window)
            pg.display.flip()
        elif event.type == COMPUTE:
            game1.update(1/calcps)
            if(game1.over):
                game1=None
                break
    
    