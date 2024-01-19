import pygame
pygame.init() #after importing pygame we should initialize it

WIDTH, HEIGHT = 700, 500 #size of the game window
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #constant meanings can't change
pygame.display.set_caption("Pong") #caption title
FPS = 60 #time(clock) FPS
WHITE = (255, 255, 255) #RGB
BLACK = (0, 0, 0) #RGB
PINK = (255,105,180) #RGB
BLUE = (135,206,235) #RGB
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7
SCORE_FONT = pygame.font.SysFont("comicans", 50)
WINNING_SCORE = 10

class Paddle: #creating the objects and giving them their coordinations
    COLOR = WHITE
    VEL = 4 #add speed to the bars
    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def draw(self,win):
        pygame.draw.rect(
            win, self.COLOR, (self.x, self.y, self.width, self.height)) # making the window as rectangle shape
    def move(self, up=True): #movement func
        if up:
            self.y -= self.VEL #move the paddle up
        else:
            self.y += self.VEL #move the paddle down
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

class Ball: #creating the ball object
    MAX_VEL = 5
    COLOR = BLUE

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1

def draw(win, paddles, ball, left_score, right_score): #coloring the window
    win.fill(BLACK)
    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width()//2, 20))

    for paddle in paddles:
        paddle.draw(win)
    #******DASH LINE******
    for i in range(10, HEIGHT, HEIGHT//20): #we'll do this for loop for 20 times with 10 pixel rectangles
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, PINK, (WIDTH//2, i, 1, HEIGHT//20))
    #*********************
    ball.draw(win)
    pygame.display.update()

def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT: #ball hits the bottom
        ball.y_vel += -1 #change the direction
    elif ball.y - ball.radius <= 0: #ball hits the upper
        ball.y_vel *= -1 # change the direction
    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1 #change the direction

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1 #change the direction

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

def handle_paddle_movement(keys, left_paddle, right_paddle): #defining paddle movements func
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0: #with that, paddle can't go outside of the window
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)

#This'll be the main loop that constantly running everything in the background.
def main():
    run = True
    clock = pygame.time.Clock()
    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT) #10 pixels padding left side and middle of the screen
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT) #same procedure is applied to the right side
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)
    left_score = 0
    right_score = 0

    while run:
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score) #calling the draw func

        for event in pygame.event.get(): #for the actions (like clicking, quitting the game...)
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)
        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()
        won = False
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "Blue Player WON!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Pink Player WON!"

        if won:
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

    pygame.quit()

if __name__ == '__main__': #being sure of running the main func
    main()