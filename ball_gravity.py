import pygame
import sys
import random
import matplotlib.pyplot as plt
from collections import deque

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
BALL_RADIUS = 20
GRAVITY = 0.5
BOUNCE_DAMPING = 0.9  # Energy loss on bounce
AIR_RESISTANCE = 0.99
FPS = 60
NUM_BALLS = 5
MASS = 1
ENERGY_HISTORY_LENGTH = 500
MOVEMENT_TRESHOLD = 0.1
# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
COLORS = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,165,0)]

paused = False

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
        # Bounce off the floor
        if self.y + BALL_RADIUS >= HEIGHT:
            self.y = HEIGHT - BALL_RADIUS  # Keep it above ground
            self.vy *= -BOUNCE_DAMPING  # Reverse & dampen velocity
            if abs(self.vy) < 1:
                self.vy = 0

    def energy(self):
        kinetic_energy = 0.5 * MASS * (self.vx**2 + self.vy**2)
        potential_energy = MASS * GRAVITY + (HEIGHT - self.y)
        total_energy = kinetic_energy + potential_energy
        return kinetic_energy, potential_energy, total_energy

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), BALL_RADIUS)

    def is_moving(self):
        return abs(self.vx) > MOVEMENT_TRESHOLD or abs(self.vy) > MOVEMENT_TRESHOLD


balls = [Ball(random.randint(BALL_RADIUS, WIDTH - BALL_RADIUS),
              random.randint(BALL_RADIUS, HEIGHT // 2),
              random.choice(COLORS)) for _ in range(NUM_BALLS)]


# Pygame setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball Simulation")
clock = pygame.time.Clock()

ke_history = deque(maxlen= ENERGY_HISTORY_LENGTH)
pe_history = deque(maxlen= ENERGY_HISTORY_LENGTH)
te_history = deque(maxlen= ENERGY_HISTORY_LENGTH)
time_steps = deque(maxlen= ENERGY_HISTORY_LENGTH)
frame_count = 0

# Matplotlib setup
plt.ion()
fig, ax = plt.subplots()
ax.set_ylim(0, 5000)
ax.set_xlim(0, ENERGY_HISTORY_LENGTH)

ke_line, = ax.plot([], [], label="Kinetic Energy", color="r")
pe_line, = ax.plot([], [], label="Potential Energy", color="b")
te_line, = ax.plot([], [], label="Total Energy", color="g")
ax.legend()

def update_graph():
    ke_line.set_data(time_steps, ke_history)
    pe_line.set_data(time_steps, pe_history)
    te_line.set_data(time_steps, te_history)
    ax.set_xlim(max(0, frame_count - ENERGY_HISTORY_LENGTH), frame_count)
    ax.set_ylim(0, max(max(ke_history, default=1), max(pe_history, default=1), max(te_history, default=1)))
    plt.draw()
    plt.pause(0.01)
# Main loop
running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
    if not paused:
      total_ke, total_pe, total_te = 0,0,0
      all_stopped = True
      # Update and draw balls
      for ball in balls:
         ball.update()
         ball.draw(screen)
         ke, pe, te = ball.energy()
         total_ke += ke
         total_pe += pe
         total_te += te
         if ball.is_moving():
             all_stopped = False
      if not all_stopped:
        ke_history.append(total_ke)
        pe_history.append(total_pe)
        te_history.append(total_te)
        time_steps.append(frame_count)
        frame_count += 1
        update_graph()

        # Update display
        pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
