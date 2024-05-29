import pygame
import pygame_gui
import sys
import math
import button
import time

# Initialize Pygame 
pygame.init()

# Initialize Sounds 
success_sound = pygame.mixer.Sound("success_sound.wav")

# Flag to track if success sound has been played
success_sound_played = False

# Play background music (Only plays it in main menu)
pygame.mixer.music.load("bg_music.wav")
pygame.mixer.music.play(-1)  # -1 plays the music in an infinite loop

# Screen dimensions 
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rotational Dynamics Simulation - Falling Mass")

# Load background stuff
background_img = pygame.image.load("bg.png").convert()
foreground_img = pygame.image.load("upforeground.png").convert_alpha()
background_img_width = background_img.get_width()

# Scale the foreground image to fit the screen
foreground_img = pygame.transform.scale(foreground_img, (width * 1.3, height * 1.3))

# Initialize Pygame_GUI with a custom theme 
theme = "text_box.json"
MANAGER = pygame_gui.UIManager((width, height), theme)
MANAGER.get_theme().load_theme(theme)

# Buttons 
start_img = pygame.image.load("start_btn.png").convert_alpha()
exit_img = pygame.image.load("exit_btn.png").convert_alpha()
play_img = pygame.image.load("play_btn.png").convert_alpha()
clear_img = pygame.image.load("clear_btn.png").convert_alpha()
title_img = pygame.image.load("menu_title.png").convert_alpha()
input_img = pygame.image.load("input_table.png").convert_alpha()

# Center the buttons and title 
start_button_x = (width // 2) - (start_img.get_width() * 0.35 / 2)
exit_button_x = (width // 2) - (exit_img.get_width() * 0.35 / 2)
menu_title_x = (width // 2) - (title_img.get_width() * 0.7 / 2)

# Button instances 
start_button = button.Button(start_button_x, 240, start_img, 0.35)
exit_button = button.Button(exit_button_x, 298, exit_img, 0.35)
play_button = button.Button(114, 269, play_img, 0.30)
clear_button = button.Button(64, 269, clear_img, 0.30)
menu_title = button.Button(menu_title_x, 53, title_img, 0.7)
input_table = button.Button(20, 22, input_img, 0.6)

# Text input 
PMassInput = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((43, 65), (98, 22)),
    manager=MANAGER,
    object_id="#PullyMass",
)
PRadiusInput = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((43, 113), (98, 22)),
    manager=MANAGER,
    object_id="#PullyRadius",
)
WMass1Input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((43, 161), (98, 22)),
    manager=MANAGER,
    object_id="#WeighMass",
)
WMass2Input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((43, 250), (98, 22)),
    manager=MANAGER,
    object_id="#WeighMass",
)
DurationInput = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((43, 210), (98, 22)),
    manager=MANAGER,
    object_id="#DropDuration",
)

# Initialize text with default values 
PMassInput.set_text("20.0")  # kg
PRadiusInput.set_text("2.0")  # m
WMass1Input.set_text("10.0")  # kg
WMass2Input.set_text("5.0")  # kg
DurationInput.set_text("8.0")  # s

# Colors 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (128, 0, 128)
GRAY = (169, 169, 169)
RED = (255, 0, 0)
SKY_BLUE = (84, 192, 201) 

# Time parameters 
time_left = 8.0  # s (default)

