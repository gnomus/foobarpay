from time import sleep


class Screensaver(object):
    def __init__(self, display, tick_time):
        self.display = display
        self.screensavers = [PacmanScreensaver(display, tick_time)]
        self.active_screensaver = self.screensavers[0]

    def get_active_screensaver(self):
        return self.screensavers[self.active_screensaver].reset()

    def reset(self):
        self.active_screensaver.reset()

    def tick(self):
        if not self.active_screensaver.tick():
            self.active_screensaver.reset()


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
