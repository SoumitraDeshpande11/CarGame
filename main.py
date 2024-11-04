import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Racing Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (169, 169, 169)
BLUE = (30, 144, 255)
YELLOW = (255, 255, 0)

CAR_WIDTH, CAR_HEIGHT = 50, 100
car_rect = pygame.Rect((SCREEN_WIDTH // 2 - CAR_WIDTH // 2, SCREEN_HEIGHT - 120), (CAR_WIDTH, CAR_HEIGHT))

OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 50, 100
obstacle_speed = 5
obstacles = []

clock = pygame.time.Clock()
score = 0
game_speed = 5
game_over = False

font = pygame.font.Font(None, 36)

def create_obstacle():
    x_position = random.randint(0, SCREEN_WIDTH - OBSTACLE_WIDTH)
    y_position = -OBSTACLE_HEIGHT
    return pygame.Rect(x_position, y_position, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)

def move_obstacles():
    for obstacle in obstacles:
        obstacle.y += game_speed
    obstacles[:] = [obs for obs in obstacles if obs.y < SCREEN_HEIGHT]

def check_collision():
    for obstacle in obstacles:
        if car_rect.colliderect(obstacle):
            return True
    return False

def update_score():
    global score
    score += 1

def display_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def restart_game():
    global obstacles, car_rect, score, game_speed, game_over
    obstacles = []
    car_rect.centerx = SCREEN_WIDTH // 2
    score = 0
    game_speed = 5
    game_over = False

def draw_car(surface, rect):
    pygame.draw.rect(surface, BLUE, rect)
    pygame.draw.rect(surface, BLACK, (rect.x + 5, rect.y + 10, 40, 60))
    pygame.draw.rect(surface, WHITE, (rect.x + 12, rect.y + 15, 25, 50))
    pygame.draw.circle(surface, YELLOW, (rect.x + 10, rect.y + 5), 5)
    pygame.draw.circle(surface, YELLOW, (rect.x + 40, rect.y + 5), 5)
    pygame.draw.circle(surface, BLACK, (rect.x + 10, rect.y + 85), 8)
    pygame.draw.circle(surface, BLACK, (rect.x + 40, rect.y + 85), 8)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_SPACE:
                restart_game()

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and car_rect.left > 0:
            car_rect.x -= 5
        if keys[pygame.K_RIGHT] and car_rect.right < SCREEN_WIDTH:
            car_rect.x += 5

        if random.randint(0, 30) == 1:
            obstacles.append(create_obstacle())
        move_obstacles()

        game_speed = 5 + score // 100

        if check_collision():
            game_over = True

        update_score()

    screen.fill(GRAY)
    pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH // 4, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))

    draw_car(screen, car_rect)
    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, obstacle)

    display_score()

    if game_over:
        game_over_text = font.render("Game Over!", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        restart_text = font.render("Press SPACE to Restart", True, BLACK)
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2))

    pygame.display.flip()
    clock.tick(30)
