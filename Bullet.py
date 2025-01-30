import pygame


class Bullet:
    def __init__(self, x, y, direction, BULLET_SPEED):
        self.BULLET_SPEED = BULLET_SPEED
        self.rect = pygame.Rect(x, y, 10, 5)
        self.alive = True
        self.direction = direction  # Направление пули (1 - вправо, -1 - влево)

    def update(self):
        if self.alive:
            self.rect.x += self.BULLET_SPEED * self.direction  # Умножаем скорость на направление

    def draw(self, screen, camera_offset_x, camera_offset_y, arrow_r, arrow_l):
        if self.alive:
            if self.direction == 1:
                screen.blit(pygame.transform.scale(arrow_r, (10, 5)), (
                    self.rect.x - camera_offset_x, self.rect.y - camera_offset_y, self.rect.width, self.rect.height))
            else:
                screen.blit(pygame.transform.scale(arrow_l, (10, 5)), (
                    self.rect.x - camera_offset_x, self.rect.y - camera_offset_y, self.rect.width, self.rect.height))