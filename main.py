import pygame
import random

from pygame import K_RIGHT, K_LEFT

pygame.init()

SCREEN_WIDTH = 730
SCREEN_HEIGHT = 600
GAP = 10
SIDE = 30
run = True

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brick Breakout")
clock = pygame.time.Clock()
pygame.font.init()

paddle_x = 450
paddle_y = 570
PADDLE_WIDTH = 120
PADDLE_HEIGHT = 15

BRICK_WIDTH = 50
BRICK_HEIGHT = 30
score = 0
is_pause = False

ball_x = 350
ball_y = 400
x_vel = 400
y_vel = 400
RAD = 10
bricks_drew = False

BRICK_COLORS = [
    (255, 0, 0),      # Red
    (255, 165, 0),    # Orange
    (255, 255, 0),    # Yellow
    (0, 255, 0),      # Green
    (0, 255, 255),    # Cyan
    (0, 104, 199),      # Blue
    "PURPLE",    # Purple
]

bricks = []
for j in range(1, 8):
    bricks.append([])
    for i in range(0,12):
        x = GAP*(i+1) + BRICK_WIDTH *i
        y = GAP*j + BRICK_HEIGHT *j
        bricks[-1].append([x,y, random.choice(BRICK_COLORS), True])

    bricks[-1].append("R")

def check_collision():
    global x_vel, y_vel, ball_y, ball_x, score, is_pause

    # Paddle
    if (ball_x+RAD > paddle_x and ball_x+RAD < paddle_x+PADDLE_WIDTH) and (ball_y+RAD+1>paddle_y and ball_y+RAD+1 < paddle_y+PADDLE_HEIGHT):
        ball_y = paddle_y-RAD
        y_vel = -y_vel

    # Wall
    if ball_x-RAD < 0:
        x_vel = -x_vel
        ball_x = RAD

    elif ball_x+RAD+1 > SCREEN_WIDTH:
        x_vel = -x_vel
        ball_x = SCREEN_WIDTH-RAD

    if ball_y-RAD < 30:
        y_vel = -y_vel
        ball_y = 30 + RAD

    elif ball_y+RAD > SCREEN_HEIGHT:
        y_vel = -y_vel
        ball_y = SCREEN_HEIGHT - RAD
        is_pause = True

    # Bricks
    for i, row in enumerate(bricks):
        if row[-1] == "R":
            for j, data in enumerate(row):
                if not type(data) == str:
                    x, y, color, visibility = data #

                    if visibility:
                        if (ball_x+RAD > x and ball_x-RAD < x+BRICK_WIDTH) and (y<ball_y-RAD and y+BRICK_HEIGHT > ball_y-RAD): # Bottom
                            visibility = False
                            data[-1] = "W"
                            y_vel = -y_vel
                            score += 1

                        elif (x < ball_x-RAD and x+BRICK_WIDTH > ball_x-RAD) and (y < ball_y-RAD and y + BRICK_HEIGHT > ball_y-RAD): # Left
                            visibility = False
                            data[-1] = "W"
                            x_vel = -x_vel
                            score += 1

                        elif (x < ball_x + RAD and x + BRICK_WIDTH > ball_x + RAD) and (y < ball_y + RAD and y + BRICK_HEIGHT > ball_y - RAD):  # Right
                            visibility = False
                            data[-1] = "W"
                            x_vel = -x_vel
                            score += 1

                        elif (x < ball_x + RAD and x + BRICK_WIDTH > ball_x - RAD and ball_y + RAD >= y and ball_y - RAD < y):  # Top
                            visibility = False
                            data[-1] = "W"
                            y_vel = -y_vel
                            score += 1

                    bricks[i][j] = [x,y,color,visibility]

font_1 = pygame.font.SysFont('Courier New', 30)

while run:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill('BLACK')

    keys = pygame.key.get_pressed()

    if keys[K_RIGHT] and paddle_x+400*dt + PADDLE_WIDTH + 5 < SCREEN_WIDTH and not is_pause:
        paddle_x += 500*dt

    elif keys[K_LEFT] and -5+paddle_x-400*dt > 0 and not is_pause:
        paddle_x -= 500*dt

    pygame.draw.rect(screen, 'WHITE', (paddle_x,paddle_y, PADDLE_WIDTH,PADDLE_HEIGHT))
    pygame.draw.circle(screen, 'WHITE', (ball_x,ball_y), RAD)

    pygame.draw.line(screen, 'white', (0,30),(SCREEN_WIDTH, 30))
    #pygame.draw.line(screen, 'white', (0, 320), (SCREEN_WIDTH, 320))

    for row in bricks:
        for data in row:
            if not type(data) == str:
                x, y, color, visibility = data
                if visibility:
                    pygame.draw.rect(screen, color, (x, y, BRICK_WIDTH, BRICK_HEIGHT))

    if not is_pause:
        ball_x += x_vel * dt
        ball_y += y_vel * dt
        check_collision()

    else:
        text = font_1.render(f"Game Over", 1, 'WHITE')
        screen.blit(text, (-80+SCREEN_WIDTH//2, 0))

    text = font_1.render(f"Score: {score}", 1, 'WHITE')
    screen.blit(text, (0,0))

    pygame.display.update()