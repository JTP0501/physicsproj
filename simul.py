import pygame
import pygame_gui
import sys
import math
import button

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rotational Dynamics Simulation - Falling Mass")

# Initialize Pygame_GUI
MANAGER = pygame_gui.UIManager((width, height))

# Buttons
start_img = pygame.image.load('start_btn.png').convert_alpha()
exit_img = pygame.image.load('exit_btn.png').convert_alpha()
play_img = pygame.image.load('play_btn.png').convert_alpha()
clear_img = pygame.image.load('clear_btn.png').convert_alpha()
title_img = pygame.image.load('menu_title.png').convert_alpha()
input_img = pygame.image.load('input_table.png').convert_alpha()

# Button instances
start_button = button.Button(251, 240, start_img, 0.35)
exit_button = button.Button(258, 298, exit_img, 0.35)
play_button = button.Button(114, 255, play_img, 0.30)
clear_button = button.Button(64, 255, clear_img, 0.30)
menu_title = button.Button(95, 53, title_img, 0.7)
input_table = button.Button(20, 22, input_img, 0.6)

# Text input
PMassInput = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((45, 65), (125, 20)), manager=MANAGER, object_id="#PullyMass")
PRadiusInput = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((45, 107), (125, 20)), manager=MANAGER, object_id="#PullyRadius")
WMassInput = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((45, 155), (125, 20)), manager=MANAGER, object_id="#WeighMass")
DurationInput = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((45, 200), (125, 20)), manager=MANAGER, object_id="#DropDuration")

# Initialize text with default values
PMassInput.set_text("20") # kg
PRadiusInput.set_text("2") # m
WMassInput.set_text("10") # kg
DurationInput.set_text("8") # s

def draw_text(text, font, text_col, x, y, line_spacing=29):
    for i, line in enumerate(text):
        img = font.render(line, True, text_col)
        width1 = img.get_width()
        screen.blit(img, (x - (width1 / 2), y + i * (font.get_height() + line_spacing)))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (128, 0, 128)
GRAY = (169, 169, 169)

# Pulley parameters
pulley_mass = 20  # kg
pulley_radius = 2 * 20  # pixels, smaller size (1m per 20 pixels)
pulley_center = (300, 100)
border_thickness = 2  # Thickness of the border
fulcrum_radius = 3  # Radius of the fulcrum

# Weight parameters
base_weight_mass = 10  # Base weight mass for scaling
base_weight_size = 40  # Base size for the weight
base_font_size = 18  # Base font size for the weight text
weight_mass = 10  # kg
weight_width = weight_height = base_weight_size  # Initial size of the weight
weight_border_thickness = 1  # Thickness of the border for the weight box
weight_second_border_thickness = 4

# Simulation parameters
drop_duration = 8  # seconds
fps = 60  # frames per second
drop_speed = (height - pulley_center[1] - weight_height - pulley_radius) / (drop_duration * fps)  # pixels per frame

# Weight position
weight_x = pulley_center[0] + pulley_radius - weight_width // 2  # Centered below the pulley
weight_y = pulley_center[1] + pulley_radius  # Starting position below the pulley

# Pulley rotation
angle = 0
angle_speed = (2 * math.pi) / (drop_duration * fps)

# Font for the text
font_size = 24
font = pygame.font.SysFont(None, font_size)
font2 = pygame.font.SysFont(None, 35)
small_font = pygame.font.SysFont(None, 18)

# Main loop
running = True
started = False  # Simulation started flag
clock = pygame.time.Clock()
frames = 0
angular_acceleration = 0
angular_velocity = 0

# Gravity
g = 9.81 # m/s^2

