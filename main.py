import pygame
import os
import random
import sqlite3
from menu import menu
from game_over import game_over
from Base_func import WIDTH as W, HEIGHT as H


menu()
os.environ['SDL_VIDEO_CENTERED'] = '1'

WIDTH = 1900
HEIGHT = 1250
screen_size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(screen_size)
GRAVITY = 0.4
SPEED = 2
LOOPS = 0
hero_gr = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
pygame.mixer.pre_init()
pygame.init()


class SpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


boy1 = load_image("boy1 (2).png")
boy2 = load_image("boy2 (2).png")
boy3 = load_image("boy3 (2).png")
boy4 = load_image("boy4 (2).png")
boy5 = load_image("boy3 (1).png")
boy6 = load_image("boy4 (1).png")
boy7 = load_image("boy1 (1).png")

player_image = 'mar.png'
screen_rect = (0, 0, WIDTH, HEIGHT)


class Money:
    pass


class DB:
    def __init__(self):
        self.db = sqlite3.connect('data/stat.db')
        self.cur = self.db.cursor()
        act = 100
        self.cur.execute("""INSERT INTO stat VALUES (?, ?)""", (act, 0))
        self.res = self.cur.execute("""SELECT * FROM score""").fetchall()
        self.db.commit()


class Particle(pygame.sprite.Sprite):
    fire = [load_image("waterDrop.png")]
    for scale in (10, 11):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


def couples(position):
    particle_count = 20
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


class Collision:
    def between(self, obj1,  obj2):
        distance = (((obj2.x + 100) - (obj1[0] + 80)) ** 2 + ((obj2.y + 80) - (obj1[1] + 200)) ** 2) ** 0.5
        return distance <= 130


class Score:
    def __init__(self):
        self.hs = db.res[0][0]
        self.act = 0
        self.font = pygame.font.SysFont('fffvf', 50)
        self.color = (100, 70, 120)
        self.show()

    def update(self, loops):
        self.act = loops // 10 + game.speed // 10
        self.check_hs()
        self.show()

    def show(self):
        self.lbl = self.font.render(f'RECORD {db.cur.execute("""SELECT * FROM score""").fetchall()[0][0]}    NOW {self.act}', 1, self.color)
        lbl_width = self.lbl.get_rect().width
        screen.blit(self.lbl, (WIDTH - lbl_width - 120, 150))

    def check_hs(self):
        if db.cur.execute("""SELECT * FROM score """).fetchall()[0][0] <= self.act:
            db.cur.execute("""DELETE FROM score """)
            db.cur.execute("""INSERT INTO score VALUES (?)""", (self.act, ))
            db.db.commit()


class Background:
    def __init__(self, x):
        self.width = WIDTH
        self.height = HEIGHT
        self.set_texture()
        self.x = x
        self.y = 0
        self.show()

    def show(self):
        screen.blit(self.texture, (self.x, self.y))

    def set_texture(self):
        self.texture = load_image('mbgood.jpg')
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))

    def update(self, dx):
        self.x += dx
        if self.x <= -WIDTH:
            self.x = WIDTH


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Hero(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_gr)
        self.image = boy1
        self.rect = self.image.get_rect().move((250, 775))
        self.pos = (pos_x, pos_y)
        self.jumping = False
        self.boy1 = True
        self.boy2 = False
        self.boy3 = False
        self.boy4 = False
        self.mask = pygame.mask.from_surface(self.image)
        self.falling = False
        self.onground = True
        self.up = 0
        self.down = 0

    def update(self, x, y):
        if self.jumping:
            self.image = boy2
            self.velocity += 0.5
            self.rect[1] += self.velocity
            if self.rect[1] <= 298:
                game.hero.fall()

        elif self.falling:
            self.velocity += 0.3
            self.rect[1] += self.velocity
            if self.rect[1] >= 775:
                game.hero.run()

        elif self.onground:
            if self.boy1 and LOOPS % 10 == 0:
                self.boy1 = False
                self.image = boy1
                self.rect = self.image.get_rect().move((250, 775))
                self.boy2 = True

            elif self.boy2 and LOOPS % 10 == 0:
                self.boy2 = False
                self.image = boy2
                self.rect = self.image.get_rect().move((240, 775))
                self.boy3 = True

            elif self.boy3 and LOOPS % 10 == 0:
                self.boy3 = False
                self.image = boy3
                self.rect = self.image.get_rect().move((230, 775))
                self.boy4 = True

            elif self.boy4 and LOOPS % 10 == 0:
                self.boy4 = False
                self.image = boy4
                self.rect = self.image.get_rect().move((220, 775))
                self.boy1 = True

    def jump(self):
        self.velocity = -22
        self.jumping = True
        self.onground = False
        self.falling = False
        self.image = boy6
        self.rect = self.image.get_rect().move((220, 775))

    def fall(self):
        self.velocity = 2
        self.jumping = False
        self.onground = False
        self.falling = True

    def run(self):
        self.jumping = False
        self.onground = True
        self.falling = False


