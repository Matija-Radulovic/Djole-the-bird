import pygame as pg 
import random as rnd 

def drawPipe(pipe):
    (left,bottom)=pipe
    pg.draw.rect(window,pipe_color,pg.Rect(left,bottom,pipe_w,h-bottom))
    pg.draw.rect(window,pipe_color,pg.Rect(left,0,pipe_w,bottom-pipe_h))
def game_speed(score):
    return (10+0.75*score)*1

def next_step():
    return

def new_pipe():
    return

def pipeRect(left,bottom):
    return ((left,bottom,pipe_w,h-bottom),(left,0,pipe_w,bottom-pipe_h))

def collision_help(circle,rect):
    bx=circle[0]
    by=circle[1]
    br=circle[2]
    px=rect[0]
    py=rect[1]
    pw=rect[2]
    ph=rect[3]
    
    min_right=min(bx+br,px+pw)
    max_left=max(bx-br,px)
    
    max_top=max(by-br,py)
    min_bot=min(by+br,py+ph)
    
    if min_right>max_left and min_bot>max_top:
        return True
    return False

def collision(bird,pipe):
    pipe_rect1=pipeRect(pipe[0],pipe[1])[0]
    pipe_rect2=pipeRect(pipe[0],pipe[1])[1]
    return collision_help(bird,pipe_rect1) or collision_help(bird,pipe_rect2)

def game_over():
    return
def game_reset():
    return

pg.init()

window=pg.display.set_mode((1200,800))
w, h = pg.display.get_surface().get_size()

pipe_w=60
pipe_h=200

next_dist=-1

pipe_color=(30,200,80)

end = False

pipes=[]

x_speed_pxps=300
fps=60
period=1000/fps

x_step=x_speed_pxps/fps

DRAW=pg.USEREVENT+1
pg.time.set_timer(DRAW,round(period))


gravity_pxps=600
gravity_step=gravity_pxps/(fps^2)

y_vel=0
jump_vel_pxps=450
jump_step=jump_vel_pxps/fps
bounce_perc=0.2

bird_x=w/6
bird_y=h/2
bird_r=25

bird_color=(230,200,80)

points=0

stop=False 

while not end:
    event = pg.event.poll()
    if event.type == pg.QUIT:
        end=True
    elif event.type == DRAW:   
        if stop:
            continue

        for i in range(len(pipes)):
            pipes[i]=(pipes[i][0]-x_step,pipes[i][1])
        
        pipes = [p for p in pipes if p[0]+pipe_w>=0]
        
        next_dist-= x_step
        y_vel+=gravity_step
        y_step=y_vel/fps
        bird_y+=y_step
        
        if next_dist<=0:
            points+=1
            
            x_speed_pxps+=game_speed(points)
            x_step=x_speed_pxps/fps
            
            next_dist=rnd.randint(round(w/3),round(w/1.5))
            pipe_bot=rnd.randint(round(h/8)+pipe_h,round(7*h/8))
    
            pipe=(w,pipe_bot)
            pipes.append(pipe)
        
        for pipe in pipes:
            if collision((bird_x,bird_y,bird_r),pipe):
                stop=True


        window.fill((0,0,0))
        
        pg.draw.rect(window,bird_color,(bird_x-bird_r,bird_y-bird_r,bird_r*2,bird_r*2))        
        
        for i in range(len(pipes)):
            pipe=pipes[i]
            drawPipe(pipe)
            
        font = pg.font.SysFont(None, 48)
        score_label = font.render("Speed: " + str(round(x_speed_pxps)), True, (255,255,255))
        
        window.blit(score_label,(50,50))

        pg.display.flip()
    
    elif event.type == pg.KEYDOWN:
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            y_vel = y_vel*bounce_perc- jump_vel_pxps
