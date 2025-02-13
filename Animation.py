import pygame


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, all_sprites, count_frame, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.count_frame = count_frame
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(-100, -100, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        if self.cur_frame > len(self.frames): self.cur_frame = 0
        self.cur_frame = (self.cur_frame + self.count_frame) % len(self.frames)
        self.image = self.frames[int(self.cur_frame)]
