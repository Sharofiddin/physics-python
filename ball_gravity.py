import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
BALL_RADIUS = 20
GRAVITY = 0.5
BOUNCE_DAMPING = 0.8  # Energy loss on bounce
AIR_RESISTANCE = .99
FPS = 60
NUM_BALLS = 5

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
COLORS = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,165,0)]

class Ball:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3,3) # Random initial horizontal velocity
        self.vy = random.uniform(-2,2) # Random initial vertical velocity
        self.color = color
    def update(self):
        self.vy += GRAVITY # Apply gravity
        self.vx *= AIR_RESISTANCE # Apply air resistance
        self.vy *= AIR_RESISTANCE

        self.x += self.vx
        self.y += self.vy

        # Bounce of walls
        if self.x - BALL_RADIUS <= 0 or self.x + BALL_RADIUS >= WIDTH:
            self.vx *= -BOUNCE_DAMPING
            self.x = max(BALL_RADIUS, min(WIDTH - BALL_RADIUS, self.x))
        # Bounce of floor the floor
        if self.y + BALL_RADIUS >= HEIGHT:
            self.y = HEIGHT - BALL_RADIUS  # Keep it above ground
            self.vy *= -BOUNCE_DAMPING  # Reverse & dampen velocity
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), BALL_RADIUS)

balls = [Ball(random.randint(BALL_RADIUS, WIDTH - BALL_RADIUS),
              random.randint(BALL_RADIUS, HEIGHT // 2),
              random.choice(COLORS)) for _ in range(NUM_BALLS)]


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

    # Update and draw balls
    for ball in balls:
       ball.update()
       ball.draw(screen)
    # Update display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
