from time import sleep
from random import randint
from enum import Enum


class Screensaver(object):
    def __init__(self, display, tick_time):
        self.display = display
        self.screensavers = [
            WelcomeScreensaver(display, tick_time),
            PacmanScreensaver(display, tick_time),
            SpaceshipScreensaver(display, tick_time)
        ]
        self.active_screensaver = 1

    def get_active_screensaver(self):
        return self.screensavers[self.active_screensaver]

    def reset(self):
        self.get_active_screensaver().reset()

    def tick(self):
        screensaver = self.get_active_screensaver()
        if screensaver.tick():
            return
        screensaver.reset()
        if self.active_screensaver > 0:
            self.active_screensaver = 0
        else:
            self.active_screensaver = randint(1, len(self.screensavers) - 1)
        self.get_active_screensaver().reset()


class WelcomeScreensaver(object):
    def __init__(self, display, tick_time):
        self.display = display
        self.sleep_duration = 0.5
        self.duration = 30 / self.sleep_duration
        self.tick_time = tick_time
        self.reset()

    def reset(self):
        self.display.clear()
        self.current_tick = 0

    def tick(self):
        self.display.show_welcome(clear=False)
        self.current_tick += 1
        sleep(self.sleep_duration - self.tick_time)
        return self.current_tick <= self.duration


class PacmanScreensaver(object):
    def __init__(self, display, tick_time):
        self.display = display
        self.tick_time = tick_time
        self.pacman = ['c', 'C']
        self.reset()

    def reset(self):
        self.pacman_index = 0
        self.pacman_position = -1
        self.line_index = 0
        self.lines = [self.generate_line(init_pacman=True), self.generate_line()]

    def generate_line(self, width=20, init_pacman=False):
        line = list(" " * width)
        for i in range(1, width, 3):
            line[i] = 'o'
        if init_pacman:
            line[0] = self.pacman[self.pacman_index]
        return "".join(line)

    def show(self):
        self.display.show_two_messages(self.lines[0], self.lines[1], False)
        sleep(0.5 - self.tick_time)

    """ Returns True while active and False when finished """
    def tick(self):
        # just show the first frame and return
        if self.pacman_position < 0:
            self.pacman_position += 1
            self.show()
            return True
        # unset last position and increment counters
        line = list(self.lines[self.line_index])
        line[self.pacman_position] = ' '
        self.pacman_index = (self.pacman_index + 1) % len(self.pacman)
        self.pacman_position += 1
        # switch line after reaching the end
        if self.pacman_position >= len(line):
            line[self.pacman_position - 1] = ' '
            self.pacman_position = 0
            self.lines[self.line_index] = "".join(line)
            self.line_index = (self.line_index + 1)
            # finish if last line reached the end
            if self.line_index >= len(self.lines):
                self.lines[self.line_index - 1] = "".join(line)
                self.show()
                return False
            line = list(self.lines[self.line_index])
        # assign pacman char and show on display
        line[self.pacman_position] = self.pacman[self.pacman_index]
        self.lines[self.line_index] = "".join(line)
        self.show()
        return True


