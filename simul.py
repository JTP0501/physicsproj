import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rotational  Dynamics Simulation - Falling Mass")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (128, 0, 128)
GRAY = (169, 169, 169)

# Pulley parameters
pulley_mass = 20  # kg
pulley_radius = 40  # pixels, smaller size
pulley_center = (300, 100)

# Weight parameters
weight_mass = 10  # kg
weight_width, weight_height = 40, 40  # Size of the weight

# Simulation parameters
drop_duration = 2  # seconds
fps = 60  # frames per second
drop_speed = (height - pulley_center[1] - weight_height) / (drop_duration * fps)  # pixels per frame

# Weight position
initial_weight_x_offset = weight_width
initial_weight_y_offset = -(weight_height) + 5
weight_x = pulley_center[0] + initial_weight_x_offset - weight_width // 2  # Centered below the pulley
weight_y = pulley_center[1] + initial_weight_y_offset + pulley_radius  # Starting position below the pulley

# Pulley rotation
angle = 0
angle_speed = (2 * math.pi) / (drop_duration * fps)

# Font for the text
font = pygame.font.SysFont(None, 24)

# Main loop
running = True
clock = pygame.time.Clock()
frames = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill(BLACK)

    # Draw pulley (rotated)
    pygame.draw.circle(screen, PURPLE, pulley_center, pulley_radius)
    pygame.draw.line(screen, WHITE, pulley_center, 
                     (pulley_center[0] + pulley_radius * math.cos(angle), pulley_center[1] + pulley_radius * math.sin(angle)), 2)

    # Draw rope
    pygame.draw.line(screen, WHITE, (pulley_center[0] + initial_weight_x_offset, pulley_center[1] + initial_weight_y_offset + pulley_radius), 
                     (weight_x + weight_width // 2, weight_y), 2)

    # Draw weight
    pygame.draw.rect(screen, GRAY, (weight_x, weight_y, weight_width, weight_height))

    # Draw weight text
    weight_text = font.render(f'{weight_mass} kg', True, WHITE)
    screen.blit(weight_text, (weight_x + 5, weight_y + weight_height // 4))

    # Update display
    pygame.display.flip()

    # Update physics
    if frames < drop_duration * fps:
        weight_y += drop_speed
        angle += angle_speed
        frames += 1

    clock.tick(fps)

# Quit Pygame
pygame.quit()
sys.exit()