def reset_simulation():
    global drop_duration, pulley_mass, weight_mass, pulley_radius, drop_speed, weight_x, weight_y, angle_speed, frames, weight_width, weight_height, small_font, angular_acceleration
    # Read values from stored_text and convert them to integers
    pulley_mass = float(PMassInput.get_text())
    pulley_radius = 20 * float(PRadiusInput.get_text()) # Input in terms of meters, multiplies by 20 pixels
    weight_mass = float(WMassInput.get_text())
    drop_duration = float(DurationInput.get_text())

    # Recalculate weight size based on weight mass
    weight_scale = weight_mass / base_weight_mass
    weight_width = weight_height = int(base_weight_size * weight_scale)

    # Recalculate font size based on weight mass
    font_size = int(base_font_size * weight_scale)
    small_font = pygame.font.SysFont(None, font_size)

    drop_speed = (height - pulley_center[1] - weight_height - pulley_radius) / (drop_duration * fps)
    weight_x = pulley_center[0] + pulley_radius - weight_width // 2
    weight_y = pulley_center[1] + pulley_radius
    angle_speed = (2 * math.pi) / (drop_duration * fps)
    frames = 0

    # Calculate angular acceleration 

    moment_of_inertia = (0.5) * pulley_mass * ((pulley_radius / 20) ** 2) # I = 1/2mr^2
    angular_acceleration = ((weight_mass) * (g) * (pulley_radius / 20)) / (moment_of_inertia + weight_mass * ((pulley_radius / 20) ** 2)) # α = [mgR]/[I + mgR^2]

    return angular_acceleration

while running:
    UiRefreshrate = clock.tick(60)/1000

    # Clear screen
    screen.fill((202, 228, 241))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        
        MANAGER.process_events(event)

    if not started:
        # Draw buttons and title
        menu_title.draw(screen)
        if start_button.draw(screen):
            started = True  # Start the simulation

        if exit_button.draw(screen):
            running = False  # Exit the program

    if started:
        input_table.draw(screen)

        if play_button.draw(screen):
            print("PLAY")
            reset_simulation()  # Reset simulation with updated parameters

        if clear_button.draw(screen):
            print("CLEAR")
            # Reset text input fields
            PMassInput.set_text("")     
            PRadiusInput.set_text("")
            WMassInput.set_text("")
            DurationInput.set_text("")
            # Reset y position of the weight
            weight_y = pulley_center[1] + pulley_radius

        # Draw pulley (rotated)
        pygame.draw.circle(screen, (83, 56, 71), pulley_center, pulley_radius + border_thickness)
        pygame.draw.circle(screen, (117, 191, 46), pulley_center, pulley_radius)
        pygame.draw.circle(screen, (83, 56, 71), pulley_center, fulcrum_radius)
        pygame.draw.line(screen, (83, 56, 71), pulley_center,
                         (pulley_center[0] + pulley_radius * math.cos(angle),
                          pulley_center[1] + pulley_radius * math.sin(angle)), 2)

        # Draw rope
        pygame.draw.line(screen, (83, 56, 71), (
        pulley_center[0] + pulley_radius, pulley_center[1]),    # Made it adjust dynamically to the position of the pulley
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
        text_rect = weight_text.get_rect(center=(weight_x + weight_width // 2, weight_y + weight_height // 2))
        screen.blit(weight_text, text_rect)

        # Update physics (now based on calculated angular acceleration)
        if frames < drop_duration * fps:
            angular_velocity += angular_acceleration / fps

            angle += angular_velocity / fps

            linear_velocity = angular_velocity * pulley_radius

            weight_y += linear_velocity / fps
            
            frames += 1
            time_left = drop_duration - frames / fps
        else :
            time_left = 0

        # Display angular acceleration (to be improved)
        angular_acceleration_text = font.render(f'Angular Acceleration: {angular_acceleration:.2f} rad/s²', True, BLACK)
        angular_acceleration_text_x = 300 # Adjusted position
        angular_acceleration_text_y = 20
        screen.blit(angular_acceleration_text, (angular_acceleration_text_x, angular_acceleration_text_y))
        
        # Display timer
        timer_text = font2.render(f'Time: {time_left:.2f}s', True, BLACK)
        screen.blit(timer_text, (width - 150, height - 50))

        # Draw input fields/UI elements
        MANAGER.draw_ui(screen)
        
    # Update display
    pygame.display.flip()
    clock.tick(fps)
    MANAGER.update(UiRefreshrate)

# Quit Pygame
pygame.quit()
sys.exit()
