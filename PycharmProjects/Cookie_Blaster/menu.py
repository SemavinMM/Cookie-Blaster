import pygame
import sys

pygame.font.init()
font_path = 'Font/EightBits.ttf'
title_font = pygame.font.Font(font_path, 100)
menu_font = pygame.font.Font(font_path, 55)


def show_menu(screen):
    title_text = pygame.image.load('image/header2.png')
    start_text = menu_font.render("Press Enter to Start", True, (255, 255, 255))
    quit_text = menu_font.render("Press Esc to Quit", True, (255, 255, 255))

    while True:
        menu_background = pygame.image.load('image/menu_background.png').convert()
        screen.blit(menu_background, (0, 0))
        screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 100))
        screen.blit(start_text, (screen.get_width() // 2 - start_text.get_width() // 2, 400))
        screen.blit(quit_text, (screen.get_width() // 2 - quit_text.get_width() // 2, 450))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    return False
