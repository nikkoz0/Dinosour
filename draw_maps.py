import pygame

from Base_func import WIDTH, HEIGHT, terminate, load_image, VOLUME


class Map(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image, sound, *groups):
        super().__init__(*groups)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.image_text = image
        self.image = pygame.transform.scale(load_image(image, -1), (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.volume = VOLUME
        self.sound = pygame.mixer.Sound(sound)
        self.sound.set_volume(self.volume)

        self.on_icon = False

    def update(self, pos):
        self.on_icon = self.rect.collidepoint(pos)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

        f = open('data/consts.txt')
        old_data = list(map(str.strip, f.readlines()))
        map_now = old_data[1]
        f.close()
        if map_now == self.image_text:
            x = self.x - 2
            y = self.y - 2
            width = self.width + 2
            height = self.height + 2
            rect = pygame.Rect(x, y, width, height)
            pygame.draw.rect(screen, pygame.Color('White'), rect, 2)

    def clicked(self, event, volume=None):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.on_icon:
            if volume:
                self.volume = volume
                self.sound.set_volume(self.volume)
            self.sound.play()
            f = open('data/consts.txt')
            old_data = list(map(str.strip, f.readlines()))
            old_data[1] = self.image_text
            f.close()
            f = open('data/consts.txt', mode='w')
            for i in old_data:
                f.write(f'{str(i)}\n')
            f.close()


