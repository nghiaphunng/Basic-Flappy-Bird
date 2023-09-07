import pygame
from random import randint
from time import time

pygame.init()

WIDTH_SC=800
HEIGHT_SC=600
screen=pygame.display.set_mode((WIDTH_SC, HEIGHT_SC))
pygame.display.set_caption("Basic Flappy Bird")

running=True
clock=pygame.time.Clock()

#color
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
BLACK=(0,0,0)
BG_COLOR=(96,96,96)
PIPE_COLOR=(0,255,255)
BIRD_COLOR=(255,255,0)

#bird
BIRD_WIDTH = 50
BIRD_HEIGHT = 50
BIRD_X = 80 #bird's x-coordinate
BIRD_y = 300 #bird's y-coordinate
GRAVITY = 0.5
drop_velocity = 0

game_over = False
score = 0

#create text
font=pygame.font.SysFont("sans-serif", 50)
game_over_text = font.render("Game Over", True, RED)
game_over_text_rect = game_over_text.get_rect(center=(WIDTH_SC/2,100))

play_again_text = font.render("Press ENTER To Play Again", True, GREEN)
play_again_text_rect = play_again_text.get_rect(center=(WIDTH_SC/2,200))

start = False
start_time = time()
current_time = time()
update_time = 1
total_secs = 3
time_font = pygame.font.SysFont('sans-serif', 200)

#pipe parameters
DISTANCE_PIPE = 250 #distance between pipes
DISTANCE_PIPE_OPPOSITE = 150 #distance between opposite tubes
PIPE_WIDTH = 70 #pipe width
PIPE_VELOCITY = 5 #speed pipe

class Pipe():
    def __init__(self,x,height_pipe):
        self.x = x
        self.height_pipe = height_pipe
        self.over = False
        
    def draw(self):
        global score
        global game_over
        
        pipe=pygame.draw.rect(screen, PIPE_COLOR, (self.x, 0, PIPE_WIDTH, self.height_pipe))
        pygame.draw.rect(screen, BLACK, (self.x, self.height_pipe - 20, PIPE_WIDTH, 20))
        pipe_opposite = pygame.draw.rect(screen, PIPE_COLOR, (self.x, self.height_pipe + DISTANCE_PIPE_OPPOSITE, PIPE_WIDTH, HEIGHT_SC - self.height_pipe - DISTANCE_PIPE_OPPOSITE))
        pygame.draw.rect(screen, BLACK, (self.x, self.height_pipe + DISTANCE_PIPE_OPPOSITE, PIPE_WIDTH, 20))

        #update
        if start == True:
            if self.x >= -PIPE_WIDTH: #pipe turn left
                self.x -= PIPE_VELOCITY
            else: #the pipe moves all the way to the left of the screen
                self.x = PIPE_X_AFTER
                self.height_pipe = randint(100,360)
                self.over = False
            
            #colliding
            if bird.colliderect(pipe) or bird.colliderect(pipe_opposite): #collision with the pipe
                game_over = True
            
            #score
            if BIRD_X > self.x + PIPE_WIDTH and self.over == False:
                score += 1
                self.over = True

            
        
        
# initialize the initial position for the pipes
pipe_1 = Pipe(WIDTH_SC, randint(100,360))
pipe_2 = Pipe(pipe_1.x+DISTANCE_PIPE, randint(100,360))
pipe_3 = Pipe(pipe_2.x+DISTANCE_PIPE, randint(100,360))
pipe_4 = Pipe(pipe_3.x+DISTANCE_PIPE,randint(100,360))

# update coordinates
PIPE_X_AFTER = (pipe_4.x - (pipe_1.x + PIPE_WIDTH )) + DISTANCE_PIPE 

while running:
    clock.tick(60)
    
    current_time = time()
    
    screen.fill(BG_COLOR)
    
    #draw 4 tubes above and draw 4 tubes below
    pipe_1.draw()
    pipe_2.draw()
    pipe_3.draw()
    pipe_4.draw()
    
    #draw bird
    bird = pygame.draw.rect(screen, BIRD_COLOR, (BIRD_X,BIRD_y,BIRD_WIDTH, BIRD_HEIGHT))
    
    #start time
    if start == False:
        time_text = time_font.render(str(total_secs), True, (225,204,225))
        time_text_rect = time_text.get_rect(center=(WIDTH_SC/2,250))
        screen.blit(time_text, time_text_rect)
        if current_time - start_time >= update_time:
            total_secs -= 1
            start_time = current_time
            if total_secs == -1:
                start = True
    
    elif start == True:
        #bird fall
        BIRD_y += drop_velocity
        drop_velocity += GRAVITY
        
        # #collide with the wall
        if BIRD_y < 0 or BIRD_y > HEIGHT_SC - BIRD_HEIGHT:
            game_over = True
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #game control buttons
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                drop_velocity = -8
            
            #Play again when you lose
            if event.key == pygame.K_RETURN and game_over == True:
                game_over = False
                score = 0
                PIPE_VELOCITY = 5 #reset pipe travel speed
                
                #redraw the pipes
                pipe_1.x = WIDTH_SC 
                pipe_1.height_pipe = randint(100,360)

                pipe_2.x = pipe_1.x + DISTANCE_PIPE
                pipe_2.height_pipe = randint(100,360)

                pipe_3.x= pipe_2.x + DISTANCE_PIPE
                pipe_3.height_pipe = randint(100,360)

                pipe_4.x = pipe_3.x + DISTANCE_PIPE
                pipe_4.height_pipe = randint(100,360)

                #reposition the bird
                BIRD_X = 80
                BIRD_y = 300
                
                #count back time
                start = False
                start_time = time()
                total_secs = 3
    
    score_text = font.render("Score: "+str(score), True, BLUE)
    screen.blit(score_text, (10,10))
    
    #when you close
    if game_over == True:
        screen.blit(game_over_text, game_over_text_rect)
        screen.blit(play_again_text, play_again_text_rect)
        #stop screen
        drop_velocity = 0
        PIPE_VELOCITY = 0
    pygame.display.flip()
    
pygame.quit()     