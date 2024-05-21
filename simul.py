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
text = ["20", "40", "10", "2"]
stored_text = []

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
font_size = 24
font = pygame.font.SysFont(None, font_size)
font2 = pygame.font.SysFont(None, 35)
small_font = pygame.font.SysFont(None, 18)

# Main loop
running = True
started = False  # Simulation started flag
clock = pygame.time.Clock()
frames = 0

def reset_simulation():
    global drop_duration, pulley_mass, weight_mass, pulley_radius, drop_speed, weight_x, weight_y, angle_speed, frames
    # Read values from stored_text and convert them to integers
    if len(stored_text) >= 4:
        pulley_mass = int(stored_text[0])
        pulley_radius = int(stored_text[1])
        weight_mass = int(stored_text[2])
        drop_duration = int(stored_text[3])

    drop_speed = (height - pulley_center[1] - weight_height) / (drop_duration * fps)
    weight_x = pulley_center[0] + pulley_radius - weight_width // 2
    weight_y = pulley_center[1] + (2*pulley_radius)
    angle_speed = (2 * math.pi) / (drop_duration * fps)
    frames = 0

while running:
    UiRefereshrate = clock.tick(60)/1000

    # Clear screen
    screen.fill((202, 228, 241))

    for event in pygame.event.get():
        if event.type == pygame.TEXTINPUT:
            text[-1] += event.text

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                text[-1] = text[-1][:-1]
                if len(text[-1]) == 0:
                    if len(text) > 1:
                        text = text[:-1]

            elif event.key == pygame.K_RETURN:
                stored_text.append(text[-1])
                print("Stored text:", stored_text)  # Print the stored text to the console
                text.append("")

        if event.type == pygame.QUIT:
            running = False
        
        MANAGER.process_events(event)

    MANAGER.update(UiRefereshrate)

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
            text = [""]  # Clear the text
            stored_text = [] # Clear stored text so that you can reset multiple times

        draw_text(text, font, (95, 43, 46), 60, 68)

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
        screen.blit(weight_text, (weight_x + 5, weight_y + weight_height // 4))

        # Update physics
        if frames < drop_duration * fps:
            weight_y += drop_speed
            angle += angle_speed
            frames += 1
        
        MANAGER.draw_ui(screen)
        PMassInput = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((45,65), (125, 20)), manager=MANAGER, object_id="#PullyMass")
        PRadiusInput = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((45,107), (125, 20)), manager=MANAGER, object_id="#PullyRadius")
        WMassInput = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((45,155), (125, 20)), manager=MANAGER, object_id="#WeighMass")
        DurationInput = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((45,200), (125, 20)), manager=MANAGER, object_id="#DropDuration")
    # Update display
    pygame.display.flip()
    clock.tick(fps)

# Quit Pygame
pygame.quit()
sys.exit()
