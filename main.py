import time
import pygame
pygame.init()

# UTVECKLING
#           ADD A BALL AFTER A CURTAIN AMOUNT OF TIME
#           MAKE "COINS/POINTS" SHOW UP IN THE MAP TO TRAIN MORE IN COLLISION
#           MAKE THE BALL CHANGE VELOCITY AFTER SOME TIME IF NO ONE SCORES
# CHECK -   ADD A COOL BACK GROUND
# CHECK -   MAKE A PADDLE SHOT REPTILES WHICH THE OTHER PLAYER SHOULD AVOID
#           ADD SOME RANDOMS, MAYBE TO THE ANGLE OF WICH THE BALL GOES

WIDTH, HEIGHT = 900, 600 # FÖNSTRETS STORLEK
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("Pong by glennis")  # Visar "Pong" i fönstret

FPS = 60 

# FÄRGER SOM ANVÄNDS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARKBLUE = (120, 120, 120)
RED = (150, 0, 0)

# PADDLE & BALL STORLEK
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7

# SCORE VARIABELS
SCORE_FONT = pygame.font.SysFont("comicsans", 50)
WINNING_SCORE = 5

# ------------------------- REPTILES ---------------------------
BG = pygame.image.load("5920.jpg")
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

REPTILES_WIDTH, REPTILES_HEIGHT = 15, 5

class Reptile:
    COLOR = RED
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

# ----------------------------------------------------------------

class Paddle:  # för att vi sak ha fler paddles

    COLOR = WHITE  # Klassattribut för ALLA paddles
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


class Ball:
    MAX_VEL = 6
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = self.original_x = x  # Skapar en separat variabel för att kunna reseta bollen
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
        self.x_vel *= -1  # Ändrar riktningen på bollen när någon gjort "Mål"


def draw(win, paddles, ball, left_score, right_score, left_reptiles, right_reptiles):
    # win.fill(BLACK)
    win.blit(BG, (0, 0))

    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 20))  # För att visa texten på mitten av första halvan av rutan
    win.blit(right_score_text, (WIDTH * (3 / 4) - right_score_text.get_width() // 2, 20))  # samma fast tre fjärdedelar så den hamnar på mitten av den andra "rutan"

    # PADDLES
    for paddle in paddles:
        paddle.draw(win)

    # MITTLINJE
    for i in range(10, HEIGHT, HEIGHT // 20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, DARKBLUE, (WIDTH // 2 - 5, i, 10, HEIGHT // 20))

    ball.draw(win)

# ------------------------- REPTILES ---------------------------

    # REPTILES
    for reptile in left_reptiles + right_reptiles:
        reptile.draw(win)

# -------------------------------------------------------------

    pygame.display.update()


def handle_collision(ball, left_paddle, right_paddle):
    # CEILING
    if ball.y + ball.radius >= HEIGHT:  # ta med radius för att den ska ta "kanten" på bollen och inte centrum
        ball.y_vel *= -1  # reverse direction
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    # PADDLES
    if ball.x_vel < 0:  # Om den åker vänster
        if left_paddle.y <= ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1  # byt direction

                middle_y = left_paddle.y + left_paddle.height / 2  # paddels mitt
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    else:  # right paddle
        if right_paddle.y <= ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2  # paddels mitt
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel


def handle_paddle_movement(keys, left_paddle, right_paddle, left_reptiles, right_reptiles, left_last_shot, right_last_shot, COOLDOWN):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)

    # -------------------------REPTILES ---------------------------

    current_time = time.time()
    if keys[pygame.K_LCTRL] and current_time - left_last_shot > COOLDOWN:
        left_reptiles.append(Reptile(left_paddle.x + left_paddle.width, left_paddle.y + left_paddle.height // 2, REPTILES_WIDTH, REPTILES_HEIGHT, 1))
        left_last_shot = current_time

    if keys[pygame.K_RCTRL] and current_time - right_last_shot > COOLDOWN:
        right_reptiles.append(Reptile(right_paddle.x - REPTILES_WIDTH, right_paddle.y + right_paddle.height // 2, REPTILES_WIDTH, REPTILES_HEIGHT, -1))
        right_last_shot = current_time

    return left_last_shot, right_last_shot

    # --------------------------------------------------------------

def main():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)  # För att centrara paddeln, annars hamnat översta vänstra hörnet där man sätter rektangeln
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)  # Fönstrets storlek, minus 10, minus paddelns width
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    left_score = 0
    right_score = 0

    # ------------------------- REPTILES ---------------------------
    left_reptiles = []
    right_reptiles = []
    left_last_shot = 0
    right_last_shot = 0
    COOLDOWN = 3  # SÄTTS HÄR FÖR ATT DET INTE ÄR EN INNEBOENDE EGENSKAP HOS EN ENSKILD REPTIL
    
    # -------------------------REPTILES---------------------------

    while run:
        clock.tick(FPS)

        keys = pygame.key.get_pressed()
        left_last_shot, right_last_shot = handle_paddle_movement(keys, left_paddle, right_paddle, left_reptiles, right_reptiles, left_last_shot, right_last_shot, COOLDOWN)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        # Flytta och hantera borttagning av reptiler
        for reptile in list(left_reptiles):  # Iterera över en kopia
            reptile.move()
            if reptile.x < 0 or reptile.x > WIDTH:
                left_reptiles.remove(reptile)

        for reptile in list(right_reptiles):  # Iterera över en kopia
            reptile.move()
            if reptile.x < 0 or reptile.x > WIDTH:
                right_reptiles.remove(reptile)

        # ------------------------- REPTILES ---------------------------

        # Kontrollera kollisioner mellan reptiler och paddlar
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
                
        # -----------------------------------------------------------

        # Hantera poäng för bollen
        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()

        # Rita allt - FLYTTAD HIT FÖR ATT VISA SCORE INNAN ALLT RESETTAS VID VINST
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score, left_reptiles, right_reptiles)

        # Kontrollera om någon har vunnit
        if left_score >= WINNING_SCORE or right_score >= WINNING_SCORE:
            if left_score > right_score:
                win_text = "Left Player Won!" # Sätter samma variabelnamn
            else:
                win_text = "Right Player Won!"

            text = SCORE_FONT.render(win_text, 1, GREEN)
            WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.update()
            
        # Resettar allt för ny omgång    
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
    
    pygame.quit()


if __name__ == '__main__':
    main()
