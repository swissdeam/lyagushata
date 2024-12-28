import pygame
import random
import os
from pygame.locals import *

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE_SHADE = (100, 149, 237)  # Nice blue shade for the progress bar
DARK_BLUE = (25, 25, 112)  # Dark blue for silhouettes
LIGHT_GREY = (200, 200, 200, 150) 

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Recycle Game")

# Clock
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 36)  # Use a nicer font (replace "arial.ttf" with your font file)
small_font = pygame.font.Font(None, 24)  # Smaller font for instructions

# Load and resize background images
backgrounds = [
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "first_level.jpg")), (SCREEN_WIDTH, SCREEN_HEIGHT)),  # Level 1
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "second_level.jpg")), (SCREEN_WIDTH, SCREEN_HEIGHT)),  # Level 2
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "third_level.jpg")), (SCREEN_WIDTH, SCREEN_HEIGHT))   # Level 3
]

# Apply 15% blur to all backgrounds
for i in range(len(backgrounds)):
    backgrounds[i] = pygame.transform.smoothscale(backgrounds[i], (SCREEN_WIDTH // 7, SCREEN_HEIGHT // 7))
    backgrounds[i] = pygame.transform.smoothscale(backgrounds[i], (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load player image
player_image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "frog.png")), (100, 100))

organic_size = (60, 60)
organic_garbage_images = [
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "банана.png")), organic_size),
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "ветка.png")), organic_size),
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "кабачок.png")), organic_size),
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "мясо.png")), organic_size),
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "яблоко.png")), organic_size)
]


# Load recyclable plastic images and resize them to a small size
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


# Load item images for the left section
item_images = [
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "player1.png")), (50, 50)),  # Item 1
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "player2.png")), (50, 50)),  # Item 2
    pygame.transform.scale(pygame.image.load(os.path.join("assets", "player3.png")), (50, 50))   # Item 3
]

# Load sounds (MP3 format)
catch_organic_sound = pygame.mixer.Sound(os.path.join("assets", "frog.mp3"))
unlock_item_sound = pygame.mixer.Sound(os.path.join("assets", "create.mp3"))

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

# Item section variables
item_section_x = 10
item_section_y = 100
item_spacing = 60
unlocked_items = []  # List of unlocked items

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
    screen.blit(player_image, (player_x, player_y))

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
    global score, progress, current_goal, item_speed, current_level
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    for item in plastic_items[:]:
        if player_rect.colliderect(item["rect"]):
            plastic_items.remove(item)
            score += 1
            progress += 1
            if progress >= current_goal:
                # Unlock a new item
                if len(unlocked_items) < len(item_images):
                    unlocked_items.append(len(unlocked_items))
                    unlock_item_sound.play()
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
            catch_organic_sound.play()

def draw_score():
    score_text = font.render(f"Очки {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def draw_progress_bar():
    # Draw the background of the progress bar with rounded ends
    pygame.draw.rect(screen, (200, 200, 200, 100), (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height), border_radius=10)
    # Draw the progress with rounded ends and a nice blue shade
    progress_width = (progress / current_goal) * progress_bar_width
    pygame.draw.rect(screen, BLUE_SHADE, (progress_bar_x, progress_bar_y, progress_width, progress_bar_height), border_radius=10)

def draw_item_section():
    # Draw a light grey semi-transparent background for the item section
    item_section_width = 70  # Width of the item section
    item_section_height = len(item_images) * item_spacing + 20  # Height based on the number of items
    background_surface = pygame.Surface((item_section_width, item_section_height), pygame.SRCALPHA)
    background_surface.fill(LIGHT_GREY)
    screen.blit(background_surface, (item_section_x - 10, item_section_y - 10))  # Offset for padding

    # Draw the items
    for i in range(len(item_images)):
        if i in unlocked_items:
            screen.blit(item_images[i], (item_section_x, item_section_y + i * item_spacing))
        else:
            # Draw a dark blue silhouette
            silhouette = pygame.Surface((50, 50), pygame.SRCALPHA)
            silhouette.fill(DARK_BLUE)
            screen.blit(silhouette, (item_section_x, item_section_y + i * item_spacing))

def draw_instruction_popup():
    # Draw the blurred background (level 3)
    screen.blit(backgrounds[2], (0, 0))
    # Draw the popup box
    popup_width = 600
    popup_height = 400
    popup_x = (SCREEN_WIDTH - popup_width) // 2
    popup_y = (SCREEN_HEIGHT - popup_height) // 2
    pygame.draw.rect(screen, (200, 200, 200, 200), (popup_x, popup_y, popup_width, popup_height), border_radius=20)
    # Draw the title
    title_text = font.render("Добро пожаловать в игру Recycle Game!", True, BLACK)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, popup_y + 50))
    screen.blit(title_text, title_rect)
    # Draw the instruction text
    instruction_text = [
        "В этой игре вы играете за персонажа, который перерабатывает пластик,",
        "чтобы спасти окружающую среду. Избегайте органических отходов",
        "и собирайте как можно больше пластика,",
        "чтобы разблокировать новые предметы и уровни",
        "Удачи!"
    ]
    for i, line in enumerate(instruction_text):
        line_surface = small_font.render(line, True, BLACK)
        line_rect = line_surface.get_rect(center=(SCREEN_WIDTH // 2, popup_y + 150 + i * 30))
        screen.blit(line_surface, line_rect)
    # Draw the "Press SPACE to start" text
    start_text = small_font.render("Нажмите ПРОБЕЛ, чтобы начать", True, BLACK)
    start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, popup_y + 350))
    screen.blit(start_text, start_rect)

# Game loop
running = True
show_instructions = True
while running:
    if show_instructions:
        # Draw the instruction popup
        draw_instruction_popup()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    show_instructions = False
    else:
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
        draw_item_section()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()