import pygame
import sys
import time

# def run()

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Timeline settings
timeline_width = 600
timeline_height = 10
timeline_x = (SCREEN_WIDTH - timeline_width) // 2
timeline_y = SCREEN_HEIGHT // 2
selector_position = timeline_x  # Starting position of the selector
selector_width = 10
selector_height = 30

# Playback settings
total_duration = 40
is_playing = False
is_dragging = False
edit_timeline = False
start_time = 0  # Initialize start_time
paused_time = 0  # Time when playback was paused

# Main loop
elapsed_time = 0
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Press SPACE to toggle playback
                if not is_playing:
                    is_playing = True
                    start_time = time.time() - paused_time
                else:
                    is_playing = False
                    paused_time = time.time() - start_time
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if timeline_y - 10 <= event.pos[1] <= timeline_y + 20:
                edit_timeline = True
                is_dragging = True
                is_playing = False  # Stop playback if it was playing
                mouse_x, _ = event.pos
                selector_position = max(timeline_x, min(mouse_x, timeline_x + timeline_width - selector_width))
        elif event.type == pygame.MOUSEBUTTONUP:
            if edit_timeline is True:
                edit_timeline = False
                is_dragging = False
                # Update paused_time based on the selector's position when dragging ends
                paused_time = (selector_position - timeline_x) / (timeline_width - selector_width) * total_duration
                elapsed_time = (selector_position - timeline_x) / (timeline_width - selector_width) * total_duration
        elif event.type == pygame.MOUSEMOTION and is_dragging:
            # Update the selector's position while dragging, ensuring it stays within the timeline
            mouse_x, _ = event.pos
            selector_position = max(timeline_x, min(mouse_x, timeline_x + timeline_width - selector_width))

    if is_playing:
        elapsed_time = time.time() - start_time
        if elapsed_time > total_duration:
            elapsed_time = total_duration
            is_playing = False  # Stop playback when duration is reached
        selector_position = timeline_x + (elapsed_time / total_duration) * (timeline_width - selector_width)
    else:
        # When not playing, calculate elapsed_time based on the selector's position
        if elapsed_time < total_duration:
            elapsed_time = paused_time
        else:
            elapsed_time = total_duration

        # Draw
    screen.fill(WHITE)

    # Display elapsed time
    font = pygame.font.SysFont(None, 24)
    img = font.render(f"Elapsed Time: {elapsed_time:.2f}s", True, BLACK)
    screen.blit(img, (20, 20))

    pygame.draw.rect(screen, BLACK, (timeline_x, timeline_y, timeline_width, timeline_height))  # Timeline
    pygame.draw.rect(screen, RED, (selector_position, timeline_y - 10, selector_width, selector_height))  # Selector

    pygame.display.flip()
    clock.tick(60)  # 60 frames per second

pygame.quit()
sys.exit()