class SpaceshipScreensaver(object):
    class State(Enum):
        Intro = 0
        Main = 1
        Outro = 2
        GameOver = 3

    def __init__(self, display, tick_time):
        self.spaceship = '>'
        self.enemy = '<'
        self.bullet = '-'
        self.explosion = '*'
        self.display = display
        self.tick_time = tick_time
        self.sleep_duration = 0.3
        self.duration = 40 / self.sleep_duration
        self.game_over_duration = 5 / self.sleep_duration
        self.reset()

    def reset(self):
        self.spaceship_position = (19, 0)
        self.clear_lines()
        self.bullets = []
        self.enemies = []
        self.explosions = []
        self.current_tick = 0
        self.state = self.State.Intro

    def clear_lines(self):
        self.lines = [" " * 20, " " * 20]

    def show(self):
        self.clear_lines()
        lines = [list(self.lines[0]), list(self.lines[1])]

        # render bullets
        for x, y in self.bullets:
            if x >= 19:
                continue
            lines[y][x] = self.bullet
        # render enemies
        for x, y in self.enemies:
            if x >= 19:
                continue
            lines[y][x] = self.enemy
        # render enemies
        for x, y in self.explosions:
            lines[y][x] = self.explosion

        # if not game over, remove explosions and show spaceship
        if self.state != self.State.GameOver:
            self.explosions = []
            lines[self.spaceship_position[1]][self.spaceship_position[0]] = self.spaceship
        else:
            text = list("Game Over")
            for i in range(len(text)):
                lines[0][5 + i] = text[i]

        # display
        self.lines = ["".join(lines[0]), "".join(lines[1])]
        self.display.show_two_messages(self.lines[0], self.lines[1], False)
        sleep(self.sleep_duration - self.tick_time)

    def move_bullets(self):
        new_bullets = []
        for x, y in self.bullets:
            if x + 1 < 20:
                new_bullets.append((x + 1, y))
        self.bullets = new_bullets

    def move_enemies(self, x_delta=-1):
        new_enemies = []
        for x, y in self.enemies:
            if x > 0:
                new_enemies.append((x + x_delta, y))
        self.enemies = new_enemies

    def move_spaceship(self, x_delta=0):
        if x_delta != 0:
            self.spaceship_position = (self.spaceship_position[0] + x_delta,
                                       self.spaceship_position[1])
            return
        if 0 != self.current_tick % 4:
            return
        self.spaceship_position = (self.spaceship_position[0], randint(0, 1))

    def shoot(self, distribution=4, min_bullets=2):
        if 0 != self.current_tick % 4:
            return
        if 0 != randint(0, distribution - 1) and len(self.bullets) >= min_bullets:
            return
        self.bullets.append((self.spaceship_position[0] + 1, self.spaceship_position[1]))

    def spawn_enemy(self, distribution=2, max_enemies=3):
        if self.state == self.State.Intro and self.current_tick < 8:
            return
        if 0 != self.current_tick % 4:
            return
        if len(self.enemies) >= max_enemies:
            return
        if 0 != randint(0, distribution - 1):
            return
        self.enemies.append((19, randint(0, 1)))

    def check_collision(self):
        new_bullets = []
        new_enemies = []
        collided_enemies = []
        for b_x, b_y in self.bullets:
            bullet_collided = False
            for e_x, e_y in self.enemies:
                if b_x == e_x and b_y == e_y or \
                   b_x - 1 == e_x and b_y == e_y:
                    bullet_collided = True
                    collided_enemies.append((e_x, e_y))
                    self.explosions.append((e_x, e_y))
                    break
            if not bullet_collided:
                new_bullets.append((b_x, b_y))
        for e_x, e_y in self.enemies:
            if (e_x, e_y) == self.spaceship_position:
                self.explosions.append((e_x, e_y))
                self.state = self.state.GameOver
                self.current_tick = 0
                continue
            if (e_x, e_y) not in collided_enemies:
                new_enemies.append((e_x, e_y))
        self.bullets = new_bullets
        self.enemies = new_enemies

    def tick_state(self, x_delta_ship=0, x_delta_enemies=-1):
        self.move_spaceship(x_delta_ship)
        self.move_bullets()
        self.move_enemies(x_delta_enemies)
        self.spawn_enemy()
        self.shoot()
        self.check_collision()
        self.show()

    def tick(self):
        self.current_tick += 1
        # game over
        if self.state == self.State.GameOver:
            self.show()
            return self.current_tick <= self.game_over_duration
        # into mode
        if self.state == self.State.Intro:
            # switch from intro to main
            if self.spaceship_position[0] <= 0:
                self.state = self.State.Main
                self.current_tick = 0
                return True
            self.tick_state(-1, -1)
            return True
        # outro mode
        if self.state == self.State.Outro:
            # outro finished
            if self.spaceship_position[0] >= 19:
                return False
            self.move_bullets()
            self.tick_state(1, 1)
            return True
        # switch from main into outro mode
        if self.current_tick > self.duration:
            self.state = self.State.Outro
            self.current_tick = 0
            return True
        # main mode
        self.tick_state(0, -1)
        return True
