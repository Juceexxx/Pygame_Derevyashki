import pygame


def draw_text(text, fonts, color, surface, x, y):
    textobj = fonts.render(text, True, color)
    surface.blit(textobj, (x, y))


class Enemy:
    def __init__(self, x, y, min_x, max_x, hp, speed_enemy):

        self.rect = pygame.Rect(x, y, 50, 50)
        self.speed = speed_enemy
        self.direction = 1  # 1 - вправо, -1 - влево
        self.min_x = min_x
        self.max_x = max_x
        self.hp = hp
        self.alive = True  # Добавляем состояние "живой"

    def update(self):
        # Движение NPC
        self.rect.x += self.speed * self.direction

        # Проверка на столкновение с границами платформы
        if self.rect.x <= self.min_x or self.rect.x >= self.max_x:  # Предполагаем, что платформа находится в пределах этих координат
            self.direction *= -1  # Меняем направление

    def draw(self, screen, camera_offset_x, camera_offset_y, enemy_pitch_r, enemy_pitch_l, front, color_front):
        if self.alive:  # Отрисовываем NPC только если он жив
            if self.direction == 1:
                screen.blit(pygame.transform.scale(enemy_pitch_r, (50, 50)), (
                    self.rect.x - camera_offset_x, self.rect.y - camera_offset_y, self.rect.width, self.rect.height))
            else:
                screen.blit(pygame.transform.scale(enemy_pitch_l, (50, 50)), (
                    self.rect.x - camera_offset_x, self.rect.y - camera_offset_y, self.rect.width, self.rect.height))
            draw_text(f'{int(self.hp)}', front, color_front, screen, self.rect.x + 10 - camera_offset_x,
                      self.rect.y - 30 - camera_offset_y)
