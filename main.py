import pygame
import sys

from Base_func import WIDTH, HEIGHT, terminate
from ButtonClass import Button


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

button_group = pygame.sprite.Group()

start_btn = Button(WIDTH // 2 - 100, HEIGHT // 2, 339, 92, '', 'button.png',
                   'button_clicked.png', 'data/click.mp3', button_group)

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            terminate()

        button_group.update(pygame.mouse.get_pos())

        for b in button_group:
            b.clicked(event)
    screen.fill(pygame.Color('black'))
    for b in button_group:
        b.draw(screen)
    pygame.display.flip()
