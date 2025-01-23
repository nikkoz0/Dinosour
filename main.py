import pygame

from Base_func import WIDTH, HEIGHT, terminate, load_image, FPS
from ButtonClass import Button


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

main_img = load_image('main_menu.png')


def main():
    button_group = pygame.sprite.Group()

    start_btn = Button(WIDTH // 2 - 160, HEIGHT // 2 - 240, 339, 92, '', 'button.png',
                       'button_clicked.png', 'data/click.mp3', button_group)

    settings_btn = Button(WIDTH // 2 - 160, HEIGHT // 2 - 110, 339, 92, '', 'button.png',
                          'button_clicked.png', 'data/click.mp3', button_group)

    choose_chr_btn = Button(WIDTH // 2 - 160, HEIGHT // 2 + 20, 339, 92, '', 'button.png',
                            'button_clicked.png', 'data/click.mp3', button_group)
    exit_button = Button(WIDTH // 2 - 160, HEIGHT // 2 + 150, 339, 92, '', 'button.png',
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
            if choose_chr_btn.clicked(event):
                choose_chr()

        screen.fill(pygame.Color('black'))
        screen.blit(main_img, (0, 0))
        button_group.update(pygame.mouse.get_pos())

        for button in button_group:
            button.draw(screen)

        pygame.display.flip()


def settings():
    button_group = pygame.sprite.Group()


    exit_button = Button(WIDTH // 2 - 160, HEIGHT // 2 + 150, 339, 92, '', 'button.png',
                         'button_clicked.png', 'data/click.mp3', button_group)
    running = True

    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.fill((0, 0, 0))

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


def choose_chr():
    pass


if __name__ == '__main__':
    main()
