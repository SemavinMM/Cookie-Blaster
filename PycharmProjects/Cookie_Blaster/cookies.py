import pygame
from pygame.sprite import Sprite
import random
WIDTH = 70
HEIGHT = 70


class Cookie(Sprite):
    def __init__(self, screen, position, speed, direction):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load('image/COOKIES2.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.speed = speed
        self.direction = pygame.math.Vector2(direction)
        self.velocity = pygame.math.Vector2(speed * direction[0], speed * direction[1])
        self.acceleration = pygame.math.Vector2(0, 0.1)  # Исправлено: изменен вектор ускорения
        self.max_speed = 1  # Максимальная горизонтальная скорость
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, screen, gun_bottom):
        self.velocity += self.acceleration
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        if abs(self.velocity.x) > self.max_speed:
            self.velocity.x = self.max_speed * self.direction.x

        if self.rect.right >= screen.get_width() or self.rect.left <= 0:
            self.velocity.x *= -1

        if self.rect.bottom >= gun_bottom:
            self.rect.bottom = gun_bottom
            self.velocity.y *= -0.9
            self.velocity.x *= 0.9

    def draw(self, screen):
        self.screen.blit(self.image, self.rect)


class CookieCrumb(Sprite):
    def __init__(self, screen, position):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load('image/cookie_crumb.png')
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.speed = 1  # Скорость падения крошки печенья

    def update(self):
        self.rect.y += self.speed

    def draw(self):
        self.screen.blit(self.image, self.rect)