# Pulley parameters 
pulley_mass = 20  # kg
pulley_radius = 2 * 20  # pixels, smaller size (1m per 20 pixels)
pulley_center = ((width // 2) + 10, 100)  # Centered horizontally
border_thickness = 2  # Thickness of the border
fulcrum_radius = 3  # Radius of the fulcrum

# Weight parameters 
base_weight1_mass = 10  # Base weight mass for scaling
base_weight1_size = 40  # Base size for the weight
base_font1_size = 18  # Base font size for the weight text
weight1_mass = 10.0  # kg
weight1_width = weight1_height = base_weight1_size  # Initial size of the weight
weight1_border_thickness = 1  # Thickness of the border for the weight box
weight1_second_border_thickness = 4

base_weight2_mass = 5  # Base weight mass for scaling
base_weight2_size = 20  # Base size for the weight
base_font2_size = 9  # Base font size for the weight text
weight2_mass = 5.0  # kg
weight2_width = weight2_height = base_weight2_size  # Initial size of the weight
weight2_border_thickness = 1  # Thickness of the border for the weight box
weight2_second_border_thickness = 4

# Simulation parameters 
drop_duration = 8  # seconds 
fps = 60  # frames per second 

# Weight position 
weight1_x = (pulley_center[0] + pulley_radius - weight1_width // 2)  # Centered below the pulley
weight1_y = pulley_center[1] + pulley_radius + 100  # Starting position below the pulley
weight2_x = (pulley_center[0] - pulley_radius - weight2_width // 2)  # Centered below the pulley
weight2_y = pulley_center[1] + pulley_radius + 100 # Starting position below the pulley
weight_scaley = 47

# Pulley rotation 
angle = 0
angle_speed = (2 * math.pi) / (drop_duration * fps)

# Font for the text 
font_size = 24
font = pygame.font.SysFont(None, font_size)
font2 = pygame.font.SysFont(None, 35)
small_font = pygame.font.SysFont(None, 18)
smaller_font = pygame.font.SysFont(None, 9)
warning_font = pygame.font.SysFont(None, 20)

# Main loop 
running = True
started = False  # Simulation started flag
playing = False
clock = pygame.time.Clock()
frames = 0
angular_acceleration = 0
angular_velocity = 0
warning_text = ""
MAX_FLAG_WEIGHT = 0  # Flag to discern if the user's input has reached the max, so to know if the visual representation logic will be different (for weight_mass)

# Gravity 
g = 9.81  # m/s^2

# Distance initialized to zero 
distance = 0

# Define maximum allowable values 
MAX_PULLEY_RADIUS = 10  # meters
MAX_WEIGHT_MASS = 50  # kg

def reset_simulation():
    global drop_duration, pulley_mass, pulley_radius, weight1_x, weight1_y, weight2_x, weight2_y, weight1_width, weight1_height, weight2_width, weight2_height, weight1_scale, weight2_scale, weight1_mass, weight2_mass, angle_speed, frames, small_font, smaller_font, angular_acceleration, distance, final_velocity
    global success_sound_played, warning_display_time

    # Reset success sound played
    success_sound_played = False
    # Reset warning text 
    warning_text = ""

    # Read values from stored_text and convert them to floats 
    pulley_mass = float(PMassInput.get_text())
    pulley_radius = float(PRadiusInput.get_text())  # Input in terms of meters 
    weight1_mass = float(WMass1Input.get_text())
    weight2_mass = float(WMass2Input.get_text())
    drop_duration = float(DurationInput.get_text())

    # Check for maximum values and set warnings 
    if pulley_radius > MAX_PULLEY_RADIUS:
        pulley_radius = MAX_PULLEY_RADIUS
        warning_display_time = time.time()  # Update the warning display time
        warning_text = warning_font.render(f"Pulley radius exceeds maximum value. Set to maximum 10 m.", True, RED)
        screen.blit(warning_text, (220, height // 2))
        pygame.display.flip()  # Update the display
        time.sleep(3)  # Pause the simulation for 3 seconds
        # Update the text in the input line
        PRadiusInput.set_text(str(MAX_PULLEY_RADIUS))  # Set the input line text to the maximum allowable value 

    if weight1_mass > MAX_WEIGHT_MASS:
        MAX_FLAG_WEIGHT1 = 1
        warning_display_time = time.time()  # Update the warning display time
        warning_text = warning_font.render(f"Weight mass exceeds maximum value. Visual representation adjusted to 50 kg.",True,RED,)
        screen.blit(warning_text, (155, (height // 2) + 20))
        pygame.display.flip()  # Update the display
        time.sleep(3)  # Pause the simulation for 3 seconds
    else:
        MAX_FLAG_WEIGHT1 = 0

    if weight2_mass > MAX_WEIGHT_MASS:
        MAX_FLAG_WEIGHT2 = 1
        warning_display_time = time.time()  # Update the warning display time
        warning_text = warning_font.render(f"Weight mass exceeds maximum value. Visual representation adjusted to 50 kg.",True,RED,)
        screen.blit(warning_text, (155, (height // 2) + 20))
        pygame.display.flip()  # Update the display
        time.sleep(3)  # Pause the simulation for 3 seconds
    else:
        MAX_FLAG_WEIGHT2 = 0

    pulley_radius *= 20  # Convert to pixels (1 meter = 20 pixels) 

    # Recalculate weight size based on weight mass 
    if MAX_FLAG_WEIGHT1 != 1:
        weight1_scale = weight1_mass / base_weight1_mass
        weight1_width = weight1_height = int(base_weight1_size * weight1_scale)
    else:
        weight1_scale = MAX_WEIGHT_MASS / base_weight1_mass
        weight1_width = weight1_height = int(base_weight1_size * weight1_scale)
    if MAX_FLAG_WEIGHT2 != 1:
        weight2_scale = weight2_mass / base_weight2_mass
        weight2_width = weight2_height = int(base_weight2_size * weight2_scale)
    else:
        weight2_scale = MAX_WEIGHT_MASS / base_weight2_mass
        weight2_width = weight2_height = int(base_weight2_size * weight2_scale)

    # Recalculate font size based on weight mass 
    font1_size = int(base_font1_size * weight1_scale)
    small_font = pygame.font.SysFont(None, font1_size)

    weight1_x = pulley_center[0] + pulley_radius - weight1_width // 2
    weight1_y = pulley_center[1] + pulley_radius + 100
    angle_speed = (2 * math.pi) / (drop_duration * fps)
    frames = 0

    font2_size = int(base_font2_size * weight2_scale)
    smaller_font = pygame.font.SysFont(None, font2_size)

    weight2_x = pulley_center[0] - pulley_radius - weight2_width // 2
    weight2_y = pulley_center[1] + pulley_radius + 100
    angle_speed = (2 * math.pi) / (drop_duration * fps)
    frames = 0

    # Calculate angular acceleration, as well as the final velocity and distance after 'x' amount of seconds 
    moment_of_inertia = (0.5) * pulley_mass * ((pulley_radius / 20) ** 2)  # I = 1/2mr^2
    angular_acceleration1 = ((weight1_mass) * (g) * (pulley_radius / 20)) / (moment_of_inertia + weight1_mass * ((pulley_radius / 20) ** 2))  # α = [mgR]/[I + mgR^2]
    angular_acceleration2 = ((weight2_mass) * (g) * (pulley_radius / 20)) / (moment_of_inertia + weight2_mass * ((pulley_radius / 20) ** 2))  # α = [mgR]/[I + mgR^2]
    angular_acceleration = angular_acceleration1-angular_acceleration2
    final_velocity = (angular_acceleration * (pulley_radius / 20) * drop_duration * (-1))  # Vf = Vo + at where Vo is 0, a is α * R, and t is inputted drop duration (-)
    distance = (final_velocity**2) / (2 * (angular_acceleration * (pulley_radius / 20)))  # Vf^2 = Vo^2 + 2ad

    return angular_acceleration

# Define Game Variables
scroll = 0
tiles = math.ceil(width / background_img_width) + 1

while running:
    UiRefreshrate = clock.tick(fps) / 1000

    # Clear the screen
    screen.fill((0, 0, 0))


    # Draw Scrolling Background
    for i in range(0, tiles):
        screen.blit(background_img, (i * background_img_width + scroll, 0))

    # Scroll background
    scroll -= 5

    # Reset scroll
    if abs(scroll) > background_img_width:
        scroll = 0

    # Blit foreground image
    screen.blit(foreground_img, (-120, -100))

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
            success_sound_played = False
            print("PLAY")

            reset_simulation()  # Reset simulation with updated parameters
            angular_velocity = 0
            playing = True

        if clear_button.draw(screen):
            print("CLEAR")
            # Reset text input fields
            PMassInput.set_text("")
            PRadiusInput.set_text("")
            WMass1Input.set_text("")
            WMass2Input.set_text("")
            DurationInput.set_text("")
            # Reset y position of the weight
            weight1_y = pulley_center[1] + pulley_radius + 100
            weight2_y = pulley_center[1] + pulley_radius + 100
            playing = False
            success_sound_played = True 

        # Draw pulley (rotated)
        pygame.draw.circle(screen, (83, 56, 71), pulley_center, pulley_radius + border_thickness)
        pygame.draw.circle(screen, (117, 191, 46), pulley_center, pulley_radius)
        pygame.draw.circle(screen, (83, 56, 71), pulley_center, fulcrum_radius)
        pygame.draw.line(screen,(83, 56, 71),pulley_center,(pulley_center[0] + pulley_radius * math.cos(angle),pulley_center[1] + pulley_radius * math.sin(angle),),2,)

        # Draw rope
        pygame.draw.line(screen,(83, 56, 71),(pulley_center[0] + pulley_radius,pulley_center[1],),  # Made it adjust dynamically to the position of the pulley
            (weight1_x + weight1_width // 2, weight1_y), 2)

        pygame.draw.line(screen,(83, 56, 71),(pulley_center[0] - pulley_radius-2,pulley_center[1],),  # Made it adjust dynamically to the position of the pulley
            ((weight2_x + weight2_width // 2)-2, weight2_y), 2)

        # Draw weight
        pygame.draw.rect(screen,(83, 56, 71),
            (
                weight1_x - weight1_second_border_thickness,
                weight1_y - weight1_second_border_thickness,
                weight1_width + 2 * weight1_second_border_thickness,
                weight1_height + 2 * weight1_second_border_thickness,
            ),
        )
        pygame.draw.rect(screen,WHITE,
            (
                weight1_x - weight1_border_thickness,
                weight1_y - weight1_border_thickness,
                weight1_width + 2 * weight1_border_thickness,
                weight1_height + 2 * weight1_border_thickness,
            ),
        )
        pygame.draw.rect(screen, (223, 98, 26), (weight1_x, weight1_y, weight1_width, weight1_height))

        pygame.draw.rect(screen,(83, 56, 71),
            (
                weight2_x - weight2_second_border_thickness - 2,
                weight2_y - weight2_second_border_thickness,
                weight2_width + 2 * weight2_second_border_thickness,
                weight2_height + 2 * weight2_second_border_thickness,
            ),
        )
        pygame.draw.rect(screen,WHITE,
            (
                weight2_x - weight2_border_thickness - 2,
                weight2_y - weight2_border_thickness,
                weight2_width + 2 * weight2_border_thickness,
                weight2_height + 2 * weight2_border_thickness,
            ),
        )
        pygame.draw.rect(screen, (223, 98, 26), (weight2_x-2, weight2_y, weight2_width, weight2_height))

        # Draw weight text
        weight_text = small_font.render(f"{weight1_mass}kg", True, WHITE)
        text_rect = weight_text.get_rect(center=(weight1_x + weight1_width // 2, weight1_y + weight1_height // 2))
        screen.blit(weight_text, text_rect)
        weight_text = smaller_font.render(f"{weight2_mass}kg", True, WHITE)
        text_rect = weight_text.get_rect(center=(weight2_x + weight2_width // 2, weight2_y + weight2_height // 2))
        screen.blit(weight_text, text_rect)

        # Update physics (now based on calculated angular acceleration)
        if frames < drop_duration * fps and playing:
            angular_velocity += angular_acceleration / fps
            angle += angular_velocity / fps
            linear_velocity = angular_velocity * pulley_radius
            weight1_y += linear_velocity / fps
            weight2_y += (linear_velocity / fps)*-1
            weight_scaley += linear_velocity / fps
            frames += 1
            time_left = drop_duration - frames / fps
        elif playing:
            time_left = 0

        # Display timer
        timer_text = font2.render(f"Time: {time_left:.2f}s", True, BLACK)
        screen.blit(timer_text, (20, height - 150))

        # Display velocity and angular acceleration after the simulation duration
        if time_left <= 0 or weight1_y <= pulley_center[1] or weight2_y <= pulley_center[1]:

            angular_acceleration_text = font.render(f"Angular Acceleration: {angular_acceleration:.2f} rad/s²", True, BLACK)
            angular_acceleration_text_x = 20  # Adjusted position
            angular_acceleration_text_y = 350
            screen.blit(angular_acceleration_text,(angular_acceleration_text_x, angular_acceleration_text_y))

            final_velocity_text = font.render(f"Final Velocity: {final_velocity:.2f} m/s", True, BLACK)
            screen.blit(final_velocity_text, (20, 370))

            distance_text = font.render(f"Distance: {distance:.2f} m", True, BLACK)
            screen.blit(distance_text, (20, 390))
            
            distance_text = font.render(f"Time Taken: {(drop_duration-time_left):.2f} s", True, BLACK)
            screen.blit(distance_text, (20, 410))

            playing = False


            # Play success sound only once
            if not success_sound_played:
                pygame.mixer.Sound.play(success_sound)
                success_sound_played = True

        # Draw input fields/UI elements
        MANAGER.draw_ui(screen)

    # Update display
    pygame.display.flip()
    clock.tick(fps)
    MANAGER.update(UiRefreshrate)

# Quit Pygame
pygame.quit()
sys.exit()