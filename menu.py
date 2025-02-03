import pygame
import sqlite3

from Base_func import WIDTH, HEIGHT, terminate, load_image, FPS, VOLUME
from ButtonClass import Button, Slaider, Point
from draw_table import draw_table
from draw_maps import Map

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

main_img = load_image('main_menu.png')


def menu():
    button_group = pygame.sprite.Group()
    # 169.5 = width изображения / 2
    start_btn = Button(WIDTH // 2 - 169.5, HEIGHT // 2 - HEIGHT // 3, 339, 92, 'Играть', 'button.png',
                       'button_clicked.png', 'data/click.mp3', button_group)

    settings_btn = Button(WIDTH // 2 - 169.5, HEIGHT // 2 - HEIGHT // 6.5, 339, 92, 'Настройки', 'button.png',
                          'button_clicked.png', 'data/click.mp3', button_group)

    score_btn = Button(WIDTH // 2 - 169.5, HEIGHT // 2 + HEIGHT // 33, 339, 92, 'Статистика', 'button.png',
                            'button_clicked.png', 'data/click.mp3', button_group)
    exit_button = Button(WIDTH // 2 - 169.5, HEIGHT // 2 + HEIGHT//4.7, 339, 92, 'Выйти', 'button.png',
                         'button_clicked.png', 'data/click.mp3', button_group)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or exit_button.clicked(event):
                running = False
                terminate()

            if start_btn.clicked(event, VOLUME):
                return
            if settings_btn.clicked(event, VOLUME):
                settings()
            if score_btn.clicked(event, VOLUME):
                score()

        screen.fill(pygame.Color('black'))
        screen.blit(main_img, (0, 0))
        button_group.update(pygame.mouse.get_pos())

        for button in button_group:
            button.draw(screen)

        pygame.display.flip()


def settings():
    global VOLUME
    button_group = pygame.sprite.Group()

    exit_button = Button(WIDTH // 2 - 169.5, HEIGHT // 2 + HEIGHT//3, 339, 92, 'Назад', 'button.png',
                         'button_clicked.png', 'data/click.mp3', button_group)
    slaider = Slaider(50, 50, WIDTH - 100, 'data/click.mp3', button_group)
    point = Point(50 + (WIDTH - 150) * VOLUME, 50, WIDTH - 100, button_group)

    first_map = Map(40, 100, 200, 200,
                    'mbgood.jpg', 'data/click.mp3', button_group)

    second_map = Map(360, 100, 200, 200,
                    'back_2.jpg', 'data/click.mp3', button_group)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()

            if exit_button.clicked(event, VOLUME):
                f = open('data/consts.txt')
                old_data = list(map(str.strip, f.readlines()))
                old_data[0] = VOLUME
                f.close()
                f = open('data/consts.txt', mode='w')
                for i in old_data:
                    f.write(f'{str(i)}\n')
                f.close()

                return
            if slaider.clicked(event, point, pygame.mouse.get_pos(), VOLUME):
                VOLUME = (point.x - slaider.x) / ((slaider.width - slaider.x) / 100) / 100

            first_map.clicked(event)
            second_map.clicked(event)

        screen.fill(pygame.Color('black'))
        screen.blit(main_img, (-600, 0))
        button_group.update(pygame.mouse.get_pos())

        for button in button_group:
            button.draw(screen)

        txt = 'Настроить звук'
        font = pygame.font.Font(None, 36)
        text = font.render(txt, True, (0, 0, 0))
        cords = (WIDTH // 2 - 90, 20)
        screen.blit(text, cords)

        pygame.display.flip()


def score():
    button_group = pygame.sprite.Group()

    exit_button = Button(WIDTH // 2 - 169.5, HEIGHT // 2 + HEIGHT//4.7, 339, 92, 'Назад', 'button.png',
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

            if exit_button.clicked(event, VOLUME):
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

