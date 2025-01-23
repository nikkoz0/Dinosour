import pygame
import sqlite3

from Base_func import WIDTH, HEIGHT, terminate, load_image, FPS
from ButtonClass import Button
from draw_table import draw_table


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

main_img = load_image('main_menu.png')


def main():
    button_group = pygame.sprite.Group()

    start_btn = Button(WIDTH // 2 - 169.5, HEIGHT // 2 - HEIGHT // 3, 339, 92, 'Играть', 'button.png',
                       'button_clicked.png', 'data/click.mp3', button_group)

    settings_btn = Button(WIDTH // 2 - 169.5, HEIGHT // 2 - HEIGHT // 6.5, 339, 92, 'Настройки', 'button.png',
                          'button_clicked.png', 'data/click.mp3', button_group)

    score_btn = Button(WIDTH // 2 - 169.5, HEIGHT // 2 + HEIGHT // 33, 339, 92, 'Статистика', 'button.png',
                            'button_clicked.png', 'data/click.mp3', button_group)
    exit_button = Button(WIDTH // 2 - 169.5, HEIGHT // 2 + HEIGHT//5, 339, 92, 'Выйти', 'button.png',
                         'button_clicked.png', 'data/click.mp3', button_group)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or exit_button.clicked(event):
                running = False
                terminate()

            if start_btn.clicked(event):
                return# будет вызов функции самой игры
            if settings_btn.clicked(event):
                settings()
            if score_btn.clicked(event):
                score()

        screen.fill(pygame.Color('black'))
        screen.blit(main_img, (0, 0))
        button_group.update(pygame.mouse.get_pos())

        for button in button_group:
            button.draw(screen)

        pygame.display.flip()


def settings():
    button_group = pygame.sprite.Group()

    exit_button = Button(WIDTH // 2 - 169.5, HEIGHT // 2 + HEIGHT//5, 339, 92, 'Назад', 'button.png',
                         'button_clicked.png', 'data/click.mp3', button_group)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()

            if exit_button.clicked(event):
                return

        screen.fill(pygame.Color('black'))
        screen.blit(main_img, (-600, 0))
        button_group.update(pygame.mouse.get_pos())

        for button in button_group:
            button.draw(screen)

        pygame.display.flip()


def score():
    button_group = pygame.sprite.Group()

    exit_button = Button(WIDTH // 2 - 169.5, HEIGHT // 2 + HEIGHT//5, 339, 92, 'Назад', 'button.png',
                         'button_clicked.png', 'data/click.mp3', button_group)

    con = sqlite3.connect('data/stat.db')
    cursor = con.cursor()
    cursor.execute('SELECT * FROM stat')
    scores = cursor.fetchall()
    con.close()
    scroll = 0
    row = 30

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()

            if exit_button.clicked(event):
                return
            if event.type == pygame.MOUSEWHEEL:
                if event.y == 1:
                    scroll = max(scroll - 1, 0)
                elif event.y == -1:
                    max_down = len(scores) * row
                    scroll = min(scroll + 1, max_down)
        screen.fill(pygame.Color('black'))
        screen.blit(main_img, (-600, 0))
        button_group.update(pygame.mouse.get_pos())

        for button in button_group:
            button.draw(screen)

        draw_table(scores, scroll, screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
