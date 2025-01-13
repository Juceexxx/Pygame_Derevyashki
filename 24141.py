import pygame
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Древесные Рыцари")

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BROWN = (139, 69, 19)
GRAY = (200, 200, 200)

background_image = pygame.image.load('background.png')  # Замените на путь к вашему изображению
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Изменяем размер изображения под экран

# Шрифты
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Функция для отображения текста на экране
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Функция для создания кнопки
def draw_button(text, x, y, width, height, color):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, button_rect)
    draw_text(text, small_font, WHITE, screen, x + 10, y + 10)
    return button_rect

# Главная функция меню
def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Отображение фонового изображения
        screen.blit(background_image, (0, 0))


        # Отображение заголовка
        draw_text('Деревяшки', font, WHITE, screen, 300, 100)

        # Создание кнопок
        start_button = draw_button('Начать игру', 300, 200, 200, 50, GREEN)
        continue_button = draw_button('Продолжить игру', 300, 270, 250, 50, GREEN)
        settings_button = draw_button('Настройки', 300, 340, 200, 50, GREEN)
        exit_button = draw_button('Выход', 300, 410, 200, 50, GREEN)

        # Обработка нажатий кнопок
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if start_button.collidepoint(mouse_pos) and mouse_click[0]:
            game_loop()  # Здесь вы можете вызвать функцию игры
        elif continue_button.collidepoint(mouse_pos) and mouse_click[0]:
            continue_game()  # Функция для продолжения игры
        elif settings_button.collidepoint(mouse_pos) and mouse_click[0]:
            settings_menu()  # Функция для настроек
        elif exit_button.collidepoint(mouse_pos) and mouse_click[0]:
            pygame.quit()
            sys.exit()

        # Обновление экрана
        pygame.display.flip()

# Основной игровой цикл (здесь можно разместить логику игры)
def game_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Логика игры будет здесь

        # Обновление экрана
        screen.fill(BROWN)  # Замените на вашу игровую логику
        pygame.display.flip()

# Функция для продолжения игры
def continue_game():
    print("Продолжение игры...")  # Здесь вы можете добавить логику продолжения

# Функция для настроек
def settings_menu():
    print("Настройки...")  # Здесь вы можете добавить логику настроек

if __name__ == "__main__":
    main_menu()
