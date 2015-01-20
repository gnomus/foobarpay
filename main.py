import os
import binascii
import evdev
from display import Display
from logic import Logic
from db import Database

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



db = Database("db.sqlite")
display = Display("/dev/hidraw1")
scanner = evdev.InputDevice("/dev/input/by-id/usb-©_Symbol_Technologies__Inc__2000_Symbol_Bar_Code_Scanner_S_N:ac08a7010000_Rev:NBRXUAAQ3-event-kbd")
scanner.grab()
logic = Logic(display, db)

input_buffer = ""

while True:
    for event in scanner.read_loop():
        if event.type == evdev.ecodes.EV_KEY and event.value == 1:
            if event.code == 28:
                logic.handleScan(input_buffer)
                input_buffer = ""
            else:
                input_buffer += scancodes.get(event.code) or ""
