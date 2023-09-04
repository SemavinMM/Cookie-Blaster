import pygame

# BLASTER_WIDTH = 150
# BLASTER_HEIGHT = 150


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load('image/blaster_beta.png').convert_alpha()
        # self.image = pygame.transform.scale(self.image, (BLASTER_WIDTH, BLASTER_HEIGHT))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.center = float(self.rect.centerx)
        self.rect.bottom = self.screen_rect.bottom
        self.moving_right = False
        self.moving_left = False
        self.rect.y -= 190
        self.lives = 3

    def output(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += 5
        if self.moving_left and self.rect.left > 0:
            self.center -= 5
        self.rect.centerx = self.center

        if self.rect.bottom >= self.screen_rect.bottom:
            self.rect.bottom = self.screen_rect.bottom - 190  # Измените значение на нужную вам высоту

        self.rect.centerx = self.center