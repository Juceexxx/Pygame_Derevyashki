import pygame
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
# Получаем текущее разрешение экрана
infoObject = pygame.display.Info()
WIDTH, HEIGHT =  800, 600
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

# Настройка экрана в полноэкранном режиме
current_resolution = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(current_resolution)
pygame.display.set_caption('Древесные Рыцари')

# Шрифты
font = pygame.font.Font('Bitcell.ttf', 80)
small_font = pygame.font.Font('Bitcell.ttf', 46)

# Переменные для настроек
difficulty_level = 'Легкий'  # Начальный уровень сложности



# Функция для отображения текста на экране
def draw_text(text, fonts, color, surface, x, y):
    textobj = fonts.render(text, True, color)
    surface.blit(textobj, (x, y))
def center_rect(rect):
    """Центрирует прямоугольник в текущем размере экрана."""
    return rect.move((current_resolution[0] - rect.width) // 2, (current_resolution[1] - rect.height) // 2)


# Главная функция меню
def main_menu():
    global current_resolution, screen
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
                if WIDTH // 2 - 150 <= mouse_pos[0] <= WIDTH // 2 + 150:
                    if HEIGHT // 2 + 20 <= mouse_pos[1] <= HEIGHT // 2 + 60:
                        game_loop()  # Начать игру
                    elif HEIGHT // 2 + 90 <= mouse_pos[1] <= HEIGHT // 2 + 130:
                        settings_menu()  # Открыть меню настроек
                    elif HEIGHT // 2 + 160 <= mouse_pos[1] <= HEIGHT // 2 + 200:
                        pygame.quit()
                pygame.quit()
                sys.exit()  # Выход

        # Обновление экрана
        pygame.display.flip()



# Игровые параметры
player_pos = [100, 500]  # Начальная позиция игрока
player_size = 50  # Размер игрока
player_speed = 5  # Скорость движения игрока
gravity = 0.5  # Сила притяжения
jump_strength = 20  # Сила прыжка
is_jumping = False  # Флаг прыжка
velocity_y = 0  # Вертикальная скорость игрока

# Платформы
platforms = [
    pygame.Rect(50, 550, 200, 10),
    pygame.Rect(300, 400, 200, 10),
    pygame.Rect(600, 300, 200, 10),
]
# Основной игровой цикл
def game_loop():
    global is_jumping, velocity_y

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # Завершение программы

        # Обработка ввода
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT]:
            player_pos[0] += player_speed
        if not is_jumping:
            if keys[pygame.K_SPACE]:  # Прыжок
                is_jumping = True
                velocity_y = -jump_strength
        else:
            # Применение силы тяжести
            velocity_y += gravity
            player_pos[1] += velocity_y

            # Проверка коллизии с платформами
            for platform in platforms:
                if player_pos[0] + player_size > platform.x and player_pos[0] < platform.x + platform.width:
                    if player_pos[1] + player_size >= platform.y and player_pos[
                        1] + player_size + velocity_y <= platform.y + platform.height:
                        player_pos[1] = platform.y - player_size
                        is_jumping = False
                        velocity_y = 0

            # Проверка выхода за границы экрана
            if player_pos[1] > HEIGHT:
                player_pos[1] = HEIGHT - player_size
                is_jumping = False
                velocity_y = 0

        # Отображение фона и игрока
        screen.fill(WHITE)  # Заполнение экрана белым цветом
        pygame.draw.rect(screen, "RED", (player_pos[0], player_pos[1], player_size, player_size))  # Рисуем игрока

        # Рисуем платформы
        for platform in platforms:
            pygame.draw.rect(screen, "GREEN", platform)

        # Обновление экрана
        pygame.display.flip()
        pygame.time.Clock().tick(60)  # Ограничение FPS


# Функция для продолжения игры
def continue_game():
    print("Продолжение игры...")  # Здесь будет логика продолжения игры


# Функция для настроек
def settings_menu():
    global current_resolution, screen, fullscreen

    resolutions = [(800, 600), (1024, 768), (1280, 720)]
    difficulty_options = ['Легкий', 'Средний', 'Сложный']

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Отображение фона меню настроек
        screen.blit(background_image, (0, 0))

        # Заголовок настроек
        draw_text('Настройки', font, WHITE, screen, current_resolution[0] // 2 - 150, 50)

        # Уровень сложности
        draw_text('Уровень сложности:', small_font, WHITE, screen, current_resolution[0] // 2 - 150, 150)
        for i, option in enumerate(difficulty_options):
            text_color = WHITE if option != difficulty_level else DIRTY_WHITE
            draw_text(option, small_font, text_color, screen, current_resolution[0] // 2 - 150, 200 + i * 40)
            draw_text('Разрешение экрана:', small_font, WHITE, screen, current_resolution[0] // 2 - 150, 350)
            for i, res in enumerate(resolutions):
                res_text = f'{res[0]}x{res[1]}'
                text_color = WHITE if res != current_resolution else DIRTY_WHITE
                draw_text(res_text, small_font, text_color, screen, current_resolution[0] // 2 - 150, 400 + i * 40)

            # Кнопка "Входной/Полноэкранный режим"
            mode_text = "Переключить на полноэкранный режим" if not fullscreen else "Переключить на оконный режим"
            draw_text(mode_text, small_font, WHITE, screen, current_resolution[0] // 2 - 850, HEIGHT - 1000)


            back_button = pygame.Rect(current_resolution[0] // 2 - 150 , HEIGHT - 550, 100, 30)
            pygame.draw.rect(screen, WHITE, back_button)
            draw_text('Назад', small_font, DARK_GRAY, screen, back_button.x + 10, back_button.y)

            # Обработка нажатий
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()

            for i, res in enumerate(resolutions):
                res_rect = pygame.Rect(current_resolution[0] // 2 - 150, 400 + i * 40 - 5, 100, 30)
                if res_rect.collidepoint(mouse_pos) and mouse_click[0]:
                    current_resolution = res

                    screen = pygame.display.set_mode(current_resolution)


            if back_button.collidepoint(mouse_pos):
                if mouse_click[0]:
                    return

            # Обновление экрана
            pygame.display.flip()


# Запуск
if __name__ == "__main__":
    main_menu()