class Obstacles:
    def __init__(self, x):
        self.x = x
        self.y = 870
        self.ran = ''
        if self.ran == 'pix-Photoroom.png':
            self.width = 250
            self.height = 190
        else:
            self.width = 200
            self.height = 170
        self.set_texture()
        self.show()
        self.masksps = []
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dx):
        self.x += dx

    def show(self):
        screen.blit(self.texture, (self.x, self.y))

    def set_texture(self):
        self.masksps = ['pixelkoost1-Photoroom.png', 'koost3-Photoroom.png', 'pix-Photoroom.png']
        self.ran = random.choice(self.masksps)
        if self.ran == 'pix-Photoroom.png':
            self.width = 210
            self.height = 150
            self.y = 870
            self.image = load_image(self.ran)
            self.texture = pygame.transform.scale(self.image, (self.width, self.height))
        elif self.ran == 'pixelkoost1-Photoroom.png':
            self.width = 250
            self.height = 220
            self.y = 820
            self.image = load_image(self.ran)
            self.texture = pygame.transform.scale(self.image, (self.width, self.height))
        else:
            self.width = 230
            self.height = 180
            self.y = 845
            self.image = load_image(self.ran)
            self.texture = pygame.transform.scale(self.image, (self.width, self.height))


class Game:
    def __init__(self):
        self.db = sqlite3.connect('data/stat.db')
        self.cur = self.db.cursor()
        self.speed = 5
        self.bg = [Background(0), Background(1900)]
        self.obstacles = []
        self.score = Score()
        self.hero = Hero(250, 775)
        self.collision = Collision()
        self.playing = False
        self.over = False
        self.Flpause = False

    def start(self):
        self.playing = True
        if not game.Flpause:
            pygame.mixer.music.load('data/PhonMusic.mp3')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1, 10)
            self.jumpS = pygame.mixer.Sound('data/jumpSound.mp3')
            self.getS = pygame.mixer.Sound('data/100sound.mp3')
        else:
            pygame.mixer.music.unpause()
            self.Flpause = False

    def stop(self):
        pygame.mixer.music.pause()
        self.playing = False

    def spaw(self, loops):
        return loops % 100 == 0

    def spawn_obstacles(self):
        if len(self.obstacles) > 0:
            prev = self.obstacles[-1]
            x = random.randint(prev.x + 600, prev.x + 1500)
        else:
            x = random.randint(WIDTH + 100, WIDTH + 300)
            self.obstacles.append(Obstacles(x))
        obstacle = Obstacles(x)
        self.obstacles.append(obstacle)
        for i in range(len(self.obstacles) - 2):
            if self.obstacles[i].x < 0:
                del self.obstacles[i]

    def restart(self):
        self.hero.rect.x = 250
        self.hero.rect.y = 700
        self.obstacles = []
        self.over = False
        if db.cur.execute("""SELECT hi FROM score""").fetchall()[0][0] <= game.score.act:
            db.cur.execute("""DELETE FROM score """)
            db.cur.execute("""INSERT INTO score VALUES (?)""", (game.score.act, ))
            print(db.cur.execute("""SELECT * FROM score""").fetchall())
            db.db.commit()
        pygame.mixer.music.play(-1)
        print()
        self.__init__()


if __name__ == '__main__':
    db = DB()
    score = Score()
    game = Game()
    clock = pygame.time.Clock()
    running = True
    rect_heroY = game.hero.pos[1]
    a = 1
    game.start()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game.hero.onground and game.playing:
                        game.hero.jump()
                        game.jumpS.play()
                if event.key == pygame.K_p and not game.over:
                    if game.playing:
                        game.stop()
                    else:
                        game.start()
                if event.key == pygame.K_r:
                    game.hero.kill()
                    game.restart()
                    LOOPS = 0
                    game.playing = True
                elif event.key == pygame.K_UP:
                    if game.hero.onground and game.playing:
                        game.hero.jump()
                        game.jumpS.play()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    couples(pygame.mouse.get_pos())
                    pygame.mixer.music.stop()
        if game.playing:
            if game.speed != 10 and LOOPS % 1000 == 0 and LOOPS != 0:
                game.speed += 1
                game.getS.play()
            elif LOOPS % 1000 == 0 and LOOPS != 0:
                game.getS.play()
            game.score.update(LOOPS)
            game.score.show()
            for bg in game.bg:
                bg.update(-game.speed)
                bg.show()
            hero_gr.update(game.hero.rect[0], game.hero.rect[1])
            hero_gr.draw(screen)
            all_sprites.update()
            all_sprites.draw(screen)
            if game.spaw(LOOPS):
                game.spawn_obstacles()
            for obstacle in game.obstacles:
                obstacle.show()
                obstacle.update(-game.speed)
                if game.collision.between(game.hero.rect[:2], obstacle):
                    pygame.mixer.music.stop()
                    game.db.close()
                    game.hero.kill()
                    if game_over(screen):
                        game.restart()
                        LOOPS = 0
                        game.playing = True
                    else:
                        screen = pygame.display.set_mode((W, H))
                        menu()
                        screen = pygame.display.set_mode(screen_size)
                        game.restart()
                        LOOPS = 0
                        game.playing = True

            LOOPS += 1
            game.score.update(LOOPS)
            game.score.show()
            pygame.display.flip()
            clock.tick(120)
    pygame.quit()
    db.cur.close()
