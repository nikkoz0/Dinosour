import pygame

from Base_func import WIDTH, HEIGHT

# функция для вывода дб на экрна(сортировка не меняется)


def draw_table(results, scroll, screen):
    results = sorted(results, key=lambda x: x[0], reverse=True)
    font = pygame.font.Font(None, 36)
    header = font.render('Пройденный путь       Дата забега', True, (255, 255, 255))
    screen.blit(header, (WIDTH // 2 - WIDTH//2.95, HEIGHT // 20))
    c = 1
    for i in range(scroll, len(results)):
        y = 30 * (c + 1)
        if y > HEIGHT // 2 + HEIGHT//5:
            break
        dist = results[i][0]
        date = results[i][1].split('.')[0]
        text = f'{dist: < 20} {date}'
        surf = font.render(text, True, (0, 100, 124))
        screen.blit(surf, (WIDTH // 2 - WIDTH//4, y))
        c += 1

