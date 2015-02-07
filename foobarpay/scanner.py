from evdev import InputDevice

scancodes = {
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


class Scanner(object):
    def __init__(self, device):
        self.device = InputDevice(device)
        self.device.grab()

    def read_loop(self):
        return self.device.read_loop()
