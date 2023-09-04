import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, screen, gun):
        super().__init__()
        self.screen = screen
        self.image = pygame.Surface((12, 25))  # Здесь устанавливаем размеры изображения пули
        self.image.fill((204, 255, 0))  # Здесь заполняем изображение пули цветом
        self.rect = self.image.get_rect()
        self.rect.centerx = gun.rect.centerx
        self.rect.top = gun.rect.top
        self.speed = 7
        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.speed
        self.rect.y = self.y

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def check_collision(self, cookies):
        for cookie in cookies:
            if self.rect.colliderect(cookie.rect):
                return True
        return False
