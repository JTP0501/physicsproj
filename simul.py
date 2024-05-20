import pygame
import sys
import math
import button

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rotational Dynamics Simulation - Falling Mass")

# Buttons
start_img = pygame.image.load('start_btn.png').convert_alpha()
exit_img = pygame.image.load('exit_btn.png').convert_alpha()
title_img = pygame.image.load('menu_title.png').convert_alpha()

# Button instances
start_button = button.Button(251, 240, start_img, 0.35)
exit_button = button.Button(258, 298, exit_img, 0.35)
menu_title = button.Button(95, 53, title_img, 0.7)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (128, 0, 128)
GRAY = (169, 169, 169)

# Pulley parameters
pulley_mass = 20  # kg
pulley_radius = 40  # pixels, smaller size
pulley_center = (300, 100)
border_thickness = 2  # Thickness of the border
fulcrum_radius = 3  # Radius of the fulcrum

# Weight parameters
weight_mass = 10  # kg
weight_width, weight_height = 40, 40  # Size of the weight
weight_border_thickness = 1  # Thickness of the border for the weight box
weight_second_border_thickness = 4

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
small_font = pygame.font.SysFont(None, 18)

# Main loop
running = True
started = False  # Simulation started flag
clock = pygame.time.Clock()
frames = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill((202, 228, 241))

    if not started:
        # Draw buttons and title
        menu_title.draw(screen)
        if start_button.draw(screen):
            started = True  # Start the simulation

        if exit_button.draw(screen):
            running = False  # Exit the program

    if started:
        # Draw pulley (rotated)
        pygame.draw.circle(screen, (83, 56, 71), pulley_center, pulley_radius + border_thickness)
        pygame.draw.circle(screen, (117, 191, 46), pulley_center, pulley_radius)
        pygame.draw.circle(screen, (83, 56, 71), pulley_center, fulcrum_radius)
        pygame.draw.line(screen, (83, 56, 71), pulley_center,
                         (pulley_center[0] + pulley_radius * math.cos(angle), pulley_center[1] + pulley_radius * math.sin(angle)), 2)

        # Draw rope
        pygame.draw.line(screen, (83, 56, 71), (pulley_center[0] + initial_weight_x_offset, pulley_center[1] + initial_weight_y_offset + pulley_radius),
                         (weight_x + weight_width // 2, weight_y), 2)

        # Draw weight
        pygame.draw.rect(screen, (83, 56, 71),
                         (weight_x - weight_second_border_thickness, weight_y - weight_second_border_thickness,
                          weight_width + 2 * weight_second_border_thickness,
                          weight_height + 2 * weight_second_border_thickness))
        pygame.draw.rect(screen, WHITE, (weight_x - weight_border_thickness, weight_y - weight_border_thickness,
                                         weight_width + 2 * weight_border_thickness,
                                         weight_height + 2 * weight_border_thickness))
        pygame.draw.rect(screen, (223, 98, 26), (weight_x, weight_y, weight_width, weight_height))

        # Draw weight text
        weight_text = small_font.render(f'{weight_mass}kg', True, WHITE)
        screen.blit(weight_text, (weight_x + 5, weight_y + weight_height // 4))

        # Update physics
        if frames < drop_duration * fps:
            weight_y += drop_speed
            angle += angle_speed
            frames += 1

    # Update display
    pygame.display.flip()

    clock.tick(fps)

# Quit Pygame
pygame.quit()
sys.exit()
