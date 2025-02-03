import pygame
from ButtonClass import Button
from Base_func import VOLUME, terminate


def game_over(screen):
    button_group = pygame.sprite.Group()

    running = True
    width, height = screen.get_size()

    exit_button = Button(width // 5 + 339 // 2 - 40, height // 2, 339, 92, 'В меню', 'button.png',
           'button_clicked.png', 'data/click.mp3', button_group)

    restart_button = Button(width // 2 + 339 // 2 - 40, height // 2, 339, 92, 'Начать заново', 'button.png',
           'button_clicked.png', 'data/click.mp3', button_group)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()

            if exit_button.clicked(event, VOLUME):
                return 0

            if restart_button.clicked(event, VOLUME):
                return 1

        button_group.update(pygame.mouse.get_pos())

        for button in button_group:
            button.draw(screen)

        text = 'GAME OVER'
        font = pygame.font.Font(None, 36)
        text = font.render(text, True, (255, 255, 255))
        text_rect = text.get_rect(center=(width // 2, height//4.6))
        screen.blit(text, text_rect)

        pygame.display.flip()