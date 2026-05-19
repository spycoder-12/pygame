import pygame
import random

pygame.init()

# Screen
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

# Settings
BLOCK = 10
SPEED = 15

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

bg_r, bg_g, bg_b = 50, 153, 213
color_speed = 1

# Fonts
font_small = pygame.font.SysFont("bahnschrift", 25)
font_big = pygame.font.SysFont("comicsansms", 35)


# ---------- High Score ----------
def load_high_score():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except:
        return 0


def save_high_score(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))


# ---------- Draw Functions ----------
def draw_snake(snake):
    for x, y in snake:
        pygame.draw.rect(screen, GREEN, [x, y, BLOCK, BLOCK])


def show_score(score, high_score):
    s = font_big.render(f"Score: {score}", True, WHITE)
    h = font_small.render(f"High: {high_score}", True, YELLOW)

    screen.blit(s, (10, 5))
    screen.blit(h, (10, 40))


def show_message(text):
    msg = font_small.render(text, True, RED)
    screen.blit(msg, (WIDTH // 6, HEIGHT // 3))
    
def update_background():
    global bg_r, bg_g, bg_b

    bg_r += random.choice([-1, 0, 1]) * color_speed
    bg_g += random.choice([-1, 0, 1]) * color_speed
    bg_b += random.choice([-1, 0, 1]) * color_speed

    # keep values in range
    bg_r = max(0, min(255, bg_r))
    bg_g = max(0, min(255, bg_g))
    bg_b = max(0, min(255, bg_b))

    return (bg_r, bg_g, bg_b)


# ---------- Game Loop ----------
def game_loop():
    while True:  # restart loop

        # Initial state
        x = WIDTH // 2
        y = HEIGHT // 2
        dx = BLOCK
        dy = 0
        direction = "RIGHT"

        snake = []
        length = 1

        food_x = random.randrange(0, WIDTH - BLOCK, BLOCK)
        food_y = random.randrange(0, HEIGHT - BLOCK, BLOCK)

        high_score = load_high_score()

        game_over = False
        game_close = False

        while not game_over:

            # ----- Game Over Screen -----
            while game_close:
                bg_color = update_background()
                screen.fill(bg_color)
                show_message("You Lost! C-Play Again Q-Quit")
                show_score(length - 1, high_score)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            pygame.quit()
                            return
                        elif event.key == pygame.K_c:
                            game_close = False
                            game_over = True

            # ----- Controls -----
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and direction != "RIGHT":
                        direction = "LEFT"
                        dx = -BLOCK
                        dy = 0
                    elif event.key == pygame.K_RIGHT and direction != "LEFT":
                        direction = "RIGHT"
                        dx = BLOCK
                        dy = 0
                    elif event.key == pygame.K_UP and direction != "DOWN":
                        direction = "UP"
                        dx = 0
                        dy = -BLOCK
                    elif event.key == pygame.K_DOWN and direction != "UP":
                        direction = "DOWN"
                        dx = 0
                        dy = BLOCK

            # ----- Move -----
            x += dx
            y += dy

            # ----- Wall Collision -----
            if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
                game_close = True

            bg_color = update_background()
            screen.fill(bg_color)

            # Food
            pygame.draw.rect(screen, YELLOW, [food_x, food_y, BLOCK, BLOCK])

            # Snake
            head = [x, y]
            snake.append(head)

            if len(snake) > length:
                del snake[0]

            # Self Collision
            for part in snake[:-1]:
                if part == head:
                    game_close = True

            draw_snake(snake)
            show_score(length - 1, high_score)

            pygame.display.update()

            # ----- Eat Food -----
            if x == food_x and y == food_y:
                food_x = random.randrange(0, WIDTH - BLOCK, BLOCK)
                food_y = random.randrange(0, HEIGHT - BLOCK, BLOCK)
                length += 1

                if length - 1 > high_score:
                    high_score = length - 1
                    save_high_score(high_score)

            clock.tick(SPEED)


# Run game
game_loop()