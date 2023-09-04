import pygame
import sys
from bullets import Bullet
from pygame.sprite import Sprite, Group
from cookies import Cookie, CookieCrumb
import random
import menu

pygame.font.init()
font_path = 'Font/EightBits.ttf'
score_font = pygame.font.Font(font_path, 50)
lives_font = pygame.font.Font(font_path, 50)
game_over_font = pygame.font.Font(font_path, 72)
boss_text_font = pygame.font.Font(font_path, 50)
score = 0
cookie_crumbs = Group()
game_over = False
lives = 3


def events(screen, gun, bullets, cookies, cookie_crumbs):
    global game_over
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                gun.moving_right = True
            elif event.key == pygame.K_a:
                gun.moving_left = True
            elif event.key == pygame.K_SPACE:
                new_bullet = Bullet(screen, gun)
                bullets.add(new_bullet)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                gun.moving_right = False
            elif event.key == pygame.K_a:
                gun.moving_left = False

    if game_over:
        return


def update(screen, gun, cookies, bullets, cookie_crumbs, bosses):
    global score
    global game_over
    global lives

    background = pygame.image.load('image/background-mount.png').convert()
    screen.blit(background, (0, 0))
    cookies.update(screen, gun.rect.bottom)

    for bullet in bullets.sprites():
        bullet.draw()

    gun.output()
    cookies.draw(screen)

    bullets.update()

    # Обновление движения босса
    for boss in bosses.sprites():
        boss.update(gun.rect.bottom)  # Передаем позицию нижней части бластера в метод обновления босса
        boss.draw()

        boss_hits = pygame.sprite.groupcollide(bosses, bullets, False, True)
        if boss_hits:
            for boss in boss_hits:
                boss.health -= len(boss_hits[boss])
                if boss.health <= 0:
                    bosses.remove(boss)  # Удалить босса из группы, если его здоровье меньше или равно 0
                    if boss.health <= 0:
                        bosses.remove(boss)  # Удалить босса из группы, если его здоровье меньше или равно 0
                        # Увеличение счета за убийство босса
                        score += 20
                    # Дополнительные действия, которые нужно сделать при победе над боссом


    # Проверка столкновений босса с пулями
    boss_hits = pygame.sprite.groupcollide(bosses, bullets, False, True)
    if boss_hits:
        for boss in boss_hits:
            boss.health -= len(boss_hits[boss])

    # Проверка столкновения босса с бластером
    if pygame.sprite.spritecollide(gun, bosses, False):
        gun.lives -= 2

    for boss in bosses.sprites():
        boss.update(gun.rect.bottom)  # Передаем позицию нижней части бластера в метод обновления босса
        boss.draw()
        boss.draw_health_bar(screen)

    # Проверка столкновений пуль с печеньками
    collisions = pygame.sprite.groupcollide(cookies, bullets, True, True)
    if collisions:
        for cookies in collisions.values():
            # Увеличение счета за каждую сбитую печеньку
            score += len(cookies)

    # Проверка столкновения печеньки с бластером
    for cookie in cookies:
        if pygame.sprite.collide_mask(cookie, gun):
            lives -= 1
            if lives <= 0:
                game_over = True
            else:
                reset_game(screen, gun, bullets, cookies, cookie_crumbs, bosses)

    score_text = score_font.render("Score: " + str(score), True, (238, 0, 0))
    screen.blit(score_text, (10, 10))

    lives_text = lives_font.render("Lives: " + str(lives), True, (238, 0, 0))
    screen.blit(lives_text, (855, 10))

    if game_over:
        game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (screen.get_width() // 2 - game_over_text.get_width() // 2,
                                     screen.get_height() // 2 - game_over_text.get_height() // 2))
        pygame.display.flip()  #

        pygame.time.delay(2000)

        if lives == 0:
            score = 0
            lives = 3
            game_over = False
            menu.show_menu(screen)
            return

    pygame.display.flip()


def reset_game(screen, gun, bullets, cookies, cookie_crumbs, bosses):
    gun.rect.centerx = screen.get_rect().centerx
    gun.rect.bottom = screen.get_rect().bottom
    bosses.empty()
    bullets.empty()
    cookies.empty()
    cookie_crumbs.empty()
    pygame.time.delay(1000)


def update_bullets(bullets, cookies, screen):
    bullets.update()
    cookies_to_remove = []  # Список для хранения печенек, которые нужно удалить
    for bullet in bullets.sprites():
        if bullet.rect.bottom <= 0 or bullet.check_collision(cookies):
            cookies_to_remove.append(bullet.check_collision(cookies))  # Добавляем печеньку для удаления
            bullets.remove(bullet)
    for cookie in cookies_to_remove:
        cookies.remove(cookie)  # Удаляем печеньки

    for cookie in cookies_to_remove:
        cookies.remove(cookie)
        cookie_crumb = CookieCrumb(screen, cookie.rect.center)
        cookie_crumbs.add(cookie_crumb)


def create_cookies(screen, num_cookies, speed):
    cookies = pygame.sprite.Group()

    for i in range(num_cookies):
        x = random.randint(0, screen.get_width())
        y = -random.randint(50, 200)
        direction = (random.choice([-1, 1]), 1)
        cookie = Cookie(screen, (x, y), speed, direction)
        cookies.add(cookie)

    return cookies


def create_cookie_crumbs(screen, cookie_crumbs, cookies):
    for cookie in cookies:
        cookie_crumb = CookieCrumb(screen, cookie.rect.center)
        cookie_crumbs.add(cookie_crumb)
