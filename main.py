import pygame
import sys
import os
import sqlite3
import pygame_gui
import cv2

from Animation import AnimatedSprite
from Enemy import Enemy
from Bullet import Bullet

# Инициализация Pygame
pygame.init()

# Основные параметры
infoObject = pygame.display.Info()
WIDTH_1, HEIGHT_1 = infoObject.current_w, infoObject.current_h
current_resolution = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Forest Secrets")
all_sprites = pygame.sprite.Group()
manager = pygame_gui.UIManager(current_resolution)
clock = pygame.time.Clock()

# Константы
BLACK = 'black'
WHITE = (255, 255, 255)
DIRTY_WHITE = (215, 215, 215)
BROWN = (139, 69, 19)
DARK_GRAY = (128, 128, 128)
FPS = 60
BULLET_SPEED = 5
HP = 100
DAMAGE = 100

# Переменные по умолчанию
current_difficulty = 'Большой детина'
entry = False
name_user = ''
hp_player = 100
damage_player = 100
hp_en_pitch = 100
damage_enemy_pitch = 100
speed_en = 1
camera_offset_x = 0
camera_offset_y = 0
platforms = []
ex_level = 0

# Шрифты
font = pygame.font.Font('Data/Bitcell.ttf', 80)
small_font = pygame.font.Font('Data/Bitcell.ttf', 46)
miles_font = pygame.font.Font('Data/Bitcell.ttf', 30)
text_font = pygame.font.Font('Data/Bitcell.ttf', 28)


# Функция для отображения текста на экране
def draw_text(text, fonts, color, surface, x, y):
    text_object = fonts.render(text, True, color)
    surface.blit(text_object, (x, y))


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


button_image = load_image('Button.png')
button_image = pygame.transform.scale(button_image, (300, 70))
standard_button_image = load_image('Standard_Button.png')
standard_button_image = pygame.transform.scale(standard_button_image, (300, 70))
back_button_image = load_image('Back_Button.png')
back_button_image = pygame.transform.scale(back_button_image, (300, 70))
new_button_image = load_image('New_Button.png')
new_button_image = pygame.transform.scale(new_button_image, (300, 70))
settings_button_image = load_image('Settings_Button.png')
settings_button_image = pygame.transform.scale(settings_button_image, (300, 70))
exit_button_image = load_image('Exit_Button.png')
exit_button_image = pygame.transform.scale(exit_button_image, (300, 70))
next_button_image = load_image('Next_Button.png')
next_button_image = pygame.transform.scale(next_button_image, (300, 70))
button_r_image = load_image('Button_R.png')
button_r_image = pygame.transform.scale(button_r_image, (300, 70))
sign_in_button_image = load_image('Sign_In_Button.png')
sign_in_button_image = pygame.transform.scale(sign_in_button_image, (300, 70))
exit_door_image = load_image('Exit_Door.png')
exit_door_image = pygame.transform.scale(exit_door_image, (100, 130))
platform_image = load_image('Platform.png')
platform_image = pygame.transform.scale(platform_image, (200, 27))
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
grass_image = pygame.transform.scale(grass_image, (3000, 92))
lp_go_r_c_images = load_image('LP_Go_R_Crossbow.png')
lp_go_r_c_images = pygame.transform.scale(lp_go_r_c_images, (320, 80))
lp_go_l_c_images = load_image('LP_Go_L_Crossbow.png')
lp_go_l_c_images = pygame.transform.scale(lp_go_l_c_images, (320, 80))
lp_stay_r_c_image = load_image('LP_Stay_r_Crossbow.png')
lp_stay_r_c_image = pygame.transform.scale(lp_stay_r_c_image, (80, 80))
lp_stay_l_c_image = load_image('LP_Stay_l_Crossbow.png')
lp_stay_l_c_image = pygame.transform.scale(lp_stay_l_c_image, (80, 80))
lp_jump_c_r_image = load_image('LP_Crossbow_Jump_R.png')
lp_jump_c_r_image = pygame.transform.scale(lp_jump_c_r_image, (80, 80))
lp_jump_c_l_image = load_image('LP_Crossbow_Jump_L.png')
lp_jump_c_l_image = pygame.transform.scale(lp_jump_c_l_image, (80, 80))
background_image = load_image('background.png')
background_image = pygame.transform.scale(background_image, current_resolution)


# Параметры в зависимости от сложности
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


# Создание полупрозрачного фона
def surf(color, x, y, width, height):
    sur = pygame.Surface((width, height))
    sur.fill(color)
    sur.set_alpha(200)
    screen.blit(sur, (x, y))


# Изменение фона под разрешение экрана
def screen_back_ground():
    screen.blit(pygame.transform.scale(background_image, current_resolution), (0, 0))


# Проверка на полноэкранный режим
def checking_fullscreen():
    if current_resolution == (1920, 1080):
        pygame.display.set_mode(current_resolution, pygame.FULLSCREEN)
    else:
        pygame.display.set_mode(current_resolution)


