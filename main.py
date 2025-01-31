import pygame
import sys
import os
import sqlite3
import pygame_gui
from cv2 import CAP_PROP_FRAME_HEIGHT, cvtColor, COLOR_BGR2RGB, VideoCapture, CAP_PROP_FRAME_WIDTH, CAP_PROP_FPS

from Animation import AnimatedSprite
from Enemy import Enemy
from Bullet import Bullet

# Инициализация Pygame
pygame.init()

# Получаем текущее разрешение экрана
infoObject = pygame.display.Info()
WIDTH_1, HEIGHT_1 = infoObject.current_w, infoObject.current_h
current_resolution = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Древесные Рыцари")
all_sprites = pygame.sprite.Group()
manager = pygame_gui.UIManager(current_resolution)
clock = pygame.time.Clock()

# Константы
WHITE = (255, 255, 255)
DIRTY_WHITE = (215, 215, 215)
BROWN = (139, 69, 19)
DARK_GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FPS = 60
BULLET_SPEED = 5
HP = 100
DAMAGE = 100
zhmuriki = 0

# Настройка экрана в полноэкранном режиме
pygame.display.set_caption('Древесные Рыцари')

# Переменные по умолчанию
current_difficulty = 'Большой детина'
entry = False
name_user = ''
hp_player = 100
damage_player = 100
hp_enemy_pitch = 100
damage_enemy_pitch = 100
speed_en = 1

# Шрифты
font = pygame.font.Font('Data/Bitcell.ttf', 80)
small_font = pygame.font.Font('Data/Bitcell.ttf', 46)
miles_font = pygame.font.Font('Data/Bitcell.ttf', 30)

hello_text = open('Data/Hello_text.txt', 'r')
hello_text.read()
hello_text.close()


