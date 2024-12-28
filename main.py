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
BLUE_SHADE = (100, 149, 237)  # Nice blue shade for the progress bar

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Recycle Game")

# Clock
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 36)  # Use a nicer font (replace "arial.ttf" with your font file)


# Load and resize background images
backgrounds = [
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "first_level.jpg")), (SCREEN_WIDTH, SCREEN_HEIGHT)),  # Level 1
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "second_level.jpg")), (SCREEN_WIDTH, SCREEN_HEIGHT)),  # Level 2
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "third_level.jpg")), (SCREEN_WIDTH, SCREEN_HEIGHT))   # Level 3
]
# Load player images for each level
player_images = [
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "player1.png")), (100, 100)),  # Level 1
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "player2.png")), (100, 100)),  # Level 2
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "player3.png")), (100, 100))   # Level 3
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




plastic_size = (60, 60)  
recyclable_plastic_images = [
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "пакетик.png")), plastic_size),
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "пакетик_2.png")), plastic_size),
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "пакетик_3.png")), plastic_size),
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "пэт-бутылка.png")), plastic_size),
    # pygame.transform.scale(pygame.image.load(os.path.join("assets", "бутылка_2.png")), plastic_size),
    # pygame.transform.scale(pygame.image.load(os.path.join("assets", "бутылка_3.png")), plastic_size),
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "контейнер.png")), plastic_size),
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "контейнер_2.png")), plastic_size),
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "контейнер_3.png")), plastic_size)
]


# Load background music
pygame.mixer.music.load(os.path.join("assets", "Aisatsana.mp3"))
pygame.mixer.music.play(-1)  # Loop the music indefinitely




# Game variables
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - 100
player_width = 100
player_height = 100
player_speed = 10

plastic_items = []
organic_waste = []
score = 0
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

# Current player image
current_player_image = player_images[current_level]

# Item properties
item_width = 40  # Same as plastic_size width
item_height = 40  # Same as plastic_size height

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
    screen.blit(current_player_image, (player_x, player_y))

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
    global score, progress, current_goal, current_player_image, item_speed, current_level
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    for item in plastic_items[:]:
        if player_rect.colliderect(item["rect"]):
            plastic_items.remove(item)
            score += 1
            progress += 1
            if progress >= current_goal:
                # Update player state and goal
                if current_goal == 20:
                    current_player_image = player_images[1]
                elif current_goal == 50:
                    current_player_image = player_images[2]
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
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def draw_progress_bar():
    # Draw the background of the progress bar with rounded ends
    pygame.draw.rect(screen, (200, 200, 200, 100), (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height), border_radius=10)
    # Draw the progress with rounded ends and a nice blue shade
    progress_width = (progress / current_goal) * progress_bar_width
    pygame.draw.rect(screen, BLUE_SHADE, (progress_bar_x, progress_bar_y, progress_width, progress_bar_height), border_radius=10)
    # Draw the nearest target on the progress bar
    # target_text = font.render(f"Target: {current_goal}", True, BLACK)
    # target_text_rect = target_text.get_rect(center=(progress_bar_x + progress_bar_width // 2, progress_bar_y + progress_bar_height // 2))
    # screen.blit(target_text, target_text_rect)

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
    draw_progress_bar()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()