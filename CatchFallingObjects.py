import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

# Window setup
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Apple")

# Load images
basket_img = pygame.image.load("basket.jpeg")
basket_img = pygame.transform.scale(basket_img, (100, 60))

apple_img = pygame.image.load("apple.jpeg")
apple_img = pygame.transform.scale(apple_img, (40, 40))

# Load sounds
catch_sound = pygame.mixer.Sound("catch.wav")
miss_sound = pygame.mixer.Sound("drop.wav")

# Colors & fonts
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
font = pygame.font.SysFont("Arial", 28)

# Basket setup
player = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 70, 100, 60)
player_speed = 10

# Apple setup (single apple)
apple = pygame.Rect(random.randint(0, WIDTH - 40), 0, 40, 40)
fall_speed = 5
speed_increase_rate = 0.1

score = 0
misses = 0
clock = pygame.time.Clock()
running = True

# Main game loop
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move basket
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.x += player_speed

    # Move apple
    apple.y += int(fall_speed)

    # Draw objects
    screen.blit(basket_img, player.topleft)
    screen.blit(apple_img, apple.topleft)

    # Collision detection
    if player.colliderect(apple):
        score += 1
        catch_sound.play()
        fall_speed += speed_increase_rate
        apple.y = 0
        apple.x = random.randint(0, WIDTH - 40)

    # If missed
    elif apple.y > HEIGHT:
        misses += 1
        miss_sound.play()
        apple.y = 0
        apple.x = random.randint(0, WIDTH - 40)

    # Draw score and misses
    score_text = font.render(f"Score: {score}", True, BLACK)
    miss_text = font.render(f"Misses: {misses}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(miss_text, (10, 40))

    # Game Over
    if misses >= 5:
        game_over_text = font.render(f"Game Over! Final Score: {score}", True, (200, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(3000)
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