# Конечное видео
def final_video(video_path):
    # Инициализация Pygame
    pygame.init()

    # Получение информации о видео
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Ошибка: Не удалось открыть видео.")
        return

    # Получение ширины и высоты видео
    width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Создание окна Pygame
    pygame.display.set_mode((width, height))
    pygame.display.set_caption("Воспроизведение видео")

    fps_vid = int(cap.get(cv2.CAP_PROP_FPS)) or 30  # Установка FPS видео

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
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

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
    all_sprites.empty()
    main_menu()


# Проверка на вход пользователя
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


# Функции для получения статистики пользователя
def get_user_kills(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT enemies_killed FROM users WHERE username=?", (username,))
    kill = c.fetchone()
    conn.close()
    return kill if kill else (0,)  # Возвращаем 0 если пользователь не найден


def get_user_lvl(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT levels_completed FROM users WHERE username=?", (username,))
    lvl = c.fetchone()
    conn.close()
    return lvl if lvl else (0,)  # Возвращаем 0, если пользователь не найден


# Функция для регистрации пользователя
def registration_menu():
    error = ''
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
                        error = 'Пользователь с таким именем уже существует!'
                        print("Пользователь с таким именем уже существует!")
                elif event.key == pygame.K_BACKSPACE:
                    if input_active == "username" and len(username) > 0:
                        username = username[:-1]
                    elif input_active == "password" and len(password) > 0:
                        password = password[:-1]
                elif event.key == pygame.K_TAB:  # Переключение между полями
                    input_active = "password" if input_active == "username" else "username"
                elif event.key == pygame.K_ESCAPE:
                    login_menu()
                else:
                    if input_active == "username":
                        username += event.unicode
                    elif input_active == "password":
                        password += event.unicode

        # Отображение фона
        screen_back_ground()

        # Обработка нажатий кнопок и их изменение
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # Кнопки
        username_button = pygame.Rect(40, HEIGHT // 2 - 90, 600, 40)
        password_button = pygame.Rect(40, HEIGHT // 2 - 45, 600, 40)
        back_button = screen.blit((pygame.transform.scale(button_r_image, (220, 60))), (WIDTH - 210, 0))

        # Создание затемнения
        surf(DARK_GRAY, 0, 150, WIDTH, HEIGHT // 2 - 100)
        surf(DARK_GRAY, 0, HEIGHT - 100, WIDTH, HEIGHT // 2)
        surf(DARK_GRAY, username_button.x - 5, username_button.y, username_button.w, username_button.h)
        surf(DARK_GRAY, password_button.x - 5, password_button.y, password_button.w, password_button.h)

        # Отображение текста
        if error == 'Пользователь с таким именем уже существует!':
            draw_text('Пользователь с таким именем уже существует!', small_font, WHITE, screen, password_button.x,
                      password_button.y + 40)
        draw_text('Для регистрации нажмите: "Enter"', small_font, WHITE, screen, WIDTH // 2 - 220, HEIGHT - 50)
        draw_text("Регистрация:", font, WHITE, screen, WIDTH // 2 - 170, HEIGHT // 2 - 155)
        draw_text('Имя пользователя: ' + username, small_font, WHITE, screen, username_button.x, username_button.y)
        draw_text('Пароль: ' + '*' * len(password), small_font, WHITE, screen, password_button.x, password_button.y)
        draw_text('Назад', small_font, DIRTY_WHITE, screen, back_button.x + 90, back_button.y + 7)
        if username_button.collidepoint(mouse_pos):
            if mouse_click[0]:
                if input_active == "password":
                    input_active = "username"
        if password_button.collidepoint(mouse_pos):
            if mouse_click[0]:
                if input_active == "username":
                    input_active = "password"
        if back_button.collidepoint(mouse_pos):
            screen.blit((pygame.transform.scale(back_button_image, (220, 60))), (back_button.x, back_button.y))
            draw_text('Назад', small_font, DIRTY_WHITE, screen, back_button.x + 90, back_button.y + 7)
            if mouse_click[0]:
                login_menu()

        # Подсветка активного поля
        if input_active == "username":
            draw_text("->", small_font, WHITE, screen, 5, HEIGHT // 2 - 90)
        else:
            draw_text("->", small_font, WHITE, screen, 5, HEIGHT // 2 - 45)

        clock.tick(FPS)
        pygame.display.flip()


# Функция для входа пользователя
def login_menu():
    global name_user, entry
    error = ''
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
                        error = "Неверное имя пользователя или пароль!"
                        print("Неверное имя пользователя или пароль!")
                elif event.key == pygame.K_BACKSPACE:
                    if input_active == "username" and len(username) > 0:
                        username = username[:-1]
                    elif input_active == "password" and len(password) > 0:
                        password = password[:-1]
                elif event.key == pygame.K_TAB:  # Переключение между полями
                    input_active = "password" if input_active == "username" else "username"
                elif event.key == pygame.K_ESCAPE:
                    main_menu()
                else:
                    if input_active == "username":
                        username += event.unicode
                    elif input_active == "password":
                        password += event.unicode

        # Отображение фона
        screen_back_ground()

        # Обработка нажатий кнопок и их изменение
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # Кнопки
        username_button = pygame.Rect(40, HEIGHT // 2 - 90, 600, 40)
        password_button = pygame.Rect(40, HEIGHT // 2 - 45, 600, 40)
        registration_button = screen.blit(button_image, (WIDTH - 300, 70))
        exin_in_menu_button = screen.blit(button_image, (10, 70))

        # Создание затемнения
        surf(DARK_GRAY, 0, 150, WIDTH, HEIGHT // 2 - 100)
        surf(DARK_GRAY, 0, HEIGHT - 100, WIDTH, HEIGHT // 2)
        surf(DARK_GRAY, username_button.x - 5, username_button.y, username_button.w, username_button.h)
        surf(DARK_GRAY, password_button.x - 5, password_button.y, password_button.w, password_button.h)

        # Отображение текста
        if error == 'Неверное имя пользователя или пароль!':
            draw_text('Неверное имя пользователя или пароль!', small_font, WHITE, screen, password_button.x,
                      password_button.y + 40)
        draw_text('Для входа нажмите: "Enter"', small_font, WHITE, screen, WIDTH // 2 - 200, HEIGHT - 50)
        draw_text('Вход', font, WHITE, screen, WIDTH // 2 - 60, HEIGHT // 2 - 155)
        draw_text('Имя пользователя: ' + username, small_font, WHITE, screen, username_button.x, username_button.y)
        draw_text('Пароль: ' + '*' * len(password), small_font, WHITE, screen, password_button.x, password_button.y)
        draw_text('Регистрация', small_font, DIRTY_WHITE, screen, registration_button.x + 22,
                  registration_button.y + 13)
        draw_text('Выход в меню', small_font, DIRTY_WHITE, screen, exin_in_menu_button.x + 10,
                  exin_in_menu_button.y + 13)

        if username_button.collidepoint(mouse_pos):
            if mouse_click[0]:
                if input_active == "password":
                    input_active = "username"
        if password_button.collidepoint(mouse_pos):
            if mouse_click[0]:
                if input_active == "username":
                    input_active = "password"
        if registration_button.collidepoint(mouse_pos):
            screen.blit(next_button_image, (registration_button.x, registration_button.y))
            draw_text('Регистрация ', small_font, DIRTY_WHITE, screen, registration_button.x + 22,
                      registration_button.y + 13)
            if mouse_click[0]:
                registration_menu()
        if exin_in_menu_button.collidepoint(mouse_pos):
            screen.blit(exit_button_image, (exin_in_menu_button.x, exin_in_menu_button.y))
            draw_text('Выход в меню', small_font, DIRTY_WHITE, screen, exin_in_menu_button.x + 10,
                      exin_in_menu_button.y + 13)
            if mouse_click[0]:
                main_menu()

        # Подсветка активного поля
        if input_active == "username":
            draw_text("->", small_font, WHITE, screen, 5, HEIGHT // 2 - 90)
        else:
            draw_text("->", small_font, WHITE, screen, 5, HEIGHT // 2 - 45)

        clock.tick(FPS)
        pygame.display.flip()


def hello_text_screen():
    global current_resolution, screen
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                main_menu()

        # Открытие текста
        hello_text = open("Data/Hello_text.txt", encoding="utf8")

        # Отображение фонового изображения
        screen_back_ground()

        # Создание затемнения
        surf('black', 0, 0, WIDTH, HEIGHT)

        # Текст
        draw_text('Нажмите любую клавишу, чтобы продолжить', small_font, WHITE, screen, 50, HEIGHT - 50)
        draw_text('Предыстория:', small_font, WHITE, screen, 300, 10)

        for i in range(9):
            draw_text(hello_text.readline(), text_font, WHITE, screen, 30, 50 + 30 * i)
        pygame.display.flip()
        hello_text.close()


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
        surf_k = pygame.Surface((330, 400))
        surf_k.fill(DARK_GRAY)
        surf_k.set_alpha(200)
        grey_rect = screen.blit(surf_k, (WIDTH // 2 - 162, HEIGHT // 2 - 165))
        surf(DARK_GRAY, 0, 0, WIDTH, 70)

        # Отображение заголовка
        draw_text('Forest Secrets', pygame.font.Font('Data/Bitcell.ttf', 68), WHITE, screen, grey_rect.x + 15, grey_rect.y + 10)

        # Создание кнопок
        sign_in_button = screen.blit((pygame.transform.scale(button_r_image, (200, 62))), (WIDTH - 190, 5))
        start_button = screen.blit(button_image, (grey_rect.x + 12, grey_rect.y + 93))
        continue_button = screen.blit(button_image, (grey_rect.x + 12, grey_rect.y + 163))
        settings_button = screen.blit(button_image, (grey_rect.x + 12, grey_rect.y + 233))
        exit_button = screen.blit(button_image, (grey_rect.x + 12, grey_rect.y + 303))
        draw_text('Новая игра', small_font, DIRTY_WHITE, screen, start_button.x + 40, start_button.y + 13)
        draw_text('Продолжить', small_font, DIRTY_WHITE, screen, continue_button.x + 32, continue_button.y + 13)
        draw_text('Настройки', small_font, DIRTY_WHITE, screen, settings_button.x + 45, settings_button.y + 13)
        draw_text('Выход', small_font, DIRTY_WHITE, screen, exit_button.x + 65, exit_button.y + 13)
        draw_text('Войти', small_font, DIRTY_WHITE, screen, sign_in_button.x + 83, sign_in_button.y + 9)
        draw_text('Alpha v1.0', miles_font, DIRTY_WHITE, screen, 10, HEIGHT - 30)
        login_text()
        # Обработка нажатий кнопок и их изменение
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if start_button.collidepoint(mouse_pos):
            screen.blit(new_button_image, (start_button.x, start_button.y))
            draw_text('Новая игра', small_font, DIRTY_WHITE, screen, start_button.x + 40, start_button.y + 13)
            if mouse_click[0]:
                continue_g = False
                level_selection_menu(continue_g)
        # Вызов функции игры
        elif continue_button.collidepoint(mouse_pos):
            screen.blit(next_button_image, (continue_button.x, continue_button.y))
            draw_text('Продолжить', small_font, DIRTY_WHITE, screen, continue_button.x + 32, continue_button.y + 13)
            if mouse_click[0]:
                continue_g = True
                if ex_level == 1:  # Вызов функции первого уровня
                    level_one(continue_g)
                elif ex_level == 2:  # Вызов функции второго уровня
                    level_two(continue_g)
        elif settings_button.collidepoint(mouse_pos):
            screen.blit(settings_button_image, (settings_button.x, settings_button.y))
            draw_text('Настройки', small_font, DIRTY_WHITE, screen, settings_button.x + 45, settings_button.y + 13)
            if mouse_click[0]:
                settings_menu()  # Вызов функции настроек
        elif sign_in_button.collidepoint(mouse_pos):
            screen.blit(pygame.transform.scale(sign_in_button_image, (200, 62)), (sign_in_button.x, sign_in_button.y))
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


# Функция выбора уровня
def level_selection_menu(continue_g):
    levels = [
        {"image": level_one_image, "alt": level_one_alt_image, "pos": (WIDTH // 2 - 220, HEIGHT // 2 - 100),
         "action": level_one},
        {"image": level_two_image, "alt": level_two_alt_image, "pos": (WIDTH // 2, HEIGHT // 2 - 100),
         "action": level_two}
    ]

    while True:
        screen_back_ground()
        draw_text("Выберите уровень", font, WHITE, screen, WIDTH // 2 - 225, HEIGHT // 2 - 300)
        draw_text('Нажмите "Esc" для выхода', small_font, WHITE, screen, WIDTH // 2 - 200, HEIGHT - 50)

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
                    level["action"](continue_g)
        pygame.display.flip()


def level_one(continue_g):
    global ex_level
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
                 [1400, HEIGHT - 450, 200, 20],
                 ]

    platforms.clear()
    # Создание платформ
    for p in plat_co_1:
        platforms.append(pygame.Rect(*p))
    # Создание двери
    door_rect_1 = pygame.Rect(plat_co_1[-1][0] + 50, plat_co_1[-1][1] - 130, 50, 100)

    # создание NPC
    enemies_1 = [
        Enemy(plat_co_1[0][0], plat_co_1[0][1] - 50, plat_co_1[0][0], plat_co_1[0][0] + 150, hp_en_pitch, speed_en),
        Enemy(plat_co_1[1][0], plat_co_1[1][1] - 50, plat_co_1[1][0], plat_co_1[1][0] + 150, hp_en_pitch, speed_en),
        Enemy(plat_co_1[2][0], plat_co_1[2][1] - 50, plat_co_1[2][0], plat_co_1[2][0] + 150, hp_en_pitch, speed_en),
        Enemy(plat_co_1[3][0], plat_co_1[3][1] - 50, plat_co_1[3][0], plat_co_1[3][0] + 150, hp_en_pitch, speed_en)]
    ex_level = 1
    if continue_g:
        continue_game(plat_co_1, door_rect_1, enemies_1, platforms)
    else:
        game_loop(plat_co_1, door_rect_1, enemies_1, platforms)


def level_two(continue_g):
    global ex_level
    # Координаты платформ
    plat_co_2 = [[50, HEIGHT - 100, 200, 20],
                 [350, HEIGHT - 200, 200, 20],
                 [500, HEIGHT - 100, 200, 20],
                 [70, HEIGHT - 100, 200, 20],
                 [650, HEIGHT - 300, 200, 20],
                 [50, HEIGHT - 310, 200, 20],
                 [250, HEIGHT - 450, 200, 20],
                 [950, HEIGHT - 300, 200, 20],
                 [600, HEIGHT - 400, 200, 20],
                 [1050, HEIGHT - 400, 200, 20],
                 [720, HEIGHT - 150, 200, 20],
                 [1050, HEIGHT - 150, 200, 20],
                 [1300, HEIGHT - 200, 200, 20],
                 [1350, HEIGHT - 350, 200, 20],
                 [1550, HEIGHT - 300, 200, 20],
                 [1850, HEIGHT - 250, 200, 20],
                 [1800, HEIGHT - 500, 200, 20],
                 [1550, HEIGHT - 450, 200, 20],
                 [1850, HEIGHT - 100, 200, 20],
                 [1600, HEIGHT - 100, 200, 20],
                 [1950, HEIGHT - 250, 200, 20]
                 ]
    platforms.clear()
    # Создание платформ
    for p in plat_co_2:
        platforms.append(pygame.Rect(*p))
    # Создание двери
    door_rect_2 = pygame.Rect(plat_co_2[-1][0] + 50, plat_co_2[-1][1] - 130, 50, 100)

    # создание NPC
    enemies_2 = [
        Enemy(plat_co_2[0][0], plat_co_2[0][1] - 50, plat_co_2[0][0], plat_co_2[0][0] + 150, hp_en_pitch, speed_en),
        Enemy(plat_co_2[1][0], plat_co_2[1][1] - 50, plat_co_2[1][0], plat_co_2[1][0] + 150, hp_en_pitch, speed_en),
        Enemy(plat_co_2[2][0], plat_co_2[2][1] - 50, plat_co_2[2][0], plat_co_2[2][0] + 150, hp_en_pitch, speed_en),
        Enemy(plat_co_2[4][0], plat_co_2[4][1] - 50, plat_co_2[4][0], plat_co_2[4][0] + 150, hp_en_pitch, speed_en),
        Enemy(plat_co_2[5][0], plat_co_2[5][1] - 50, plat_co_2[5][0], plat_co_2[5][0] + 150, hp_en_pitch, speed_en),
        Enemy(plat_co_2[8][0], plat_co_2[8][1] - 50, plat_co_2[8][0], plat_co_2[8][0] + 150, hp_en_pitch, speed_en),
        Enemy(plat_co_2[10][0], plat_co_2[10][1] - 50, plat_co_2[10][0], plat_co_2[10][0] + 150, hp_en_pitch, speed_en),
        Enemy(plat_co_2[12][0], plat_co_2[12][1] - 50, plat_co_2[12][0], plat_co_2[12][0] + 150, hp_en_pitch, speed_en),
        Enemy(plat_co_2[14][0], plat_co_2[14][1] - 50, plat_co_2[14][0], plat_co_2[14][0] + 150, hp_en_pitch, speed_en),
        Enemy(plat_co_2[13][0], plat_co_2[13][1] - 50, plat_co_2[13][0], plat_co_2[13][0] + 150, hp_en_pitch, speed_en),
        Enemy(plat_co_2[14][0], plat_co_2[14][1] - 50, plat_co_2[14][0], plat_co_2[14][0] + 150, hp_en_pitch, speed_en),
        Enemy(plat_co_2[16][0], plat_co_2[16][1] - 50, plat_co_2[16][0], plat_co_2[16][0] + 150, hp_en_pitch, speed_en),
        Enemy(plat_co_2[18][0], plat_co_2[18][1] - 50, plat_co_2[18][0], plat_co_2[18][0] + 150, hp_en_pitch, speed_en)
    ]

    ex_level = 2
    if continue_g:
        continue_game(plat_co_2, door_rect_2, enemies_2, platforms)
    else:
        game_loop(plat_co_2, door_rect_2, enemies_2, platforms)


# Функция паузы
def pause_game():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False

        # Обработка нажатий кнопок и их изменение
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # Отрисовка экрана паузы
        screen_back_ground()

        continue_button = screen.blit(button_image, (20, 150))
        exin_in_menu_button = screen.blit(button_image, (20, 250))
        exit_button = screen.blit(button_image, (20, 350))

        draw_text('Продолжить', small_font, DIRTY_WHITE, screen, continue_button.x + 32, continue_button.y + 13)
        draw_text('Выход', small_font, DIRTY_WHITE, screen, exit_button.x + 65, exit_button.y + 13)
        draw_text('Выход в меню', small_font, DIRTY_WHITE, screen, exin_in_menu_button.x + 10,
                  exin_in_menu_button.y + 13)
        draw_text("Игра на паузе", small_font, WHITE, screen, WIDTH // 2 - 100, 50)

        if continue_button.collidepoint(mouse_pos):
            screen.blit(next_button_image, (continue_button.x, continue_button.y))
            draw_text('Продолжить', small_font, DIRTY_WHITE, screen, continue_button.x + 32, continue_button.y + 13)
            if mouse_click[0]:
                paused = False
        if exin_in_menu_button.collidepoint(mouse_pos):
            screen.blit(exit_button_image, (exin_in_menu_button.x, exin_in_menu_button.y))
            draw_text('Выход в меню', small_font, DIRTY_WHITE, screen, exin_in_menu_button.x + 10,
                      exin_in_menu_button.y + 13)
            if mouse_click[0]:
                all_sprites.empty()
                main_menu()
        elif exit_button.collidepoint(mouse_pos):
            screen.blit(exit_button_image, (exit_button.x, exit_button.y))
            draw_text('Выход', small_font, DIRTY_WHITE, screen, exit_button.x + 65, exit_button.y + 13)
            if mouse_click[0]:
                pygame.quit()
                sys.exit()  # Выход
        pygame.display.flip()
        clock.tick(FPS)


# Основной игровой цикл
def game_loop(coord_platform, door, enemies, plats):
    global screen, camera_offset_x, camera_offset_y, hp_player, hp_en_pitch, all_sprites

    # Создание окна
    pygame.display.set_caption("Forest Secrets")

    # Переменные игрока
    player_pos = [10, HEIGHT - 50]
    player_speed_y = 0
    on_ground = False
    direction = 1  # Направление игрока (1 - вправо, -1 - влево)
    bullets_list = []  # Список для пуль
    completed_level = 0
    player_state = 'stand'

    # Основной игровой цикл
    difficulty()
    count_frame = 0.09
    animations = {
        'run_right': AnimatedSprite(all_sprites, count_frame, lp_go_r_c_images, 4, 1, player_pos[0], player_pos[1]),
        'run_left': AnimatedSprite(all_sprites, count_frame, lp_go_l_c_images, 4, 1, player_pos[0], player_pos[1]),
        'stand_right': AnimatedSprite(all_sprites, count_frame, lp_stay_r_c_image, 1, 1, player_pos[0], player_pos[1]),
        'stand_left': AnimatedSprite(all_sprites, count_frame, lp_stay_l_c_image, 1, 1, player_pos[0], player_pos[1]),
        'jump_right': AnimatedSprite(all_sprites, count_frame, lp_jump_c_r_image, 1, 1, player_pos[0], player_pos[1]),
        'jump_left': AnimatedSprite(all_sprites, count_frame, lp_jump_c_l_image, 1, 1, player_pos[0], player_pos[1])
    }
    current_player = animations['stand_right']
    all_sprites.add(current_player)

    # Обновление спрайта игрока в зависимости от состояния и направления
    def update_player_sprite(new_state, new_direction):
        nonlocal current_player, player_state, direction
        if player_state != new_state or direction != new_direction:
            all_sprites.remove(current_player)
            direction = new_direction
            player_state = new_state

            if new_state == 'jump':
                current_player = animations['jump_right'] if direction == 1 else animations['jump_left']
            elif new_state == 'run':
                current_player = animations['run_right'] if direction == 1 else animations['run_left']
            else:
                current_player = animations['stand_right'] if direction == 1 else animations['stand_left']

            all_sprites.add(current_player)

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
                    bullets_list.append(bullet)
                if event.key == pygame.K_ESCAPE:
                    pause_game()

        keys = pygame.key.get_pressed()
        # Если движение влево:
        if keys[pygame.K_LEFT]:
            player_pos[0] -= 5
            if on_ground:
                update_player_sprite('run', -1)
            else:
                update_player_sprite('jump', -1)
        elif keys[pygame.K_RIGHT]:
            player_pos[0] += 5
            if on_ground:
                update_player_sprite('run', 1)
            else:
                update_player_sprite('jump', 1)
        else:
            if on_ground:
                update_player_sprite('stand', direction)
            else:
                update_player_sprite('jump', direction)
        # Проверка на границы экрана
        player_pos[0] = max(0, min(player_pos[0], WIDTH + 2000))
        player_pos[1] = max(-100, min(player_pos[1], HEIGHT))

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
            platform.move(-camera_offset_x, -camera_offset_y)
            for pl in coord_platform:
                screen.blit(platform_image, (pl[0] - camera_offset_x, pl[1] - 8 - camera_offset_y))
        # Обновление и отрисовка NPC
        for enemy in enemies[:]:  # Используем срез для безопасного удаления элементов из списка во время итерации
            enemy.update()
            enemy.draw(screen, camera_offset_x, camera_offset_y, enemy_pitch_r_image, enemy_pitch_l_image, miles_font,
                       WHITE)

            # Проверка на столкновение с игроком
            if enemy.alive and pygame.Rect(player_pos[0], player_pos[1], 50, 50).colliderect(enemy.rect):
                hp_player -= damage_enemy_pitch
                player_pos[0] -= 17 * direction
                player_pos[1] -= 5 * direction
                if hp_player <= 0:
                    hp_player = 100
                    main_menu()
            # Обновление и отрисовка пуль
            for bullet in bullets_list[:]:
                bullet.update()
                bullet.draw(screen, camera_offset_x, camera_offset_y, arrow_r_image, arrow_l_image)

                # Проверка на столкновение с NPC
                for enemy in enemies[:]:
                    if bullet.alive and enemy.alive and bullet.rect.colliderect(enemy.rect):
                        bullet.alive = False
                        enemy.hp -= damage_player
                        if enemy.hp <= 0:
                            enemy.alive = False
                            update_enemies_killed(name_user, 1)

                        # Удаление пуль за пределами экрана
                if bullet.rect.x > WIDTH * 5:
                    bullet.alive = False

            bullets_list = [bullet for bullet in bullets_list if bullet.alive]  # Удаляем мертвые пули

        # Отрисовка двери
        screen.blit(exit_door_image, (door[0] - camera_offset_x, door[1] - camera_offset_y))
        screen.blit(grass_image, (- camera_offset_x, HEIGHT - 33 - camera_offset_y))

        # Проверка на столкновение с дверью
        if pygame.Rect(player_pos[0], player_pos[1], 50, 50).colliderect(door):
            completed_level += 1
            update_levels_completed(name_user, completed_level)
            final_video("sigmaboy1.mp4")

        # Отрисовка игрока с учетом смещения экрана
        pygame.Rect(player_pos[0] - camera_offset_x, player_pos[1] - camera_offset_y, 50, 50)

        draw_text(f'{int(hp_player)}', small_font, WHITE, screen, 10, 10)

        # Орисовка спрайтов
        current_player.rect.topleft = (player_pos[0] - 10 - camera_offset_x, player_pos[1] - 30 - camera_offset_y)
        all_sprites.update()
        all_sprites.draw(screen)

        clock.tick(FPS)
        pygame.display.flip()


# Функция для продолжения игры
def continue_game(coord_platform, door, enemies, plats):
    global screen, camera_offset_x, camera_offset_y, hp_player, hp_en_pitch, all_sprites

    # Создание окна
    pygame.display.set_caption("Forest Secrets")

    # Переменные игрока
    player_pos = [10, HEIGHT - 50]
    player_speed_y = 0
    on_ground = False
    direction = 1  # Направление игрока (1 - вправо, -1 - влево)
    bullets_list = []  # Список для пуль
    completed_level = 0
    player_state = 'stand'

    # Основной игровой цикл
    difficulty()
    count_frame = 0.09
    animations = {
        'run_right': AnimatedSprite(all_sprites, count_frame, lp_go_r_c_images, 4, 1, player_pos[0], player_pos[1]),
        'run_left': AnimatedSprite(all_sprites, count_frame, lp_go_l_c_images, 4, 1, player_pos[0], player_pos[1]),
        'stand_right': AnimatedSprite(all_sprites, count_frame, lp_stay_r_c_image, 1, 1, player_pos[0], player_pos[1]),
        'stand_left': AnimatedSprite(all_sprites, count_frame, lp_stay_l_c_image, 1, 1, player_pos[0], player_pos[1]),
        'jump_right': AnimatedSprite(all_sprites, count_frame, lp_jump_c_r_image, 1, 1, player_pos[0], player_pos[1]),
        'jump_left': AnimatedSprite(all_sprites, count_frame, lp_jump_c_l_image, 1, 1, player_pos[0], player_pos[1])
    }
    current_player = animations['stand_right']
    all_sprites.add(current_player)

    # Обновление спрайта игрока в зависимости от состояния и направления
    def update_player_sprite(new_state, new_direction):
        nonlocal current_player, player_state, direction
        if player_state != new_state or direction != new_direction:
            all_sprites.remove(current_player)
            direction = new_direction
            player_state = new_state

            if new_state == 'jump':
                current_player = animations['jump_right'] if direction == 1 else animations['jump_left']
            elif new_state == 'run':
                current_player = animations['run_right'] if direction == 1 else animations['run_left']
            else:
                current_player = animations['stand_right'] if direction == 1 else animations['stand_left']

            all_sprites.add(current_player)

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
                    bullets_list.append(bullet)
                if event.key == pygame.K_ESCAPE:
                    pause_game()

        keys = pygame.key.get_pressed()
        # Если движение влево:
        if keys[pygame.K_LEFT]:
            player_pos[0] -= 5
            if on_ground:
                update_player_sprite('run', -1)
            else:
                update_player_sprite('jump', -1)
        elif keys[pygame.K_RIGHT]:
            player_pos[0] += 5
            if on_ground:
                update_player_sprite('run', 1)
            else:
                update_player_sprite('jump', 1)
        else:
            if on_ground:
                update_player_sprite('stand', direction)
            else:
                update_player_sprite('jump', direction)
        # Проверка на границы экрана
        player_pos[0] = max(0, min(player_pos[0], WIDTH + 2000))
        player_pos[1] = max(-100, min(player_pos[1], HEIGHT))

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
            platform.move(-camera_offset_x, -camera_offset_y)
            for pl in coord_platform:
                screen.blit(platform_image, (pl[0] - camera_offset_x, pl[1] - 8 - camera_offset_y))
        # Обновление и отрисовка NPC
        for enemy in enemies[:]:  # Используем срез для безопасного удаления элементов из списка во время итерации
            enemy.update()
            enemy.draw(screen, camera_offset_x, camera_offset_y, enemy_pitch_r_image, enemy_pitch_l_image, miles_font,
                       WHITE)

            # Проверка на столкновение с игроком
            if enemy.alive and pygame.Rect(player_pos[0], player_pos[1], 50, 50).colliderect(enemy.rect):
                hp_player -= damage_enemy_pitch
                player_pos[0] -= 17 * direction
                player_pos[1] -= 5 * direction
                if hp_player <= 0:
                    hp_player = 100
                    main_menu()
            # Обновление и отрисовка пуль
            for bullet in bullets_list[:]:
                bullet.update()
                bullet.draw(screen, camera_offset_x, camera_offset_y, arrow_r_image, arrow_l_image)

                # Проверка на столкновение с NPC
                for enemy in enemies[:]:
                    if bullet.alive and enemy.alive and bullet.rect.colliderect(enemy.rect):
                        bullet.alive = False
                        enemy.hp -= damage_player
                        if enemy.hp <= 0:
                            enemy.alive = False
                            update_enemies_killed(name_user, 1)

                        # Удаление пуль за пределами экрана
                if bullet.rect.x > WIDTH * 5:
                    bullet.alive = False

            bullets_list = [bullet for bullet in bullets_list if bullet.alive]  # Удаляем мертвые пули

        # Отрисовка двери
        screen.blit(exit_door_image, (door[0] - camera_offset_x, door[1] - camera_offset_y))
        screen.blit(grass_image, (- camera_offset_x, HEIGHT - 33 - camera_offset_y))

        # Проверка на столкновение с дверью
        if pygame.Rect(player_pos[0], player_pos[1], 50, 50).colliderect(door):
            completed_level += 1
            update_levels_completed(name_user, completed_level)
            final_video("sigmaboy1.mp4")

        # Отрисовка игрока с учетом смещения экрана
        pygame.Rect(player_pos[0] - camera_offset_x, player_pos[1] - camera_offset_y, 50, 50)

        draw_text(f'{int(hp_player)}', small_font, WHITE, screen, 10, 10)

        # Орисовка спрайтов
        current_player.rect.topleft = (player_pos[0] - 10 - camera_offset_x, player_pos[1] - 30 - camera_offset_y)
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

        # Фон
        surf(DARK_GRAY, WIDTH - 260, 75, 260, HEIGHT)

        # Заголовок настроек
        draw_text('Настройки:', font, WHITE, screen, WIDTH // 2 - 150, 20)

        # Уровень сложности
        draw_text('Уровень сложности:', small_font, WHITE, screen, 20, 100)
        draw_text('Разрешение экрана:', small_font, WHITE, screen, 20, 175)
        draw_text('Статистика:', small_font, WHITE, screen, WIDTH - 250, 80)
        draw_text('Врагов убито:', miles_font, WHITE, screen, WIDTH - 250, 130)
        draw_text(str(*get_user_kills(name_user)), miles_font, WHITE, screen, WIDTH - 100, 130)
        draw_text('Уровней пройдено:', miles_font, WHITE, screen, WIDTH - 250, 180)
        draw_text(str(*get_user_lvl(name_user)), miles_font, WHITE, screen, WIDTH - 60, 180)

        back_button = screen.blit((pygame.transform.scale(button_r_image, (220, 60))), (10, HEIGHT - 70))
        draw_text('Назад', small_font, DIRTY_WHITE, screen, back_button.x + 90, back_button.y + 7)

        manager.draw_ui(screen)
        # Обработка нажатий
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if back_button.collidepoint(mouse_pos):
            screen.blit((pygame.transform.scale(back_button_image, (220, 60))), (back_button.x, back_button.y))
            draw_text('Назад', small_font, DIRTY_WHITE, screen, back_button.x + 90, back_button.y + 7)
            if mouse_click[0]:
                main_menu()

        # Обновление экрана
        clock.tick(FPS)
        pygame.display.flip()


init_db()
# Запуск
if __name__ == "__main__":
    hello_text_screen()
