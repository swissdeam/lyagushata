import pygame
import random
from config import *

# Игровые переменные состояния
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - 100
player_width = PLAYER_WIDTH
player_height = PLAYER_HEIGHT
plastic_items = []
organic_waste = []
score = 0
item_speed = ITEM_SPEED
current_level = 0
progress = 0
current_goal = GOALS[0]
unlocked_items = []
show_popup = False
player_speed = PLAYER_SPEED 

# Функции
def create_plastic_item():
    x = random.randint(0, SCREEN_WIDTH - ITEM_WIDTH)
    y = 0
    image = random.choice(recyclable_plastic_images)
    plastic_items.append({"rect": pygame.Rect(x, y, ITEM_WIDTH, ITEM_HEIGHT), "image": image})

def create_organic_waste():
    x = random.randint(0, SCREEN_WIDTH - ITEM_WIDTH)
    y = 0
    image = random.choice(organic_garbage_images)
    organic_waste.append({"rect": pygame.Rect(x, y, ITEM_WIDTH, ITEM_HEIGHT), "image": image})

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
    global score, progress, current_goal, item_speed, current_level, show_popup, unlocked_items
    player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
    
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
                if GOALS:
                    GOALS.pop(0)
                if GOALS:
                    current_goal = GOALS[0]
                else:
                    current_goal = float('inf')  # No more goals
                # Increase item speed
                item_speed += 1
                # Change level if necessary
                if current_level < len(backgrounds) - 1:
                    current_level += 1
                
                # Проверка на последний предмет
                if len(unlocked_items) >= len(item_images):
                    show_popup = True
                    return  # Немедленно выходим из функции
                    
    for waste in organic_waste[:]:
        if player_rect.colliderect(waste["rect"]):
            organic_waste.remove(waste)
            score -= 1
            catch_organic_sound.play()

def draw_score():
    score_text = font.render(f"Очки {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def draw_progress_bar():
    # Рисуем фон полосы прогресса с закругленными концами
    pygame.draw.rect(screen, (200, 200, 200, 100), (PROGRESS_BAR_X, PROGRESS_BAR_Y, PROGRESS_BAR_WIDTH, PROGRESS_BAR_HEIGHT), border_radius=10)
    # Рисуем прогресс с закругленными концами и приятным синим оттенком
    progress_width = (progress / current_goal) * PROGRESS_BAR_WIDTH
    pygame.draw.rect(screen, BLUE_SHADE, (PROGRESS_BAR_X, PROGRESS_BAR_Y, progress_width, PROGRESS_BAR_HEIGHT), border_radius=10)

def draw_item_section():
    # Рисуем полупрозрачный серый фон для секции предметов
    item_section_width = 70  # Ширина секции предметов
    item_section_height = len(item_images) * ITEM_SPACING + 20  # Высота на основе количества предметов
    background_surface = pygame.Surface((item_section_width, item_section_height), pygame.SRCALPHA)
    background_surface.fill(LIGHT_GREY)
    screen.blit(background_surface, (ITEM_SECTION_X - 10, ITEM_SECTION_Y - 10))  # Отступ для подложки

    # Рисуем предметы
    for i in range(len(item_images)):
        if i in unlocked_items:
            screen.blit(item_images[i], (ITEM_SECTION_X, ITEM_SECTION_Y + i * ITEM_SPACING))
        else:
            # Рисуем темно-синий силуэт
            silhouette = pygame.Surface((50, 50), pygame.SRCALPHA)
            silhouette.fill(DARK_BLUE)
            screen.blit(silhouette, (ITEM_SECTION_X, ITEM_SECTION_Y + i * ITEM_SPACING))

def draw_instruction_popup():
    # Рисуем размытый фон (уровень 3)
    screen.blit(backgrounds[2], (0, 0))
    # Рисуем окно подсказки
    popup_width = 600
    popup_height = 400
    popup_x = (SCREEN_WIDTH - popup_width) // 2
    popup_y = (SCREEN_HEIGHT - popup_height) // 2
    pygame.draw.rect(screen, (200, 200, 200, 200), (popup_x, popup_y, popup_width, popup_height), border_radius=20)
    # Рисуем заголовок
    title_text = font.render("Добро пожаловать в игру Recycle Game!", True, BLACK)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, popup_y + 50))
    screen.blit(title_text, title_rect)
    # Рисуем текст инструкции
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
    # Рисуем текст "Нажмите ПРОБЕЛ, чтобы начать"
    start_text = small_font.render("Нажмите ПРОБЕЛ, чтобы начать", True, BLACK)
    start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, popup_y + 350))
    screen.blit(start_text, start_rect)

def draw_popup():
    # Draw the blurred background (level 3)
    screen.blit(backgrounds[2], (0, 0))
    # Draw the popup box
    popup_width = 600
    popup_height = 400
    popup_x = (SCREEN_WIDTH - popup_width) // 2
    popup_y = (SCREEN_HEIGHT - popup_height) // 2
    pygame.draw.rect(screen, (200, 200, 200, 200), (popup_x, popup_y, popup_width, popup_height), border_radius=20)
    # Draw the title
    title_text = font.render("поздравляю!", True, BLACK)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, popup_y + 50))
    screen.blit(title_text, title_rect)
    # Draw the message
    message_text = [
        "Вы спасли город от мусора!",
        "Вы большой молодец, спасибо Вам!"
    ]
    for i, line in enumerate(message_text):
        line_surface = small_font.render(line, True, BLACK)
        line_rect = line_surface.get_rect(center=(SCREEN_WIDTH // 2, popup_y + 150 + i * 30))
        screen.blit(line_surface, line_rect)
    # Draw the "Play Again" button
    play_again_button = pygame.Rect(popup_x + 50, popup_y + 250, 200, 50)
    pygame.draw.rect(screen,BLUE_SHADE, play_again_button, border_radius=10)
    play_again_text = small_font.render("Сыграть снова", True, WHITE)
    play_again_rect = play_again_text.get_rect(center=play_again_button.center)
    screen.blit(play_again_text, play_again_rect)
    # Draw the "Exit" button
    exit_button = pygame.Rect(popup_x + 350, popup_y + 250, 200, 50)
    pygame.draw.rect(screen, ROSE, exit_button, border_radius=10)
    exit_text = small_font.render("Выйти", True, WHITE)
    exit_rect = exit_text.get_rect(center=exit_button.center)
    screen.blit(exit_text, exit_rect)
    return play_again_button, exit_button

def reset_game():
    global player_x, player_y, plastic_items, organic_waste, score, item_speed
    global current_level, progress, current_goal, unlocked_items, show_popup, GOALS
    
    player_x = SCREEN_WIDTH // 2
    player_y = SCREEN_HEIGHT - 100
    plastic_items = []
    organic_waste = []
    score = 0
    item_speed = ITEM_SPEED
    current_level = 0
    progress = 0
    GOALS = [20, 50, 70, 100, 120]  # Восстанавливаем исходные цели
    current_goal = GOALS[0]
    unlocked_items = []
    show_popup = False

# Игровой цикл
running = True
show_instructions = True
while running:
    if show_instructions:
        # Показываем окно с инструкциями
        draw_instruction_popup()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    show_instructions = False
    elif show_popup:
        # Draw the current background
        screen.blit(backgrounds[current_level], (0, 0))
        play_again_button, exit_button = draw_popup()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_again_button.collidepoint(mouse_pos):
                    reset_game()
                elif exit_button.collidepoint(mouse_pos):
                    running = False
    else:
        # Draw the current background
        screen.blit(backgrounds[current_level], (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Игровая логика только если не показывается popup
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