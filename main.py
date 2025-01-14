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
DIRTY_WHITE = (215, 215, 215)
BROWN = (139, 69, 19)
DARK_GRAY = (128, 128, 128)

# Загрузка изображений и изменение размера
button_image = pygame.image.load('Button.png')
button_image = pygame.transform.scale(button_image, (300, 70))
new_button_image = pygame.image.load('New_Button.png')
new_button_image = pygame.transform.scale(new_button_image, (300, 70))
settings_button_image = pygame.image.load('Settings_Button.png')
settings_button_image = pygame.transform.scale(settings_button_image, (300, 70))
exit_button_image = pygame.image.load('Exit_Button.png')
exit_button_image = pygame.transform.scale(exit_button_image, (300, 70))
next_button_image = pygame.image.load('Next_Button.png')
next_button_image = pygame.transform.scale(next_button_image, (300, 70))
background_image = pygame.image.load('background.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Шрифты
font = pygame.font.Font('Bitcell.ttf', 80)
small_font = pygame.font.Font('Bitcell.ttf', 46)


# Функция для отображения текста на экране
def draw_text(text, fonts, color, surface, x, y):
    textobj = fonts.render(text, True, color)
    surface.blit(textobj, (x, y))


# Главная функция меню
def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Отображение фонового изображения
        screen.blit(background_image, (0, 0))

        # Фон кнопок и заголовкае
        surf = pygame.Surface((325, 400))
        surf.fill(DARK_GRAY)
        surf.set_alpha(200)
        screen.blit(surf, (262, 90))

        # Отображение заголовка
        draw_text('Деревяшки', font, WHITE, screen, 275, 100)

        # Создание кнопок
        start_button = screen.blit(button_image, (275, 183))
        continue_button = screen.blit(button_image, (275, 253))
        settings_button = screen.blit(button_image, (275, 323))
        exit_button = screen.blit(button_image, (275, 393))
        draw_text('Новая игра', small_font, DIRTY_WHITE, screen, 315, 193)
        draw_text('Продолжить', small_font, DIRTY_WHITE, screen, 307, 263)
        draw_text('Настройки', small_font, DIRTY_WHITE, screen, 320, 333)
        draw_text('Выход', small_font, DIRTY_WHITE, screen, 340, 403)

        # Обработка нажатий кнопок и из изменение
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if start_button.collidepoint(mouse_pos):
            screen.blit(new_button_image, (275, 183))
            draw_text('Новая игра', small_font, DIRTY_WHITE, screen, 315, 193)
            if mouse_click[0]:
                game_loop()  # Вызов функции игры
        elif continue_button.collidepoint(mouse_pos):
            screen.blit(next_button_image, (275, 253))
            draw_text('Продолжить', small_font, DIRTY_WHITE, screen, 307, 263)
            if mouse_click[0]:
                continue_game()  # Вызов функции продолжения игры
        elif settings_button.collidepoint(mouse_pos):
            screen.blit(settings_button_image, (275, 323))
            draw_text('Настройки', small_font, DIRTY_WHITE, screen, 320, 333)
            if mouse_click[0]:
                settings_menu()  # Вызов функции настроек
        elif exit_button.collidepoint(mouse_pos):
            screen.blit(exit_button_image, (275, 393))
            draw_text('Выход', small_font, DIRTY_WHITE, screen, 340, 403)
            if mouse_click[0]:
                pygame.quit()
                sys.exit()  # Выход

        # Обновление экрана
        pygame.display.flip()


# Основной игровой цикл
def game_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Логика игры будет здесь

        # Обновление экрана
        screen.fill(BROWN)  # To Do Заменить на игровую логику
        pygame.display.flip()


# Функция для продолжения игры
def continue_game():
    print("Продолжение игры...")  # Здесь будет логика продолжения игры


# Функция для настроек
def settings_menu():
    print("Настройки...")  # Здесь будут настройки


# Запуск
if __name__ == "__main__":
    main_menu()
