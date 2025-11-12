"""
Blink-Controlled Virtual Drone
Control a drone by blinking - each blink makes it go up!

Requirements:
pip install python-osc pygame

Make sure muse-io is running:
muse-io --device Muse-0FED --osc osc.udp://localhost:12000
"""

import pygame
from pythonosc import dispatcher
from pythonosc import osc_server
import threading
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blink-Controlled Drone")

# Colors
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Drone settings
drone_x = WIDTH // 2
drone_y = HEIGHT // 2
drone_velocity_y = 0
GRAVITY = 0.3
BLINK_BOOST = -15  # Negative because up is negative Y

# Font
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Blink counter
blink_count = 0
last_blink_time = 0

# OSC Handler for blinks
def blink_handler(unused_addr, value):
    global drone_velocity_y, blink_count, last_blink_time
    if value == 1:  # Blink detected
        drone_velocity_y = BLINK_BOOST
        blink_count += 1
        last_blink_time = pygame.time.get_ticks()
        print(f"BLINK! Count: {blink_count}")

# Setup OSC Server
def start_osc_server():
    disp = dispatcher.Dispatcher()
    disp.map("/muse/elements/blink", blink_handler)
    
    server = osc_server.ThreadingOSCUDPServer(
        ("127.0.0.1", 12000), disp)
    print("OSC Server listening on port 12000...")
    print("Waiting for blink signals from Muse...")
    server.serve_forever()

# Start OSC server in separate thread
osc_thread = threading.Thread(target=start_osc_server, daemon=True)
osc_thread.start()

# Game loop
clock = pygame.time.Clock()
running = True

print("\n" + "="*50)
print("BLINK-CONTROLLED DRONE")
print("="*50)
print("Put on your Muse headband")
print("BLINK to make the drone go UP!")
print("Try to keep it in the middle of the screen")
print("="*50 + "\n")

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            # Spacebar for testing (simulates blink)
            if event.key == pygame.K_SPACE:
                drone_velocity_y = BLINK_BOOST
                blink_count += 1
                last_blink_time = pygame.time.get_ticks()
    
    # Update drone physics
    drone_velocity_y += GRAVITY
    drone_y += drone_velocity_y
    
    # Keep drone on screen
    if drone_y < 50:
        drone_y = 50
        drone_velocity_y = 0
    if drone_y > HEIGHT - 50:
        drone_y = HEIGHT - 50
        drone_velocity_y = 0
    
    # Draw everything
    screen.fill(SKY_BLUE)
    
    # Draw ground
    pygame.draw.rect(screen, GREEN, (0, HEIGHT - 30, WIDTH, 30))
    
    # Draw target zone (middle of screen)
    target_top = HEIGHT // 2 - 50
    target_bottom = HEIGHT // 2 + 50
    pygame.draw.rect(screen, (200, 255, 200), 
                     (0, target_top, WIDTH, 100), 3)
    
    # Draw drone (simple representation)
    drone_size = 40
    # Body
    pygame.draw.circle(screen, RED, (int(drone_x), int(drone_y)), drone_size)
    # Propellers
    pygame.draw.line(screen, BLACK, 
                     (drone_x - drone_size, drone_y),
                     (drone_x + drone_size, drone_y), 3)
    pygame.draw.circle(screen, WHITE, (int(drone_x - drone_size), int(drone_y)), 8)
    pygame.draw.circle(screen, WHITE, (int(drone_x + drone_size), int(drone_y)), 8)
    
    # Display blink count
    blink_text = font.render(f"Blinks: {blink_count}", True, BLACK)
    screen.blit(blink_text, (10, 10))
    
    # Display instructions
    instruction_text = small_font.render("BLINK to go UP! (or press SPACE to test)", True, BLACK)
    screen.blit(instruction_text, (WIDTH // 2 - 200, 10))
    
    # Display altitude
    altitude = int(HEIGHT - drone_y)
    alt_text = small_font.render(f"Altitude: {altitude}", True, BLACK)
    screen.blit(alt_text, (10, 50))
    
    # Blink indicator (flash green briefly after blink)
    current_time = pygame.time.get_ticks()
    if current_time - last_blink_time < 200:  # Flash for 200ms
        pygame.draw.circle(screen, GREEN, (WIDTH - 50, 50), 30)
        blink_indicator = small_font.render("BLINK!", True, WHITE)
        screen.blit(blink_indicator, (WIDTH - 80, 90))
    
    # Update display
    pygame.display.flip()
    clock.tick(60)  # 60 FPS

pygame.quit()
sys.exit()
