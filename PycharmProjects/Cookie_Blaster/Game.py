import pygame
import sys
from pygame.sprite import Group
from controls import events, update, create_cookies, create_cookie_crumbs
from blaster import Gun
import menu
from moviepy.editor import VideoFileClip
from donut_boss import DonutBoss


def play_intro_with_sound():
    FPS = 360
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()

    clip = VideoFileClip('image/INTRO100.mp4')  # Замените "intro_video.mp4" на ваше имя видеофайла
    clip = clip.resize((1000, 1000))  # Масштабирование видео до размера экрана

    pygame.mixer.quit()  # Отключение встроенного звука Pygame
    clip.preview()  # Воспроизведение видео с звуком с помощью moviepy
    clock.tick(FPS)


def run():
    FPS = 120
    clock = pygame.time.Clock()

    # Уровень
    level = 1
    max_cookies = 1
    cookie_speed = 0.8

    pygame.init()
    screen = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption('Cookies')

    boss = DonutBoss(screen, 3)  # скорость босса
    bosses = Group()
    bosses.add(boss)

    boss_speed = 0.8
    boss_level = 3  # Уровень, на котором появляется босс
    boss_appeared = False

    score = 0
    game_over = False
    lives = 3
    play_intro_with_sound()

    while True:
        if menu.show_menu(screen):
            score = 0
            game_over = False
            lives = 3
            bosses = pygame.sprite.Group()
            level = 1
            gun = Gun(screen)
            bullets = Group()
            cookies = create_cookies(screen, max_cookies, cookie_speed)

            cookie_crumbs = Group()
            background = pygame.image.load('image/background-mount.png').convert()

            # Обновление уровней
            while True:
                screen.blit(background, (0, 0))

                events(screen, gun, bullets, cookies, cookie_crumbs)
                gun.update()
                update(screen, gun, cookies, bullets, cookie_crumbs, bosses)
                clock.tick(FPS)
                cookie_crumbs.empty()

                if len(cookies) == 0:
                    level += 1
                    cookie_speed += 0.2
                    max_cookies += 1
                    cookies = create_cookies(screen, max_cookies, cookie_speed)
                    # Создание босса на каждом пятом уровне
                    if level % boss_level == 0 and not boss_appeared:
                        boss = DonutBoss(screen, boss_speed)
                        bosses.add(boss)
                        boss_appeared = True
                    elif level % boss_level !=0:
                        boss_appeared = False
                if gun.lives <= 0:
                    break

            gun.lives = 3  # Сбросить жизни
            gun.rect.y = screen.get_height() - 160  # Вернуть бластер на место
            bullets.empty()  # Очистить пули
            cookies.empty()  # Очистить печеньки
            cookie_crumbs.empty()  # Очистить крошки печенья

        else:
            break

    pygame.quit()


run()
