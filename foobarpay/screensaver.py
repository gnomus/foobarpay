from time import sleep
from random import randint


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
    def __init__(self, display, tick_time):
        self.spaceship = '>'
        self.bullet = '-'
        self.display = display
        self.tick_time = tick_time
        self.sleep_duration = 0.3
        self.duration = 30 / self.sleep_duration
        self.reset()

    def reset(self):
        self.spaceship_position = (0, 0)
        self.clear_lines()
        self.bullets = []
        self.current_tick = 0

    def clear_lines(self):
        self.lines = [" " * 20, " " * 20]
        line = list(self.lines[self.spaceship_position[1]])
        line[self.spaceship_position[0]] = self.spaceship
        self.lines[self.spaceship_position[1]] = "".join(line)

    def show(self):
        self.display.show_two_messages(self.lines[0], self.lines[1], False)
        sleep(self.sleep_duration - self.tick_time)

    def move_bullets(self):
        new_bullets = []
        for x, y in self.bullets:
            if x + 1 < 20:
                new_bullets.append((x + 1, y))
        self.bullets = new_bullets

    def draw_bullets(self):
        lines = [list(self.lines[0]), list(self.lines[1])]
        for x, y in self.bullets:
            lines[y][x] = self.bullet
        self.lines = ["".join(lines[0]), "".join(lines[1])]

    def move_spaceship(self):
        if 0 != self.current_tick % 4:
            return
        self.spaceship_position = (self.spaceship_position[0], randint(0, 1))

    def shoot(self):
        if 0 != self.current_tick % 4:
            return
        if 0 != randint(0, 1) and len(self.bullets) >= 2:
            return
        self.bullets.append((1, self.spaceship_position[1]))

    def tick(self):
        if self.current_tick > self.duration:
            return False
        self.current_tick += 1
        self.move_spaceship()
        self.move_bullets()
        self.shoot()
        self.clear_lines()
        self.draw_bullets()
        self.show()
        return True
