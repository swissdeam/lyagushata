import pygame
import os

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

icon = pygame.image.load('assets/frog.ico') 
pygame.display.set_icon(icon)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE_SHADE = (100, 149, 237)
DARK_BLUE = (25, 25, 112)
LIGHT_GREY = (200, 200, 200, 150)
ROSE = (255, 203, 221)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Recycle Game")

# Clock
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Load and scale backgrounds
backgrounds = [
    pygame.transform.scale(pygame.image.load(os.path.join("assets", f"{i}.jpg")), (SCREEN_WIDTH, SCREEN_HEIGHT))
    for i in range(1, 6)
]
backgrounds.insert(4, pygame.transform.scale(pygame.image.load(os.path.join("assets", "third_level.jpg")), (SCREEN_WIDTH, SCREEN_HEIGHT)))

for i in range(len(backgrounds)):
    backgrounds[i] = pygame.transform.smoothscale(backgrounds[i], (SCREEN_WIDTH // 7, SCREEN_HEIGHT // 7))
    backgrounds[i] = pygame.transform.smoothscale(backgrounds[i], (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load player image
player_image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "frog.png")), (100, 100))

# Load garbage images
organic_size = (60, 60)
organic_garbage_images = [
    pygame.transform.scale(pygame.image.load(os.path.join("assets", img)), organic_size)
    for img in ["банана.png", "ветка.png", "кабачок.png", "мясо.png", "яблоко.png"]
]

plastic_size = (60, 60)
recyclable_plastic_images = [
    pygame.transform.scale(pygame.image.load(os.path.join("assets", img)), plastic_size)
    for img in ["пакетик.png", "пакетик_2.png", "пакетик_3.png", "бутылка.png",
                "контейнер.png", "контейнер_2.png", "контейнер_3.png"]
]

# Load item images
item_images = [
    pygame.transform.scale(pygame.image.load(os.path.join("assets", f"win-item{i}.png")), (50, 50))
    for i in [1, 2, 3, 4, 5]
]

# Load sounds
catch_organic_sound = pygame.mixer.Sound(os.path.join("assets", "frog.mp3"))
unlock_item_sound = pygame.mixer.Sound(os.path.join("assets", "win.mp3"))

# Load and play background music
pygame.mixer.music.load(os.path.join("assets", "Aisatsana.mp3"))
pygame.mixer.music.play(-1)

# Game settings
PLAYER_WIDTH = 100
PLAYER_HEIGHT = 100
PLAYER_SPEED = 10
ITEM_SPEED = 5
GOALS = [20, 50, 70, 100, 120]

# Progress bar settings
PROGRESS_BAR_WIDTH = int(SCREEN_WIDTH * 0.6)
PROGRESS_BAR_HEIGHT = 20
PROGRESS_BAR_X = (SCREEN_WIDTH - PROGRESS_BAR_WIDTH) // 2
PROGRESS_BAR_Y = 10

# Item section settings
ITEM_SECTION_X = 10
ITEM_SECTION_Y = 100
ITEM_SPACING = 60
ITEM_WIDTH = 40
ITEM_HEIGHT = 40 