# Загрузка изображений и изменение размера
def load_image(name):
    fullname = os.path.join('Data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f'Файл с изображением "{fullname}" не найден')
        pygame.quit()
        sys.exit()
    image = pygame.image.load(fullname).convert_alpha()
    return image


LPS_image = load_image('LPS.png')
LPS_image = pygame.transform.scale(LPS_image, (64 * 5, 16 * 5))
button_image = load_image('Button.png')
button_image = pygame.transform.scale(button_image, (300, 70))
standard_button_image = load_image('Standard_Button.png')
standard_button_image = pygame.transform.scale(standard_button_image, (300, 70))
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
button_r_image = load_image('Button_R.png')
button_r_image = pygame.transform.scale(button_r_image, (200, 62))
sign_in_button_image = load_image('Sign_In_Button.png')
sign_in_button_image = pygame.transform.scale(sign_in_button_image, (200, 62))
exit_door_image = load_image('Exit_Door.png')
exit_door_image = pygame.transform.scale(exit_door_image, (100, 130))
platform_image = load_image('Platform.png')
platform_image = pygame.transform.scale(platform_image, (200, 33))
level_one_image = load_image('Level_One.png')
level_one_image = pygame.transform.scale(level_one_image, (200, 200))
level_one_alt_image = load_image('Level_One_Alt.png')
level_one_alt_image = pygame.transform.scale(level_one_alt_image, (200, 200))
level_two_image = load_image('Level_Two.png')
level_two_image = pygame.transform.scale(level_two_image, (200, 200))
level_two_alt_image = load_image('Level_Two_Alt.png')
level_two_alt_image = pygame.transform.scale(level_two_alt_image, (200, 200))
enemy_pitch_r_image = load_image('Enemy_Pitch_R.png')
enemy_pitch_l_image = load_image('Enemy_Pitch_L.png')
arrow_r_image = load_image('Arrow_R.png')
arrow_l_image = load_image('Arrow_L.png')
grass_image = load_image('Grass.png')
# lp_go = load_image('LP_Go.png')
# lp_go = pygame.transform.scale(lp_go, (64 * 6, 16 * 6))
lp_go_r_c_images = load_image('LP_Go_R_Crossbow.png')
lp_go_r_c_images = pygame.transform.scale(lp_go_r_c_images, (64 * 5, 16 * 5))
lp_go_l_c_images = load_image('LP_Go_L_Crossbow.png')
lp_go_l_c_images = pygame.transform.scale(lp_go_l_c_images, (64 * 5, 16 * 5))
background_image = load_image('background.png')
background_image = pygame.transform.scale(background_image, current_resolution)


def difficulty():
    global damage_player, damage_enemy_pitch, speed_en
    damage_player_id = 1
    damage_enemy_pitch_id = 1
    if current_difficulty == 'Большой детина':
        damage_player_id = 1
        damage_enemy_pitch_id = 0.334
        speed_en = 1
    elif current_difficulty == 'Идеальный баланс':
        damage_player_id = 1.5
        damage_enemy_pitch_id = 0.667
        speed_en = 1
    elif current_difficulty == 'Суровая реальность':
        damage_player_id = 2
        damage_enemy_pitch_id = 1
        speed_en = 2

    damage_enemy_pitch = DAMAGE * damage_enemy_pitch_id
    damage_player = DAMAGE // damage_player_id


# Изменение разрешения
def screen_back_ground():
    screen.blit(pygame.transform.scale(background_image, current_resolution), (0, 0))


def checking_fullscreen():
    if current_resolution == (1920, 1080):
        screen = pygame.display.set_mode(current_resolution, pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(current_resolution)


def Congrutulations(video_path):
    # Инициализация Pygame
    pygame.init()

    # Получение информации о видео
    cap = VideoCapture(video_path)
    if not cap.isOpened():
        print("Ошибка: Не удалось открыть видео.")
        return

    # Получение ширины и высоты видео
    width, height = int(cap.get(CAP_PROP_FRAME_WIDTH)), int(cap.get(CAP_PROP_FRAME_HEIGHT))

    # Создание окна Pygame
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Воспроизведение видео")

    fps_vid = int(cap.get(CAP_PROP_FPS)) or 30  # Установка FPS видео

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Чтение кадра из видео
        ret, frame = cap.read()
        if not ret:
            break  # Если кадры закончились, выходим из цикла

        # Преобразование цвета BGR в RGB
        frame = cvtColor(frame, COLOR_BGR2RGB)

        # Поворот изображения для корректного отображения в Pygame
        frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

        # Отображение кадра на экране
        screen.blit(frame, (0, 0))
        pygame.display.flip()

        clock.tick(fps_vid)

    # Освобождение ресурсов
    cap.release()

    # После завершения видео вызываем главное меню
    pygame.display.set_mode(current_resolution)
    main_menu()


def login_text():
    if entry:
        draw_text(f'Пользователь: {name_user}', small_font, WHITE, screen, 10, 10)
    else:
        draw_text('Вход не выполнен', small_font, WHITE, screen, 10, 10)


# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                       username TEXT PRIMARY KEY,
                       password TEXT,
                       enemies_killed INTEGER DEFAULT 0,
                       levels_completed INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()


# Функция для проверки существования пользователя
def user_exists(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    return user is not None


# Функция для добавления пользователя в базу данных
def add_user(username, password):
    if user_exists(username):  # Проверка на существование пользователя
        return False
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()
    return True


# Функция для проверки пользователя
def check_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None


# Функция для обновления количества убитых врагов
def update_enemies_killed(username, count):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("UPDATE users SET enemies_killed = enemies_killed + ? WHERE username=?", (count, username))
    conn.commit()
    conn.close()


# Функция для обновления количества пройденных уровней
def update_levels_completed(username, count):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("UPDATE users SET levels_completed = levels_completed + ? WHERE username=?", (count, username))
    conn.commit()
    conn.close()


# Функция для получения статистики пользователя
def get_user_kills(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT enemies_killed FROM users WHERE username=?", (username,))
    kill = c.fetchone()
    conn.close()
    return kill if kill else (0,)  # Возвращаем (0, 0), если пользователь не найден


def get_user_lvl(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT levels_completed FROM users WHERE username=?", (username,))
    lvl = c.fetchone()
    conn.close()
    return lvl if lvl else (0,)  # Возвращаем (0, 0), если пользователь не найден


# Функция для отображения текста на экране
def draw_text(text, fonts, color, surface, x, y):
    textobj = fonts.render(text, True, color)
    surface.blit(textobj, (x, y))


# Функция для регистрации пользователя
def registration_menu():
    username = ""
    password = ""
    input_active = "username"  # Переменная для отслеживания активного поля
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if add_user(username, password):
                        login_menu()  # Переключение на экран входа после успешной регистрации
                    else:
                        print("Пользователь с таким именем уже существует.")  # Можно добавить отображение на экране
                elif event.key == pygame.K_BACKSPACE:
                    if input_active == "username" and len(username) > 0:
                        username = username[:-1]
                    elif input_active == "password" and len(password) > 0:
                        password = password[:-1]
                elif event.key == pygame.K_TAB:  # Переключение между полями
                    input_active = "password" if input_active == "username" else "username"
                elif event.key == pygame.K_ESCAPE:  # Выход из выбора уровня
                    login_menu()
                else:
                    if input_active == "username":
                        username += event.unicode
                    elif input_active == "password":
                        password += event.unicode
        # Отображение фона
        screen.fill(WHITE)

        # Отображение текста
        draw_text("Регистрация", font, DARK_GRAY, screen, WIDTH // 2 - 150, HEIGHT // 2 - 100)
        draw_text("Имя пользователя: " + username, small_font, DARK_GRAY, screen, WIDTH // 2 - 150, HEIGHT // 2 - 40)
        draw_text("Пароль: " + "*" * len(password), small_font, DARK_GRAY, screen, WIDTH // 2 - 150, HEIGHT // 2)
        # Кнопка "Назад"
        draw_text("Назад", small_font, DARK_GRAY, screen, WIDTH // 2 - 40, HEIGHT // 2 + 40)

        # Подсветка активного поля
        if input_active == "username":
            draw_text("←", small_font, DARK_GRAY, screen, WIDTH // 2 - 160, HEIGHT // 2 - 40)
        else:
            draw_text("←", small_font, DARK_GRAY, screen, WIDTH // 2 - 160, HEIGHT // 2)

        pygame.display.flip()


# Функция для входа пользователя
def login_menu():
    global name_user, entry
    username = ""
    password = ""
    input_active = "username"  # Переменная для отслеживания активного поля
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if check_user(username, password):
                        name_user = username
                        entry = True
                        main_menu()
                    else:
                        print("Неверное имя пользователя или пароль.")  # Можно добавить отображение на экране
                elif event.key == pygame.K_BACKSPACE:
                    if input_active == "username" and len(username) > 0:
                        username = username[:-1]
                    elif input_active == "password" and len(password) > 0:
                        password = password[:-1]
                elif event.key == pygame.K_TAB:  # Переключение между полями
                    input_active = "password" if input_active == "username" else "username"
                elif event.key == pygame.K_r:  # Клавиша 'R' для перехода к регистрации
                    registration_menu()
                elif event.key == pygame.K_ESCAPE:  # Выход из выбора уровня
                    main_menu()

                else:
                    if input_active == "username":
                        username += event.unicode
                    elif input_active == "password":
                        password += event.unicode

        # Отображение фона
        screen.fill(WHITE)

        # Отображение текста
        draw_text("Вход", font, DARK_GRAY, screen, WIDTH // 2 - 50, HEIGHT // 2 - 100)
        draw_text("Имя пользователя: " + username, small_font, DARK_GRAY, screen, WIDTH // 2 - 150, HEIGHT // 2 - 40)
        draw_text("Пароль: " + "*" * len(password), small_font, DARK_GRAY, screen, WIDTH // 2 - 150, HEIGHT // 2)
        # Кнопка "Назад"
        draw_text("Назад", small_font, DARK_GRAY, screen, WIDTH // 2 - 40, HEIGHT // 2 + 90)
        draw_text("Нажмите 'R' для регистрации", small_font, DARK_GRAY, screen, WIDTH // 2 - 180, HEIGHT // 2 + 40)

        # Подсветка активного поля
        if input_active == "username":
            draw_text("←", small_font, DARK_GRAY, screen, WIDTH // 2 - 160, HEIGHT // 2 - 40)
        else:
            draw_text("←", small_font, DARK_GRAY, screen, WIDTH // 2 - 160, HEIGHT // 2)

        pygame.display.flip()


# Главная функция меню
def main_menu():
    global current_resolution, screen
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Отображение фонового изображения
        screen_back_ground()

        # Фон кнопок и заголовка
        surf = pygame.Surface((330, 400))
        surf.fill(DARK_GRAY)
        surf.set_alpha(200)
        grey_rect = screen.blit(surf, (WIDTH // 2 - 162, HEIGHT // 2 - 165))
        surf2 = pygame.Surface((WIDTH, 70))
        surf2.fill(DARK_GRAY)
        surf2.set_alpha(200)
        screen.blit(surf2, (0, 0))

        # Отображение заголовка
        draw_text('Деревяшки', font, WHITE, screen, grey_rect.x + 15, grey_rect.y + 10)

        # Создание кнопок
        sign_in_button = screen.blit(button_r_image, (WIDTH - 190, 5))
        start_button = screen.blit(button_image, (grey_rect.x + 12, grey_rect.y + 93))
        continue_button = screen.blit(button_image, (grey_rect.x + 12, grey_rect.y + 163))
        settings_button = screen.blit(button_image, (grey_rect.x + 12, grey_rect.y + 233))
        exit_button = screen.blit(button_image, (grey_rect.x + 12, grey_rect.y + 303))
        draw_text('Новая игра', small_font, DIRTY_WHITE, screen, start_button.x + 40, start_button.y + 13)
        draw_text('Продолжить', small_font, DIRTY_WHITE, screen, continue_button.x + 32, continue_button.y + 13)
        draw_text('Настройки', small_font, DIRTY_WHITE, screen, settings_button.x + 45, settings_button.y + 13)
        draw_text('Выход', small_font, DIRTY_WHITE, screen, exit_button.x + 65, exit_button.y + 13)
        draw_text('Войти', small_font, DIRTY_WHITE, screen, sign_in_button.x + 83, sign_in_button.y + 9)
        login_text()
        # Обработка нажатий кнопок и их изменение
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if start_button.collidepoint(mouse_pos):
            screen.blit(new_button_image, (start_button.x, start_button.y))
            draw_text('Новая игра', small_font, DIRTY_WHITE, screen, start_button.x + 40, start_button.y + 13)
            if mouse_click[0]:
                level_selection_menu()
                # Вызов функции игры
        elif continue_button.collidepoint(mouse_pos):
            screen.blit(next_button_image, (continue_button.x, continue_button.y))
            draw_text('Продолжить', small_font, DIRTY_WHITE, screen, continue_button.x + 32, continue_button.y + 13)
            if mouse_click[0]:
                continue_game()  # Вызов функции продолжения игры
        elif settings_button.collidepoint(mouse_pos):
            screen.blit(settings_button_image, (settings_button.x, settings_button.y))
            draw_text('Настройки', small_font, DIRTY_WHITE, screen, settings_button.x + 45, settings_button.y + 13)
            if mouse_click[0]:
                settings_menu()  # Вызов функции настроек
        elif sign_in_button.collidepoint(mouse_pos):
            screen.blit(sign_in_button_image, (sign_in_button.x, sign_in_button.y))
            draw_text('Войти', small_font, DIRTY_WHITE, screen, sign_in_button.x + 83, sign_in_button.y + 9)
            if mouse_click[0]:
                login_menu()
        elif exit_button.collidepoint(mouse_pos):
            screen.blit(exit_button_image, (exit_button.x, exit_button.y))
            draw_text('Выход', small_font, DIRTY_WHITE, screen, exit_button.x + 65, exit_button.y + 13)
            if mouse_click[0]:
                pygame.quit()
                sys.exit()  # Выход

        # Обновление экрана
        pygame.display.flip()


platforms = []

# Переменная для смещения экрана
camera_offset_x = 0
camera_offset_y = 0


# Функция выбора уровня

def level_selection_menu():
    levels = [
        {"image": level_one_image, "alt": level_one_alt_image, "pos": (WIDTH // 2 - 220, HEIGHT // 2 - 100),
         "action": level_one},
        {"image": level_two_image, "alt": level_two_alt_image, "pos": (WIDTH // 2, HEIGHT // 2 - 100),
         "action": level_two}
    ]

    while True:
        screen_back_ground()
        draw_text("Выберите уровень", font, WHITE, screen, WIDTH // 2 - 200, HEIGHT // 2 - 300)
        draw_text("Нажмите Esc для выхода", small_font, WHITE, screen, WIDTH // 2 - 200, HEIGHT - 50)

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                main_menu()

        for level in levels:
            rect = screen.blit(level["image"], level["pos"])
            if rect.collidepoint(mouse_pos):
                screen.blit(level["alt"], level["pos"])
                if mouse_click:
                    level["action"]()

        pygame.display.flip()


def level_one():
    # Координаты платформ
    plat_co_1 = [[50, HEIGHT - 100, 200, 20],
                 [350, HEIGHT - 200, 200, 20],
                 [825, HEIGHT - 300, 200, 20],
                 [250, HEIGHT - 425, 200, 20],
                 [50, HEIGHT - 310, 200, 20],
                 [450, HEIGHT - 300, 200, 20],
                 [650, HEIGHT - 100, 200, 20],
                 [400, HEIGHT - 500, 200, 20],
                 [1125, HEIGHT - 400, 200, 20],
                 [1250, HEIGHT - 175, 200, 20],
                 [1600, HEIGHT - 175, 200, 20],
                 [1800, HEIGHT - 300, 200, 20],
                 [1700, HEIGHT - 425, 200, 20],
                 [0, HEIGHT, 2000, 20],
                 [1400, HEIGHT - 450, 200, 20],
                 ]

    platforms.clear()
    # Создание платформ
    for p in plat_co_1:
        platforms.append(pygame.Rect(*p))
    # Создание двери
    door_rect_1 = pygame.Rect(plat_co_1[-1][0] + 50, plat_co_1[-1][1] - 100, 50, 100)

    # создание NPC
    enemies_1 = [
        Enemy(plat_co_1[0][0], plat_co_1[0][1] - 50, plat_co_1[0][0], plat_co_1[0][0] + 150, hp_enemy_pitch, speed_en),
        Enemy(plat_co_1[1][0], plat_co_1[1][1] - 50, plat_co_1[1][0], plat_co_1[1][0] + 150, hp_enemy_pitch, speed_en),
        Enemy(plat_co_1[2][0], plat_co_1[2][1] - 50, plat_co_1[2][0], plat_co_1[2][0] + 150, hp_enemy_pitch, speed_en),
        Enemy(plat_co_1[3][0], plat_co_1[3][1] - 50, plat_co_1[3][0], plat_co_1[3][0] + 150, hp_enemy_pitch, speed_en)]

    game_loop(plat_co_1, door_rect_1, enemies_1, platforms)


def level_two():
    # Координаты платформ
    plat_co_2 = [[50, HEIGHT - 100, 200, 20],
                 [350, HEIGHT - 200, 200, 20],
                 [650, HEIGHT - 300, 200, 20],
                 [50, HEIGHT - 310, 200, 20],
                 [250, HEIGHT - 450, 200, 20],
                 [900, HEIGHT - 300, 200, 20],
                 [600, HEIGHT - 400, 200, 20],
                 ]

    platforms.clear()
    # Создание платформ
    for p in plat_co_2:
        platforms.append(pygame.Rect(*p))
    # Создание двери
    door_rect_2 = pygame.Rect(WIDTH - 178, HEIGHT - 500, 50, 100)

    # создание NPC
    enemies_2 = [
        Enemy(plat_co_2[0][0], plat_co_2[0][1] - 50, plat_co_2[0][0], plat_co_2[0][0] + 150, hp_enemy_pitch, speed_en),
        Enemy(plat_co_2[1][0], plat_co_2[1][1] - 50, plat_co_2[1][0], plat_co_2[1][0] + 150, hp_enemy_pitch, speed_en)]

    game_loop(plat_co_2, door_rect_2, enemies_2, platforms)


# Основной игровой цикл
def game_loop(coord_platform, door, enemie, plats):
    global screen, camera_offset_x, camera_offset_y, hp_player, hp_enemy_pitch, all_sprites



    # Создание окна
    pygame.display.set_caption("Кубик красный")

    # Переменные игрока
    player_pos = [10, HEIGHT - 50]
    player_speed_y = 0
    on_ground = False
    direction = 1  # Направление игрока (1 - вправо, -1 - влево)
    # Список для пуль
    bullets = []
    zhmuriki = 0
    proshel_urovney = 0

    # Основной игровой цикл
    difficulty()
    count_frame = 0.1
    # Создаем два спрайта, но добавляем в группу только один (по умолчанию для движения вправо)
    player_r = AnimatedSprite(all_sprites, count_frame, lp_go_r_c_images, 4, 1, player_pos[0], player_pos[1])
    player_l = AnimatedSprite(all_sprites, count_frame, lp_go_l_c_images, 4, 1, player_pos[0], player_pos[1])
    current_player = player_r
    all_sprites.add(current_player)
    # player_stay = AnimatedSprite(all_sprites, count_frame, LPS_image, 1, 1, player_pos[0], player_pos[1])
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and on_ground:
                    player_speed_y = -16
                if event.key == pygame.K_RETURN:  # Стрельба по нажатию Enter
                    bullet = Bullet(player_pos[0] + (50 if direction == 1 else -10) + 5, player_pos[1] + 7, direction,
                                    BULLET_SPEED)
                    bullets.append(bullet)

        keys = pygame.key.get_pressed()
        # Если движение влево:
        if keys[pygame.K_LEFT]:
            player_pos[0] -= 5
            if direction != -1:
                direction = -1
                # Переключаем текущий спрайт на левый
                all_sprites.remove(current_player)
                current_player = player_l
                all_sprites.add(current_player)
            current_player.rect.topleft = (player_pos[0] - 10 - camera_offset_x, player_pos[1] - 30 - camera_offset_y)
            current_player.update()
        # Если движение вправо:
        elif keys[pygame.K_RIGHT]:
            player_pos[0] += 5
            if direction != 1:
                direction = 1
                # Переключаем текущий спрайт на правый
                all_sprites.remove(current_player)
                current_player = player_r
                all_sprites.add(current_player)
            current_player.rect.topleft = (player_pos[0] - 10 - camera_offset_x, player_pos[1] - 30 - camera_offset_y)
            current_player.update()


        # Проверка на границы экрана
        if player_pos[0] < 0:            player_pos[0] = 0
        if player_pos[0] > WIDTH + 2000: player_pos[0] = WIDTH + 2000
        if player_pos[1] < -100:         player_pos[1] = -100
        if player_pos[1] > HEIGHT:       player_pos[1] = HEIGHT

        # Гравитация
        player_speed_y += 1
        player_pos[1] += player_speed_y

        # Проверка на столкновение с платформами
        on_ground = False
        for platform in plats:
            if pygame.Rect(player_pos[0], player_pos[1], 50, 50).colliderect(platform):
                if platform.top <= player_pos[1] <= platform.top + 20:
                    player_pos[1] = platform.top + 20
                    player_speed_y = 0
                    break
                else:
                    player_pos[1] = platform.top - 50  # Если убрать, получится цикл для перемещения в слизи
                    on_ground = True
                    player_speed_y = 0
                    break

        # Проверка на землю
        if not on_ground and player_pos[1] >= HEIGHT - 50:
            player_pos[1] = HEIGHT - 50
            on_ground = True
            player_speed_y = 0

        # Обновление смещения камеры в зависимости от позиции игрока
        camera_offset_x = max(0, player_pos[0] - WIDTH // 2)
        camera_offset_y = max(0, player_pos[1] - HEIGHT // 2)

        # Отрисовка фона
        screen_back_ground()

        # Отрисовка платформ с учетом смещения экрана
        for platform in plats:
            adjusted_platform = platform.move(-camera_offset_x, -camera_offset_y)
            pygame.draw.rect(screen, GREEN, adjusted_platform)
            for pl in coord_platform:
                screen.blit(platform_image, (pl[0] - camera_offset_x, pl[1] - 13 - camera_offset_y))
        # Обновление и отрисовка NPC
        for enemy in enemie[:]:  # Используем срез для безопасного удаления элементов из списка во время итерации
            enemy.update()
            enemy.draw(screen, camera_offset_x, camera_offset_y, enemy_pitch_r_image, enemy_pitch_l_image, miles_font,
                       WHITE)

            # Проверка на столкновение с игроком
            if enemy.alive and pygame.Rect(player_pos[0], player_pos[1], 50, 50).colliderect(enemy.rect):
                hp_player -= damage_enemy_pitch
                player_pos[0] -= 17 * direction
                player_pos[1] -= 5 * direction
                print('Получен урон. HP:', hp_player)
                if hp_player <= 0:
                    print("Игрок умер!")
                    hp_player = 100
                    main_menu()
            # Обновление и отрисовка пуль
            for bullet in bullets[:]:
                bullet.update()
                bullet.draw(screen, camera_offset_x, camera_offset_y, arrow_r_image, arrow_l_image)

                # Проверка на столкновение с NPC
                for enemy in enemie[:]:
                    if bullet.alive and enemy.alive and bullet.rect.colliderect(enemy.rect):
                        bullet.alive = False
                        enemy.hp -= damage_player
                        print(enemy.hp)
                        if enemy.hp <= 0:
                            enemy.alive = False
                            zhmuriki += 1
                            update_enemies_killed(name_user, zhmuriki)

                        # Удаление пуль за пределами экрана
                if bullet.rect.x > WIDTH * 5:
                    bullet.alive = False

            bullets = [bullet for bullet in bullets if bullet.alive]  # Удаляем мертвые пули

        # Отрисовка двери
        screen.blit(exit_door_image, (door[0] - camera_offset_x, door[1] - camera_offset_y))

        # Проверка на столкновение с дверью
        if pygame.Rect(player_pos[0], player_pos[1], 50, 50).colliderect(door):
            proshel_urovney += 1
            update_levels_completed(name_user, proshel_urovney)
            print("Вы прошли через дверь! Игра окончена.")
            Congrutulations("sigmaboy1.mp4")
        # Отрисовка игрока с учетом смещения экрана
        player_rect = pygame.Rect(player_pos[0] - camera_offset_x, player_pos[1] - camera_offset_y, 50, 50)
        draw_text(f'{int(hp_player)}', miles_font, WHITE, screen, player_pos[0] + 10 - camera_offset_x,
                  player_pos[1] - 30 - camera_offset_y)

        # Если направление -1 (влево), сдвигаем прямоугольник влево
        # if direction == -1: player_rect.x -= 1
        # pygame.draw.rect(screen, "RED", player_rect)

        # Орисовка спрайтов
        current_player.rect.topleft = (player_pos[0] - 10 - camera_offset_x, player_pos[1] - 30 - camera_offset_y)
        current_player.update()
        all_sprites.draw(screen)

        clock.tick(FPS)
        pygame.display.flip()


# Функция для продолжения игры
def continue_game():
    global screen, camera_offset_x, camera_offset_y, bullets
    # Инициализация Pygame
    pygame.init()

    pygame.display.set_caption("Кубик красный")

    # Переменные игрока
    player_pos = [WIDTH // 2, HEIGHT - 200]
    player_speed_y = 0
    on_ground = False

    # Основной игровой цикл
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
        if player_pos[0] > WIDTH + 600:
            player_pos[0] = WIDTH + 600
        if player_pos[1] < 0:
            player_pos[1] = 0
        if player_pos[1] > HEIGHT - 50:
            player_pos[0] = HEIGHT - 50

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
        if not on_ground and player_pos[1] >= HEIGHT - 78:
            player_pos[1] = HEIGHT - 78
            on_ground = True
            player_speed_y = 0

        # Обновление смещения камеры в зависимости от позиции игрока

        camera_offset_x = max(0, player_pos[0] - WIDTH // 2 + 25)  # +25 для центрирования игрока
        camera_offset_y = max(0, player_pos[1] - HEIGHT // 2)

        # Отрисовка
        screen_back_ground()

        # Отрисовка платформ с учетом смещения экрана
        for platform in platforms:
            adjusted_platform = platform.move(-camera_offset_x, -camera_offset_y)
            pygame.draw.rect(screen, GREEN, adjusted_platform)
        # Обновление и отрисовка NPC
        for enemy in enemies[:]:  # Используем срез для безопасного удаления элементов из списка во время итерации
            enemy.update()
            enemy.draw(screen, camera_offset_x, camera_offset_y)

            # Проверка на столкновение с игроком
            if enemy.alive and pygame.Rect(player_pos[0], player_pos[1], 50, 50).colliderect(enemy.rect):
                if player_speed_y > 0 and player_pos[1] + 50 <= enemy.rect.y:
                    # Игрок прыгает на NPC
                    enemy.alive = False  # Устанавливаем NPC как "мертвый"
                else:
                    # Игрок сталкивается с NPC и умирает (можно добавить логику смерти)
                    print("Игрок умер!")
                    # pygame.quit()
                    # sys.exit()
                # Обновление и отрисовка пуль
            for bullet in bullets[:]:
                bullet.update()
                bullet.draw(screen, camera_offset_x, camera_offset_y)

                # Проверка на столкновение с NPC
                for enemy in enemies[:]:
                    if bullet.alive and enemy.alive and bullet.rect.colliderect(enemy.rect):
                        bullet.alive = False
                        enemy.alive = False

                        # Удаление пуль за пределами экрана
                if bullet.rect.x > WIDTH:
                    bullet.alive = False

            bullets = [bullet for bullet in bullets if bullet.alive]  # Удаляем мертвые пули

        # Отрисовка двери
        door_exit = screen.blit(exit_door_image, (WIDTH - 200 - camera_offset_x, HEIGHT - 530 - camera_offset_y))

        # Проверка на столкновение с дверью
        if pygame.Rect(player_pos[0], player_pos[1], 50, 50).colliderect(door_exit):
            print("Вы прошли через дверь! Игра окончена.")
            main_menu()

        # Отрисовка игрока с учетом смещения экрана
        pygame.draw.rect(screen, RED, (player_pos[0] - camera_offset_x, player_pos[1] - camera_offset_y, 50, 50))

        # Орисовка спрайтов
        all_sprites.update()
        all_sprites.draw(screen)

        clock.tick(FPS)
        pygame.display.flip()


# Функция для настроек

def settings_menu():
    global current_resolution, screen, WIDTH, HEIGHT, current_difficulty

    resolutions = [(1920, 1080), (1280, 720), (1024, 768), (800, 600)]
    resolution = [f'{res[0]}x{res[1]}' for res in resolutions]
    difficulty_levels = ['Большой детина', 'Идеальный баланс', 'Суровая реальность']
    difficulty_menu = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(options_list=difficulty_levels,
                                                                           starting_option=difficulty_levels[0],
                                                                           relative_rect=pygame.Rect((330, 100),
                                                                                                     (200, 50)),
                                                                           manager=manager)

    screen_resolution = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(options_list=resolution,
                                                                             starting_option=resolution[-1],
                                                                             relative_rect=pygame.Rect((330, 175),
                                                                                                       (200, 50)),
                                                                             manager=manager)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    if event.ui_element == difficulty_menu:
                        current_difficulty = event.text
                        difficulty()
                        print('diff:', current_difficulty)
                    if event.ui_element == screen_resolution:
                        z = event.text
                        m = z.split('x')
                        current_resolution = WIDTH, HEIGHT = int(m[0]), int(m[1])
                        # Установка режима отображения
                        checking_fullscreen()

                        print('res:', event.text)

            manager.process_events(event)
        manager.update(clock.tick(FPS))

        # Отображение фона меню настроек
        screen_back_ground()

        surf3 = pygame.Surface((260, HEIGHT))
        surf3.fill(DARK_GRAY)
        surf3.set_alpha(200)
        screen.blit(surf3, (WIDTH - 260, 75))

        # Заголовок настроек
        draw_text('Настройки:', font, WHITE, screen, WIDTH // 2 - 150, 20)

        # Уровень сложности
        draw_text('Уровень сложности:', small_font, WHITE, screen, 20, 100)
        draw_text('Разрешение экрана:', small_font, WHITE, screen, 20, 175)
        draw_text('Статистика:', small_font, WHITE, screen, WIDTH - 250, 80)
        draw_text('Врагов убито:', miles_font, WHITE, screen, WIDTH - 250, 130)
        draw_text(str(get_user_kills(name_user))[1:-2], miles_font, WHITE, screen, WIDTH - 100, 130)
        draw_text('Уровней пройдено:', miles_font, WHITE, screen, WIDTH - 250, 180)
        draw_text(str(get_user_lvl(name_user))[1:2], miles_font, WHITE, screen, WIDTH - 60, 180)

        back_button = screen.blit(back_button_image, (10, HEIGHT - 70))
        draw_text('Назад', small_font, DIRTY_WHITE, screen, back_button.x + 100, back_button.y + 5)

        manager.draw_ui(screen)
        # Обработка нажатий
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if back_button.collidepoint(mouse_pos):
            if mouse_click[0]:
                main_menu()

        # Обновление экрана
        clock.tick(FPS)
        pygame.display.flip()


init_db()
# Запуск
if __name__ == "__main__":
    main_menu()
