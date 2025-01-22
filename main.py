import pygame

from Base_func import WIDTH, HEIGHT, terminate
from ButtonClass import Button


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

button_group = pygame.sprite.Group()

start_btn = Button(WIDTH // 2 - 100, HEIGHT // 2, 339, 92, '', 'button.png',
                   'button_clicked.png', 'data/click.mp3', button_group)


def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()

            if start_btn.clicked(event):
                return

        screen.fill(pygame.Color('black'))
        button_group.update(pygame.mouse.get_pos())
        button_group.draw(screen)

        for button in button_group:
            button.draw(screen)

        pygame.display.flip()

main()
