from evdev import InputDevice, ecodes
from fcntl import fcntl, F_SETFL, F_GETFL
from os import O_NONBLOCK, read
from threading import Thread
from collections import deque


class EvdevScanner(object):
    def __init__(self, device):
        self.device = InputDevice(device)
        self.buffer = ""
        self.lines = deque()
        self.scancodes = {
            2: u'1',
            3: u'2',
            4: u'3',
            5: u'4',
            6: u'5',
            7: u'6',
            8: u'7',
            9: u'8',
            10: u'9',
            11: u'0',
            28: u'\n',
            30: u'A',
            48: u'B',
            46: u'C',
            32: u'D',
            18: u'E',
            33: u'F',
            34: u'G',
            35: u'H',
            23: u'I',
            36: u'J',
            37: u'K',
            38: u'L',
            50: u'M',
            49: u'N',
            24: u'O',
            25: u'P',
            16: u'Q',
            19: u'R',
            31: u'S',
            20: u'T',
            22: u'U',
            47: u'V',
            17: u'W',
            45: u'X',
            21: u'Y',
            44: u'Z',
            12: u'-'
        }
        self.device.grab()
        self.thread = Thread(target=self.loop, daemon=True)
        self.thread.start()

    def loop(self):
        for event in self.device.read_loop():
            if event.type != ecodes.EV_KEY or event.value != 1:
                continue
            scanned_input = self.scancodes.get(event.code)
            if scanned_input == "\n":
                line = self.buffer
                self.buffer = ""
                self.lines.append(line)
                continue
            self.buffer += scanned_input or ""

    def read(self):
        if len(self.lines) <= 0:
            return None
        line = self.lines.popleft()
        return line


class FifoScanner(object):
    def __init__(self, device):
        self.fifo = open(device, 'r')
        self.fd = self.fifo.fileno()
        self.buffer = ""
        fcntl(self.fd, F_SETFL, fcntl(self.fd, F_GETFL) | O_NONBLOCK)

    def read(self):
        try:
            block = read(self.fd, 1024)
            self.buffer += block.decode()
            if not self.buffer.endswith("\n"):
                return None
            line = self.buffer[:-1]
            self.buffer = ""
            return line
        except BlockingIOError:
            return None
