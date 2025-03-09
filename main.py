import time
import pygame
import random #  för att randomiza bollens riktning efter mål


pygame.init()

# Fönsterinställningar
WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG by glennis")

FPS = 60

# Färger
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARKBLUE = (120, 120, 120)
RED = (150, 0, 0)

# Paddel & Boll Storlek
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7

# Score Variabler
SCORE_FONT = pygame.font.SysFont("comicsans", 50)
WINNING_SCORE = 5

BG = pygame.image.load("5920.jpg")
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

# Reptil Storlek
REPTILES_WIDTH, REPTILES_HEIGHT = 15, 5

# region REPTILE
class Reptile:
    COLOR = WHITE
    VEL = 6

    def __init__(self, x, y, width, height, direction):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.direction = direction

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self):
        self.x += self.VEL * self.direction

# region PADDLE
class Paddle:
    COLOR = WHITE
    VEL = 4

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

# region BALL
class Ball:
    MAX_VEL = 6
    START_MAX_VEL = 6
    MAX_INCREASE = 3
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.START_MAX_VEL
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
        self.x_vel = self.START_MAX_VEL
        if random.random() < 0.5:
            self.x_vel *= -1

    def increase_velocity(self):
        if abs(self.x_vel) < self.START_MAX_VEL + self.MAX_INCREASE:
            self.x_vel += 1 if self.x_vel > 0 else -1

# region DRAW
def draw(win, paddles, ball, left_score, right_score, left_reptiles, right_reptiles, elapsed_time):
    win.blit(BG, (0, 0))
    
    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 20))
    win.blit(right_score_text, (WIDTH * 3 // 4 - right_score_text.get_width() // 2, 20))

    for paddle in paddles:
        paddle.draw(win)

    for i in range(10, HEIGHT, HEIGHT // 20):
        if i % 2 == 0:
            pygame.draw.rect(win, DARKBLUE, (WIDTH // 2 - 5, i, 10, HEIGHT // 20))

    ball.draw(win)

    for reptile in left_reptiles + right_reptiles:
        reptile.draw(win)

    timer_text = SCORE_FONT.render(f"Time: {elapsed_time}", 1, WHITE)
    win.blit(timer_text, (WIDTH // 2 - timer_text.get_width() // 2, 20))

    pygame.display.update()

# region COLLISION
def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT or ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0:
        if left_paddle.y <= ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -y_vel
    else:
        if right_paddle.y <= ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1
                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -y_vel

# region MOVEMENT
def handle_paddle_movement(keys, left_paddle, right_paddle, left_reptiles, right_reptiles, left_last_shot, right_last_shot, COOLDOWN):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)

    current_time = time.time()
    if keys[pygame.K_LCTRL] and current_time - left_last_shot > COOLDOWN:
        left_reptiles.append(Reptile(left_paddle.x + left_paddle.width, left_paddle.y + left_paddle.height // 2, REPTILES_WIDTH, REPTILES_HEIGHT, 1))
        left_last_shot = current_time

    if keys[pygame.K_RCTRL] and current_time - right_last_shot > COOLDOWN:
        right_reptiles.append(Reptile(right_paddle.x - REPTILES_WIDTH, right_paddle.y + right_paddle.height // 2, REPTILES_WIDTH, REPTILES_HEIGHT, -1))
        right_last_shot = current_time

    return left_last_shot, right_last_shot


def increase_ball_velocity_if_no_score(ball, no_score_start_time):
    if time.time() - no_score_start_time >= 10:
        ball.increase_velocity()
        no_score_start_time = time.time()
    return no_score_start_time

# region MAIN
def main():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    left_score = 0
    right_score = 0

    left_reptiles = []
    right_reptiles = []
    left_last_shot = 0
    right_last_shot = 0
    COOLDOWN = 3

    start_time = time.time()
    no_score_start_time = time.time()
    
# region WHILE-LOOP
    while run:
        clock.tick(FPS)

        keys = pygame.key.get_pressed()
        left_last_shot, right_last_shot = handle_paddle_movement(keys, left_paddle, right_paddle, left_reptiles, right_reptiles, left_last_shot, right_last_shot, COOLDOWN)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        for reptile in list(left_reptiles):
            reptile.move()
            if reptile.x < 0 or reptile.x > WIDTH:
                left_reptiles.remove(reptile)

        for reptile in list(right_reptiles):
            reptile.move()
            if reptile.x < 0 or reptile.x > WIDTH:
                right_reptiles.remove(reptile)

        for reptile in list(left_reptiles):
            if right_paddle.x < reptile.x + reptile.width and right_paddle.x + right_paddle.width > reptile.x and \
                    right_paddle.y < reptile.y + reptile.height and right_paddle.y + right_paddle.height > reptile.y:
                left_score += 1
                left_reptiles.remove(reptile)

        for reptile in list(right_reptiles):
            if left_paddle.x < reptile.x + reptile.width and left_paddle.x + left_paddle.width > reptile.x and \
                    left_paddle.y < reptile.y + reptile.height and left_paddle.y + left_paddle.height > reptile.y:
                right_score += 1
                right_reptiles.remove(reptile)

        if ball.x < 0 or ball.x > WIDTH:
            if ball.x < 0:
                right_score += 1
            else:
                left_score += 1
            ball.reset()
            no_score_start_time = time.time()

        no_score_start_time = increase_ball_velocity_if_no_score(ball, no_score_start_time)

        elapsed_time = int(time.time() - start_time)

        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score, left_reptiles, right_reptiles, elapsed_time)

        if left_score >= WINNING_SCORE or right_score >= WINNING_SCORE:
            win_text = "Left Player Won!" if left_score > right_score else "Right Player Won!"
            text = SCORE_FONT.render(win_text, 1, GREEN)
            WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.update()

            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()


if __name__ == '__main__':
    main()
