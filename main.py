import pygame
import random
import os

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Recycle Game")

# Clock
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 36)

# Load background images

backgrounds = [
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "first_level.jpg")), (SCREEN_WIDTH, SCREEN_HEIGHT)),  # Level 1
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "second_level.jpg")), (SCREEN_WIDTH, SCREEN_HEIGHT)),  # Level 2
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "third_level.jpg")), (SCREEN_WIDTH, SCREEN_HEIGHT))   # Level 3
]

# Load organic garbage images
organic_size = (60, 60) 
organic_garbage_images = [
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "банана.png")), organic_size),
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "ветка.png")), organic_size),
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "кабачок.png")), organic_size),
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "мясо.png")), organic_size),
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "яблоко.png")), organic_size)
]




plastic_size = (60, 60)  # All plastic items will be 40x40 pixels
recyclable_plastic_images = [
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "пакетик.png")), plastic_size),
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "пакетик_2.png")), plastic_size),
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "пакетик_3.png")), plastic_size),
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "пэт-бутылка.png")), plastic_size),
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "бутылка_2.png")), plastic_size),
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "бутылка_3.png")), plastic_size),
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "контейнер.png")), plastic_size),
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "контейнер_2.png")), plastic_size),
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "контейнер_3.png")), plastic_size)
]

# Load background music
pygame.mixer.music.load(os.path.join("assets", "Aisatsana.mp3"))
pygame.mixer.music.play(-1)  # Loop the music indefinitely

# Game variables
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - 50
player_width = 100
player_height = 20
player_speed = 10

plastic_items = []
organic_waste = []
score = 0
recycled_items = 0
item_speed = 5
current_level = 0

# Progress bar variables
progress_bar_width = int(SCREEN_WIDTH * 0.6)  # 60% of the screen width
progress_bar_height = 20
progress_bar_x = (SCREEN_WIDTH - progress_bar_width) // 2  # Centered horizontally
progress_bar_y = 10  # 10 pixels from the top
progress = 0
goals = [20, 50, 100]  # Goals for player transformation
current_goal = goals[0]

# Player transformation states
player_states = [
    pygame.Surface((player_width, player_height)),  # Default state
    pygame.Surface((player_width, player_height)),  # State after 20 items
    pygame.Surface((player_width, player_height)),  # State after 50 items
    pygame.Surface((player_width, player_height))   # State after 100 items
]

# Fill player states with different colors for visual distinction
player_states[0].fill(GREEN)  # Default state
player_states[1].fill(BLUE)   # State after 20 items
player_states[2].fill(YELLOW) # State after 50 items
player_states[3].fill(RED)    # State after 100 items

# Current player state
current_player_state = player_states[0]

# Item properties
item_width = 30
item_height = 30

# Functions
def create_plastic_item():
    x = random.randint(0, SCREEN_WIDTH - item_width)
    y = 0
    image = random.choice(recyclable_plastic_images)
    plastic_items.append({"rect": pygame.Rect(x, y, item_width, item_height), "image": image})

def create_organic_waste():
    x = random.randint(0, SCREEN_WIDTH - item_width)
    y = 0
    image = random.choice(organic_garbage_images)
    organic_waste.append({"rect": pygame.Rect(x, y, item_width, item_height), "image": image})

def draw_player():
    screen.blit(current_player_state, (player_x, player_y))

def draw_items():
    for item in plastic_items:
        screen.blit(item["image"], item["rect"].topleft)
    for waste in organic_waste:
        screen.blit(waste["image"], waste["rect"].topleft)

def update_items():
    for item in plastic_items[:]:
        item["rect"].y += item_speed
        if item["rect"].y > SCREEN_HEIGHT:
            plastic_items.remove(item)
    for waste in organic_waste[:]:
        waste["rect"].y += item_speed
        if waste["rect"].y > SCREEN_HEIGHT:
            organic_waste.remove(waste)

def check_collisions():
    global score, recycled_items, progress, current_goal, current_player_state, item_speed, current_level
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    for item in plastic_items[:]:
        if player_rect.colliderect(item["rect"]):
            plastic_items.remove(item)
            score += 1
            progress += 1
            if score % 50 == 0:
                recycled_items += 1
            if progress >= current_goal:
                # Update player state and goal
                if current_goal == 20:
                    current_player_state = player_states[1]
                elif current_goal == 50:
                    current_player_state = player_states[2]
                elif current_goal == 100:
                    current_player_state = player_states[3]
                # Move to the next goal
                goals.pop(0)
                if goals:
                    current_goal = goals[0]
                else:
                    current_goal = float('inf')  # No more goals
                # Increase item speed
                item_speed += 1
                # Change level if necessary
                if current_level < len(backgrounds) - 1:
                    current_level += 1
    for waste in organic_waste[:]:
        if player_rect.colliderect(waste["rect"]):
            organic_waste.remove(waste)
            score -= 1

def draw_score():
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

def draw_recycled_items():
    recycled_text = font.render(f"Recycled Items: {recycled_items}", True, BLACK)
    screen.blit(recycled_text, (10, 50))

def draw_progress_bar():
    # Draw the background of the progress bar
    pygame.draw.rect(screen, BLACK, (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height))
    # Draw the progress
    progress_width = (progress / current_goal) * progress_bar_width
    pygame.draw.rect(screen, GREEN, (progress_bar_x, progress_bar_y, progress_width, progress_bar_height))
    # Draw the nearest target on the progress bar
    target_text = font.render(f"Target: {current_goal}", True, BLACK)
    target_text_rect = target_text.get_rect(center=(progress_bar_x + progress_bar_width // 2, progress_bar_y + progress_bar_height // 2))
    screen.blit(target_text, target_text_rect)

# Game loop
running = True
while running:
    # Draw the current background
    screen.blit(backgrounds[current_level], (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
        player_x += player_speed

    if random.randint(1, 100) < 5:
        create_plastic_item()
    if random.randint(1, 100) < 3:
        create_organic_waste()

    update_items()
    check_collisions()

    draw_player()
    draw_items()
    draw_score()
    draw_recycled_items()
    draw_progress_bar()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()