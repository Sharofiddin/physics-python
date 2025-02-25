import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
BALL_RADIUS = 20
GRAVITY = 0.5
BOUNCE_DAMPING = 0.8  # Energy loss on bounce
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Ball properties
ball_x, ball_y = WIDTH // 2, HEIGHT // 4  # Start near the top
ball_velocity_y = 0

# Pygame setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball Simulation")
clock = pygame.time.Clock()

# Main loop
running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Physics update
    ball_velocity_y += GRAVITY  # Apply gravity
    ball_y += ball_velocity_y  # Move the ball

    # Bounce if hitting the floor
    if ball_y + BALL_RADIUS >= HEIGHT:
        ball_y = HEIGHT - BALL_RADIUS  # Keep it above ground
        ball_velocity_y *= -BOUNCE_DAMPING  # Reverse & dampen velocity

    # Draw ball
    pygame.draw.circle(screen, BLUE, (ball_x, int(ball_y)), BALL_RADIUS)

    # Update display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
