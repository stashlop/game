import pygame
import random

# Initialize the game
pygame.init()

# Set up display (Start in full screen mode)
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h
full_screen = True
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("911")

# Set up game clock
clock = pygame.time.Clock()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)  # Light blue color to mimic glass
TRANSPARENCY = 150            # Transparency level for the glass effect

# Load bird image and scale it based on screen size
bird_img = pygame.image.load("bird.png")
bird_size = int(SCREEN_HEIGHT * 0.07)  # Scale bird to 7% of screen height
bird_img = pygame.transform.scale(bird_img, (bird_size, bird_size))

# Bird settings
bird_x = SCREEN_WIDTH * 0.1  # Bird starts at 10% of screen width
bird_y = SCREEN_HEIGHT * 0.5
bird_y_velocity = 0
GRAVITY = 1
JUMP_STRENGTH = 10

# Pipe settings
pipe_width = int(SCREEN_WIDTH * 0.12)  # Pipes will be 12% of screen width for better spacing
pipe_gap = int(SCREEN_HEIGHT * 0.25)   # Gap between pipes is 25% of screen height
pipe_velocity = 5
pipe_x = SCREEN_WIDTH
pipe_height = random.randint(int(SCREEN_HEIGHT * 0.2), int(SCREEN_HEIGHT * 0.6))

# Score
score = 0
font = pygame.font.SysFont(None, 48)  # Larger font size for bigger screen

# Game state variables
running = True
game_over = False
game_started = False

def reset_game():
    """Resets the game state to start again."""
    global bird_y, bird_y_velocity, pipe_x, pipe_height, pipe_velocity, score, game_over
    bird_y = SCREEN_HEIGHT * 0.5
    bird_y_velocity = 0
    pipe_x = SCREEN_WIDTH
    pipe_height = random.randint(int(SCREEN_HEIGHT * 0.2), int(SCREEN_HEIGHT * 0.6))
    pipe_velocity = 5
    score = 0
    game_over = False

def draw_bird():
    screen.blit(bird_img, (bird_x, bird_y))

def draw_pipe(pipe_x, pipe_height):
    # Draw upper pipe (scaled to screen size)
    upper_pipe_rect = pygame.Surface((pipe_width, SCREEN_HEIGHT))
    upper_pipe_rect.set_alpha(TRANSPARENCY)  # Set transparency
    upper_pipe_rect.fill(LIGHT_BLUE)  # Fill with light blue color
    screen.blit(upper_pipe_rect, (pipe_x, pipe_height - SCREEN_HEIGHT))

    # Draw lower pipe (scaled to screen size)
    lower_pipe_rect = pygame.Surface((pipe_width, SCREEN_HEIGHT))
    lower_pipe_rect.set_alpha(TRANSPARENCY)  # Set transparency
    lower_pipe_rect.fill(LIGHT_BLUE)  # Fill with light blue color
    screen.blit(lower_pipe_rect, (pipe_x, pipe_height + pipe_gap))

def check_collision(pipe_x, pipe_height, bird_y):
    if bird_y > SCREEN_HEIGHT - bird_size or bird_y < 0:
        return True
    if bird_x + bird_size > pipe_x and bird_x < pipe_x + pipe_width:
        if bird_y < pipe_height or bird_y + bird_size > pipe_height + pipe_gap:
            return True
    return False

def show_start_screen():
    """Displays the start screen with instructions to start the game."""
    screen.fill(BLACK)
    title_text = font.render("Flappy Bird", True, WHITE)
    instruction_text = font.render("Press 'S' to Start", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
    screen.blit(instruction_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
    pygame.display.update()

def toggle_fullscreen():
    """Toggles between fullscreen and windowed mode."""
    global full_screen, screen, SCREEN_WIDTH, SCREEN_HEIGHT
    if full_screen:
        screen = pygame.display.set_mode((800, 600))  # Windowed mode (800x600 resolution)
        SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
        full_screen = False
    else:
        screen_info = pygame.display.Info()
        SCREEN_WIDTH = screen_info.current_w
        SCREEN_HEIGHT = screen_info.current_h
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        full_screen = True

while running:
    if not game_started:
        show_start_screen()
        
        # Wait for the player to start the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:  # Press 'S' to start
                    game_started = True
                    reset_game()
                if event.key == pygame.K_F11:  # Press F11 to toggle full screen
                    toggle_fullscreen()
    else:
        screen.fill(BLACK)  # Fill background with black color
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_SPACE:
                        bird_y_velocity = -JUMP_STRENGTH
                elif game_over:
                    if event.key == pygame.K_r:  # Press 'R' to restart after game over
                        reset_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:  # Press F11 to toggle full screen during the game
                    toggle_fullscreen()

        if not game_over:
            # Update bird's position
            bird_y_velocity += GRAVITY
            bird_y += bird_y_velocity

            # Update pipe position
            pipe_x -= pipe_velocity
            if pipe_x < -pipe_width:
                pipe_x = SCREEN_WIDTH
                pipe_height = random.randint(int(SCREEN_HEIGHT * 0.2), int(SCREEN_HEIGHT * 0.6))
                score += 1

            # Draw bird and pipes
            draw_bird()
            draw_pipe(pipe_x, pipe_height)

            # Check for collisions
            if check_collision(pipe_x, pipe_height, bird_y):
                game_over = True
                bird_y_velocity = 0
                pipe_velocity = 0

        # Display score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if game_over:
            game_over_text = font.render("BIG BOOM BOOM! Press 'R' to restart", True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 20))

        pygame.display.update()
        clock.tick(30)

pygame.quit()
