import random

import pygame
from pygame.locals import *
import time

Size = 32
BackGround = (10, 14, 23)


class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/apple-block.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.parent_screen = parent_screen
        self.x = Size * 3
        self.y = Size * 3


    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(3, 31) * Size
        self.y = random.randint(3, 15) * Size


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/snake-body-block.png").convert_alpha()
        self.block = pygame.transform.scale(self.block, (32, 32))
        self.x = [Size] * length
        self.y = [Size] * length
        self.direction = 'down'


    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):

        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'left':
            self.x[0] -= Size
        if self.direction == 'right':
            self.x[0] += Size
        if self.direction == 'up':
            self.y[0] -= Size
        if self.direction == 'down':
            self.y[0] += Size

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()


def is_collision(x1, y1, x2, y2):
    if y1 == y2:
        if x1 == x2:
            return True
    return False


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game")
        self.phonk = 1


        pygame.mixer.init()
        self.play_background_music()
        pygame.mixer.music.play(10)
        pygame.mixer.music.pause()

        escape_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE})
        pygame.event.post(escape_event)

        #space_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})
        #pygame.event.post(space_event)

        self.surface = pygame.display.set_mode((1024, 512))
        icon = pygame.image.load("resources/snake-logo.png")
        pygame.display.set_icon(icon)
        self.surface.fill((110, 110, 5))
        self.snake = Snake(self.surface, 3)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def render_background(self):
        bg = pygame.image.load("resources/gogog.png")
        self.surface.blit(bg, (0, 0))

    def play_background_music(self):
        pygame.mixer.music.load("resources/PSYCHO CRUISE - ONIMXRU, STRAWANGLE  SIGMA SONG.mp3")
        pygame.mixer.music.set_volume(0.1)
        # Start playing the music




    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        if is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):

            sound = pygame.mixer.Sound("resources/apple-eat.mp3")
            sound.set_volume(0.2)
            pygame.mixer.Sound.play(sound)
            self.snake.increase_length()
            self.apple.move()

        for i in range(3, self.snake.length):
            if is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                sound = pygame.mixer.Sound("resources/collision.mp3")
                sound.set_volume(0.2)
                pygame.mixer.Sound.play(sound)
                raise "Game over"
        if self.snake.x[0] < 0 or self.snake.x[0] >= 1000 or self.snake.y[0] < 0 or self.snake.y[0] >= 500:
            sound = pygame.mixer.Sound("resources/collision.mp3")
            sound.set_volume(0.2)
            pygame.mixer.Sound.play(sound)
            raise "Game over"
        if self.snake.x[0] >= 800 and self.snake.y[0] <= 60:
            sound = pygame.mixer.Sound("resources/collision.mp3")
            sound.set_volume(0.2)
            pygame.mixer.Sound.play(sound)
            raise "Game over"

    def display_score(self):
        font = pygame.font.SysFont('calibri', 30)
        score = font.render(f"Score: {self.snake.length - 3}", True, (0, 0, 0))
        self.surface.blit(score, (860, 22))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('calibribold', 120)
        line1 = font.render("Game Over!", True, (255, 255, 255))
        self.surface.blit(line1, (240, 170))
        font1 = pygame.font.SysFont('calibri', 28)
        line2 = font1.render(f"Press Enter to play again, press X to exit", True, (255, 255, 255))
        self.surface.blit(line2, (265, 290))
        self.display_score()

        pygame.display.flip()
        pygame.mixer.music.pause()


    def pauseinfo(self):
        self.render_background()
        font16 = pygame.font.SysFont('calibri', 16)
        font30 = pygame.font.SysFont('calibri', 26)
        font32 = pygame.font.SysFont('calibri', 40)
        font100 = pygame.font.SysFont('calibribold', 120)

        self.display_score()

        copyright = font16.render("by Denys Podolkhov aka @De44iK", True, (255, 255, 255))
        self.surface.blit(copyright, (0, 0))
        ver = font16.render("ver. 1.0.1 stable", True, (255, 255, 255))
        self.surface.blit(ver, (1, 495))
        pb = font16.render("SDL 2.0.22/Python 3.10", True, (255, 255, 255))
        self.surface.blit(pb, (855, 495))
        title = font100.render("Snake Game", True, (255, 255, 255))
        self.surface.blit(title, (230, 20))
        if self.snake.length - 3 == 0:
            hint = font30.render("Press Enter to Start the game. Press X to quit", True, (255, 255, 255))
            self.surface.blit(hint, (240, 480))
        else:
            hint = font30.render("Press Enter to Continue your game. Press X to quit", True, (255, 255, 255))
            self.surface.blit(hint, (226, 480))
        kkeys = font32.render("Control Keys", True, (255, 255, 255))
        self.surface.blit(kkeys, (150, 140))
        esc = font30.render("ESC - Open this menu", True, (255, 255, 255))
        self.surface.blit(esc, (80, 200))
        wasd = font30.render("W, A, S, D - control the snake", True, (255, 255, 255))
        self.surface.blit(wasd, (80, 240))
        ph = font30.render("SPACE - Toggle phonk mode", True, (255, 255, 255))
        self.surface.blit(ph, (80, 280))
        scr = font30.render("Enter - Start/Continue/Retry the game", True, (255, 255, 255))
        self.surface.blit(scr, (80, 320))
        xx = font30.render("X - Exit the game", True, (255, 255, 255))
        self.surface.blit(xx, (80, 360))
        obj = font32.render("Objective", True, (255, 255, 255))
        self.surface.blit(obj, (690, 140))
        st1 = font30.render("Objective in this ohio game", True, (255, 255, 255))
        self.surface.blit(st1, (620, 200))
        st2 = font30.render("is to score the best result", True, (255, 255, 255))
        self.surface.blit(st2, (630, 240))
        st3 = font30.render("by snake eating apples", True, (255, 255, 255))
        self.surface.blit(st3, (630, 280))
        st4 = font30.render("(phonk mode can be useful)", True, (255, 255, 255))
        self.surface.blit(st4, (630, 320))
        st5 = font30.render("good luck bro", True, (255, 255, 255))
        self.surface.blit(st5, (690, 360))

        pygame.display.flip()
        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface, 3)
        self.apple = Apple(self.surface)
        self.phonk = 1

    def run(self):
        running = True
        pause = False
        n = 0.2
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_x:
                        running = False
                    if event.key == K_ESCAPE:
                        pause = True
                        self.pauseinfo()
                        self.phonk = 1
                    if event.key == K_RETURN:
                        pause = False

                    if not pause:
                        if event.key == pygame.K_w and self.snake.direction != "down":
                            self.snake.move_up()
                        if event.key == pygame.K_s and self.snake.direction != "up":
                            self.snake.move_down()
                        if event.key == pygame.K_a and self.snake.direction != "right":
                            self.snake.move_left()
                        if event.key == pygame.K_d and self.snake.direction != "left":
                            self.snake.move_right()
                        if event.key == pygame.K_SPACE:
                            self.phonk += 1
                    if self.phonk % 2 == 0:
                        pygame.mixer.music.unpause()
                        n = 0.05
                    else:
                        pygame.mixer.music.pause()
                        n = 0.2
                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception:
                self.show_game_over()
                pause = True
                self.reset()
            time.sleep(n)


if __name__ == "__main__":
    game = Game()
    game.run()
