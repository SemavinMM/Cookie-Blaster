import pygame
from pygame.sprite import Sprite
import random

WIDTH = 160
HEIGHT = 160


class DonutBoss(Sprite):
    def __init__(self, screen, speed):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load('image/donut.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen.get_width() - self.rect.width)  # Случайное горизонтальное положение
        self.rect.top = -self.rect.height  # Начинается за пределами экрана сверху
        self.speed = speed
        self.direction = pygame.math.Vector2(random.choice([-1, 1]), 1)  # Случайное начальное направление
        self.velocity = pygame.math.Vector2(speed * self.direction.x, speed * self.direction.y)
        self.acceleration = pygame.math.Vector2(0, 0.01)  # Исправлено: изменен вектор ускорения
        self.max_speed = 1  # Максимальная горизонтальная скорость
        self.mask = pygame.mask.from_surface(self.image)
        self.health = 10
        self.max_health = 10  # Максимальное значение здоровья
        self.health = self.max_health  # Значение текущего здоровья

        # Загружаем изображение для полоски здоровья
        self.health_bar = pygame.image.load('image/health_bar.png').convert_alpha()
        self.health_bar_width = self.health_bar.get_width()  # Ширина полоски здоровья
        self.health_bar_length = 160

    def update(self, gun_bottom):
        self.velocity += self.acceleration
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        if abs(self.velocity.x) > self.max_speed:
            self.velocity.x = self.max_speed * self.direction.x

        if self.rect.right >= self.screen.get_width() or self.rect.left <= 0:
            self.velocity.x *= -1

        if self.rect.bottom >= gun_bottom:
            self.rect.bottom = gun_bottom
            self.velocity.y *= -0.9
            self.velocity.x *= 0.9
        if self.health <= 0:  # Если здоровье босса меньше или равно нулю, удаляем его из группы
            self.kill()

    def draw(self):
        if self.health > 0:  # Рисуем босса только если его здоровье больше нуля
            self.screen.blit(self.image, self.rect)

    def draw_health_bar(self, screen):
        health_bar_width = int(self.health / self.max_health * self.health_bar_length)
        health_bar_surface = pygame.Surface((health_bar_width, 10))
        health_bar_surface.fill((255, 0, 0))
        screen.blit(health_bar_surface, (self.rect.x, self.rect.y - 10))

        screen.blit(self.health_bar, (self.rect.x + self.health_bar_width, self.rect.y - 10))
