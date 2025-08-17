import pygame
import random

# Initialize the game
pygame.init()

# Play background music in a loop
pygame.mixer.music.load("bg.mp3")
pygame.mixer.music.play(-1)  # -1 means loop forever

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
LIGHT_BLUE = (173, 216, 230)
TRANSPARENCY = 150

# Load and scale sky background image
background_img = pygame.image.load("sky.jpg").convert()
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load building image (keep only for obstacles)
building_img = pygame.image.load("building.png").convert_alpha()

# Load bird image and set bird size
bird_img = pygame.image.load("bird.png").convert_alpha()
bird_size = int(SCREEN_HEIGHT * 0.08)
bird_img = pygame.transform.scale(bird_img, (bird_size, bird_size))

# Load point sound
point_sound = pygame.mixer.Sound("point.mp3")

# Bird settings
bird_x = SCREEN_WIDTH * 0.1
bird_y = SCREEN_HEIGHT * 0.5
bird_y_velocity = 0
GRAVITY = 1
JUMP_STRENGTH = 10

# Pipe settings
pipe_width = int(SCREEN_WIDTH * 0.12)
pipe_gap = int(SCREEN_HEIGHT * 0.25)
pipe_velocity = 5
pipe_x = SCREEN_WIDTH
pipe_height = random.randint(int(SCREEN_HEIGHT * 0.2), int(SCREEN_HEIGHT * 0.6))

# Score
score = 0
font = pygame.font.SysFont(None, 64)

# Game state variables
running = True
game_over = False
game_started = False

# Add pause state variable
paused = False

# Building settings for both top and bottom
building_gap = int(SCREEN_HEIGHT * 0.25)
building_width = pipe_width
building_velocity = pipe_velocity
building_x = SCREEN_WIDTH
building_height_bottom = random.randint(int(SCREEN_HEIGHT * 0.2), int(SCREEN_HEIGHT * 0.6))
building_height_top = SCREEN_HEIGHT - building_height_bottom - building_gap


# -------- Button Class --------
class Button:
    def __init__(self, text, x, y, width, height, font, bg_color, text_color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.hover_color = hover_color

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.bg_color
        pygame.draw.rect(screen, color, self.rect, border_radius=12)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            if self.rect.collidepoint(event.pos):
                return True
        return False


# -------- Game Functions --------
def reset_game():
    global bird_y, bird_y_velocity, building_x, building_height_bottom, building_height_top, building_velocity, score, game_over
    bird_y = SCREEN_HEIGHT * 0.5
    bird_y_velocity = 0
    building_x = SCREEN_WIDTH
    building_height_bottom = random.randint(int(SCREEN_HEIGHT * 0.2), int(SCREEN_HEIGHT * 0.6))
    building_height_top = SCREEN_HEIGHT - building_height_bottom - building_gap
    building_velocity = 5
    score = 0
    game_over = False


def draw_bird():
    screen.blit(bird_img, (bird_x, bird_y))

def get_bird_rect():
    return pygame.Rect(bird_x, bird_y, bird_size, bird_size)

def draw_building_pair(x, height_top, height_bottom):
    # Top building (inverted)
    scaled_top = pygame.transform.scale(building_img, (building_width, height_top))
    flipped_top = pygame.transform.flip(scaled_top, False, True)
    screen.blit(flipped_top, (x, 0))
    # Bottom building
    scaled_bottom = pygame.transform.scale(building_img, (building_width, height_bottom))
    screen.blit(scaled_bottom, (x, SCREEN_HEIGHT - height_bottom))

def get_building_rects(x, height_top, height_bottom):
    top_rect = pygame.Rect(x, 0, building_width, height_top)
    bottom_rect = pygame.Rect(x, SCREEN_HEIGHT - height_bottom, building_width, height_bottom)
    return top_rect, bottom_rect

def check_collision(x, height_top, height_bottom, bird_y):
    bird_rect = get_bird_rect()
    top_rect, bottom_rect = get_building_rects(x, height_top, height_bottom)
    # Collision with ground or ceiling
    if bird_y > SCREEN_HEIGHT - bird_size or bird_y < 0:
        return True
    # Collision with buildings
    if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
        return True
    return False


def show_start_screen():
    screen.fill(BLACK)
    title_text = font.render("Flappy Bird", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 4))

    # Create buttons
    start_button = Button("Start", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 60,
                          font, LIGHT_BLUE, BLACK, (100, 149, 237))
    quit_button = Button("Quit", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 80, 200, 60,
                         font, LIGHT_BLUE, BLACK, (100, 149, 237))

    start_button.draw(screen)
    quit_button.draw(screen)

    pygame.display.update()
    return start_button, quit_button


def toggle_fullscreen():
    global full_screen, screen, SCREEN_WIDTH, SCREEN_HEIGHT
    if full_screen:
        screen = pygame.display.set_mode((800, 600))
        SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
        full_screen = False
    else:
        screen_info = pygame.display.Info()
        SCREEN_WIDTH = screen_info.current_w
        SCREEN_HEIGHT = screen_info.current_h
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        full_screen = True


def show_pause_message():
    pause_text = font.render("Paused", True, WHITE)
    screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2,
                             SCREEN_HEIGHT // 2 - pause_text.get_height() // 2))


# -------- Main Loop --------
while running:
    if not game_started:
        screen.blit(background_img, (0, 0))  # Draw sky background on start screen
        start_button, quit_button = show_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                toggle_fullscreen()
            elif start_button.is_clicked(event):
                game_started = True
                reset_game()
            elif quit_button.is_clicked(event):
                running = False
    else:
        screen.blit(background_img, (0, 0))  # Draw sky background during gameplay

        # Create Exit button
        exit_button = Button("Exit", SCREEN_WIDTH - 140, 20, 120, 50,
                             font, LIGHT_BLUE, BLACK, (100, 149, 237))
        exit_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird_y_velocity = -JUMP_STRENGTH
                elif event.key == pygame.K_r and game_over:
                    reset_game()
                elif event.key == pygame.K_F11:
                    toggle_fullscreen()
            elif exit_button.is_clicked(event):
                running = False

        if not game_over:
            bird_y_velocity += GRAVITY
            bird_y += bird_y_velocity

            building_x -= building_velocity
            if building_x < -building_width:
                building_x = SCREEN_WIDTH
                building_height_bottom = random.randint(int(SCREEN_HEIGHT * 0.2), int(SCREEN_HEIGHT * 0.6))
                building_height_top = SCREEN_HEIGHT - building_height_bottom - building_gap
                score += 1

                # Play point sound
                point_sound.play()

                # Increase speed every 5 points
                if score % 5 == 0:
                    building_velocity += 1

            draw_bird()
            draw_building_pair(building_x, building_height_top, building_height_bottom)

            if check_collision(building_x, building_height_top, building_height_bottom, bird_y):
                game_over = True
                bird_y_velocity = 0
                building_velocity = 0

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (20, 20))

        if game_over:
            game_over_text = font.render("BIG BOOM BOOM! Press 'R' to restart", True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                                         SCREEN_HEIGHT // 2 - 20))

        pygame.display.update()
        clock.tick(60)

pygame.quit()
