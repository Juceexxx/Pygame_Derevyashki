import pygame
import sys
import os

# Инициализация Pygame
pygame.init()

# Получаем текущее разрешение экрана
infoObject = pygame.display.Info()
WIDTH_1, HEIGHT_1 = infoObject.current_w, infoObject.current_h
current_resolution = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Древесные Рыцари")

# Константы
WHITE = (255, 255, 255)
DIRTY_WHITE = (215, 215, 215)
BROWN = (139, 69, 19)
DARK_GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FPS = 60

# Загрузка изображений и изменение размера

def load_image(name):
    fullname = os.path.join('Data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f'Файл с изображением "{fullname}" не найден')
        sys.exit()
    image = pygame.image.load(fullname)
    return image


LPS_image = load_image('LPS.png')
LPS_image = pygame.transform.scale(LPS_image, (100, 100))
button_image = load_image('Button.png')
button_image = pygame.transform.scale(button_image, (300, 70))
standart_button_image = load_image('Sandart_Button.png')
standart_button_image = pygame.transform.scale(standart_button_image, (300, 70))
back_button_image = load_image('Back_Button.png')
back_button_image = pygame.transform.scale(back_button_image, (240, 60))
new_button_image = load_image('New_Button.png')
new_button_image = pygame.transform.scale(new_button_image, (300, 70))
settings_button_image = load_image('Settings_Button.png')
settings_button_image = pygame.transform.scale(settings_button_image, (300, 70))
exit_button_image = load_image('Exit_Button.png')
exit_button_image = pygame.transform.scale(exit_button_image, (300, 70))
next_button_image = load_image('Next_Button.png')
next_button_image = pygame.transform.scale(next_button_image, (300, 70))
grass_without_wind_image = load_image('Grass_Without_Wind.png')
# grass_without_wind_image
grass_with_wind = load_image('Grass_With_Wind.png')
# grass_with_wind
grass_with_strong_wind = load_image('Grass_With_Strong_Wind.png')
# grass_with_strong_wind
background_image = load_image('background.png')
background_image = pygame.transform.scale(background_image, current_resolution)


# Изменение разрешения
def screen_resolution():
    if current_resolution == (current_resolution):
        screen.blit(pygame.transform.scale(background_image, current_resolution), (0, 0))

# Настройка экрана в полноэкранном режиме
# screen = pygame.display.set_mode(current_resolution)
pygame.display.set_caption('Древесные Рыцари')

# Шрифты
font = pygame.font.Font('Bitcell.ttf', 80)
small_font = pygame.font.Font('Bitcell.ttf', 46)

# Переменные для настроек
difficulty_level = 'Легкий'  # Начальный уровень сложности
full_screen = False


# Функция для отображения текста на экране
def draw_text(ext, fonts, color, surface, x, y):
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
                sys.exit()

        # Отображение фонового изображения
        screen_resolution()

        # Фон кнопок и заголовка
        surf = pygame.Surface((325, 400))
        surf.fill(DARK_GRAY)
        surf.set_alpha(200)
        screen.blit(surf, (WIDTH // 2 - 162, HEIGHT // 2 - 90))

        # Отображение заголовка
        draw_text('Деревяшки', font, WHITE, screen, WIDTH // 2 - 150, HEIGHT // 6)

        # Создание кнопок
        start_button = screen.blit(button_image, (WIDTH // 2 - 150, HEIGHT // 3.279))
        continue_button = screen.blit(button_image, (WIDTH // 2 - 150, HEIGHT // 3.279 + 70))
        settings_button = screen.blit(button_image, (WIDTH // 2 - 150, HEIGHT // 3.279 + 140))
        exit_button = screen.blit(button_image, (WIDTH // 2 - 150, HEIGHT // 3.279 + 210))
        draw_text('Новая игра', small_font, DIRTY_WHITE, screen, start_button.x + 40, start_button.y + 13)
        draw_text('Продолжить', small_font, DIRTY_WHITE, screen, continue_button.x + 32, continue_button.y + 13)
        draw_text('Настройки', small_font, DIRTY_WHITE, screen, settings_button.x + 45, settings_button.y + 13)
        draw_text('Выход', small_font, DIRTY_WHITE, screen, exit_button.x + 65, exit_button.y + 13)

        # Обработка нажатий кнопок и их изменение
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if start_button.collidepoint(mouse_pos):
            screen.blit(new_button_image, (WIDTH // 2 - 150, HEIGHT // 3.279))
            draw_text('Новая игра', small_font, DIRTY_WHITE, screen, start_button.x + 40, start_button.y + 13)
            if mouse_click[0]:
                game_loop()  # Вызов функции игры
        elif continue_button.collidepoint(mouse_pos):
            screen.blit(next_button_image, (WIDTH // 2 - 150, HEIGHT // 3.279 + 70))
            draw_text('Продолжить', small_font, DIRTY_WHITE, screen, continue_button.x + 32, continue_button.y + 13)
            if mouse_click[0]:
                continue_game()  # Вызов функции продолжения игры
        elif settings_button.collidepoint(mouse_pos):
            screen.blit(settings_button_image, (WIDTH // 2 - 150, HEIGHT // 3.279 + 140))
            draw_text('Настройки', small_font, DIRTY_WHITE, screen, settings_button.x + 45, settings_button.y + 13)
            if mouse_click[0]:
                settings_menu()  # Вызов функции настроек
        elif exit_button.collidepoint(mouse_pos):
            screen.blit(exit_button_image, (WIDTH // 2 - 150, HEIGHT // 3.279 + 210))
            draw_text('Выход', small_font, DIRTY_WHITE, screen, exit_button.x + 65, exit_button.y + 13)
            if mouse_click[0]:
                if WIDTH // 2 - 150 <= mouse_pos[0] <= WIDTH // 2 + 150:
                sys.exit()  # Выход

        # Обновление экрана
        pygame.display.flip()




# Основной игровой цикл
def game_loop():
    # Инициализация Pygame
    pygame.init()

    # Создание окна
    if current_resolution == (1920, 1080):
        screen = pygame.display.set_mode(current_resolution, pygame.FULLSCREEN)
        full_screen = True
    else:
        screen = pygame.display.set_mode(current_resolution)
        full_screen = False
    pygame.display.set_caption("Кубик красный")

    # Переменные игрока
    player_pos = [WIDTH // 2, HEIGHT // 2]
    player_speed_y = 0
    on_ground = False

    # Платформы
    platforms = [
        pygame.Rect(100, 500, 200, 20),
        pygame.Rect(400, 400, 200, 20),
        pygame.Rect(600, 300, 650, 20)
    ]

    # Основной игровой цикл
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and on_ground:
                    player_speed_y = -15

        # Управление движением
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_pos[0] -= 5
        if keys[pygame.K_RIGHT]:
            player_pos[0] += 5

        # Проверка на границы экрана
        if player_pos[0] < 0:
            player_pos[0] = 0
        if player_pos[0] > WIDTH - 50:
            player_pos[0] = WIDTH - 50

        # Гравитация
        player_speed_y += 1
        player_pos[1] += player_speed_y

        # Проверка на столкновение с платформами
        on_ground = False
        for platform in platforms:
            if pygame.Rect(player_pos[0], player_pos[1], 50, 50).colliderect(platform) and player_speed_y >= 0:
                player_pos[1] = platform.top - 50
                on_ground = True
                player_speed_y = 0
                break

        # Проверка на землю
        if not on_ground and player_pos[1] >= HEIGHT - 50:
            player_pos[1] = HEIGHT - 50
            on_ground = True
            player_speed_y = 0

        # Отрисовка
        screen.fill(WHITE)
        for platform in platforms:
            pygame.draw.rect(screen, GREEN, platform)
        pygame.draw.rect(screen, RED, (*player_pos, 50, 50))

        pygame.display.flip()
        clock.tick(FPS)


# Функция для продолжения игры
def continue_game():
    print("Продолжение игры...")  # Здесь будет логика продолжения игры


# Функция для настроек
def settings_menu():
    global current_resolution, screen, full_screen, WIDTH, HEIGHT

    resolutions = [(1920, 1080), (1280, 720), (1024, 768), (800, 600)]
    difficulty_options = ['Большой детина', 'Идеальный баланс', 'Суровая реальность']

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Отображение фона меню настроек
        screen_resolution()
        # Заголовок настроек
        draw_text('Настройки', font, WHITE, screen, WIDTH // 2 - 150, 50)

        # Уровень сложности
        draw_text('Уровень сложности:', small_font, WHITE, screen, current_resolution[0] // 2 - 150, 150)
        draw_text('Разрешение экрана:', small_font, WHITE, screen, current_resolution[0] // 2 - 150, 350)

        for i, option in enumerate(difficulty_options):
            text_color = WHITE if option != difficulty_level else DIRTY_WHITE
            draw_text(option, small_font, text_color, screen, current_resolution[0] // 2 - 150, 200 + i * 40)

        for j, res in enumerate(resolutions):
            if res == (1920, 1080):
                res_rext = 'Полноэкранный режии'
            else:
                res_text = f'{res[0]}x{res[1]}'
            text_color = WHITE if res != current_resolution else DIRTY_WHITE
            draw_text(res_text, small_font, text_color, screen, current_resolution[0] // 2 - 150, 400 + j * 40)


        back_button = screen.blit(back_button_image, (10, HEIGHT - 70))
        draw_text('Назад', small_font, DIRTY_WHITE, screen, back_button.x + 100, back_button.y + 5)

        # Обработка нажатий
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        for k, res in enumerate(resolutions):
            res_rect = pygame.Rect(current_resolution[0] // 2 - 150, 400 + k * 40 - 5, 100, 30)
            if res_rect.collidepoint(mouse_pos) and mouse_click[0]:
                current_resolution = res
                WIDTH, HEIGHT = current_resolution

                # Установка режима отображения
                if current_resolution == (1920, 1080):
                    screen = pygame.display.set_mode(current_resolution, pygame.FULLSCREEN)
                    full_screen = True
                else:
                    screen = pygame.display.set_mode(current_resolution)
                    full_screen = False

                screen.blit(background_image, (0, 0))

        if back_button.collidepoint(mouse_pos):
            if mouse_click[0]:
                return

        # Обновление экрана
        pygame.display.flip()


# Запуск
if __name__ == "__main__":
    main_menu()
