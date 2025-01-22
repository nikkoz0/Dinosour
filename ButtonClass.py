import pygame

from Base_func import load_image


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text, image, image_on_icon, sound, *groups):
        super().__init__(*groups)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

        # изображение будет меняться при наведении на кнопку

        self.image = pygame.transform.scale(load_image(image, -1), (width, height))
        self.image_on_icon = pygame.transform.scale(load_image(image_on_icon, -1), (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.sound = pygame.mixer.Sound(sound)

        self.on_icon = False

    def draw(self, screen):
        # есть наведение на кнопку или нет
        if self.on_icon:
            img = self.image_on_icon
        else:
            img = self.image

        screen.blit(img, self.rect)

        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def update(self, pos):
        self.on_icon = self.rect.collidepoint(pos)

    def clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.on_icon:
            self.sound.play()

