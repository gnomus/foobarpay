import os
import binascii
import evdev
from time import sleep

saldo = 10
cart = 0

class Display(object):
    def __init__(self,path):
        self.path = path

    def setPos(self, posX,posY):
        self.__sendCmd(b"\x06\x1B\x5B" + str.encode(str(posY)) + b"\x3B" + str.encode(str(posX)) + b"\x48")

    def showRawMsg(self, msg):
        self.__sendCmd(str.encode(msg))

    def showWelcome(self):
        self.clear()
        self.setPos(6,1)
        self.showRawMsg("Welcome to")
        self.setPos(6,2)
        self.showRawMsg("foobarpay!")

    def showMsg(self, msg):
        self.clear()
        self.setPos(1,1)
        self.showRawMsg(msg)

    def showTwoMsgs(self, msg1, msg2):
        self.clear()
        self.setPos(1,1)
        self.showRawMsg(msg1)
        self.setPos(1,2)
        self.showRawMsg(msg2)

    def clear(self):
        self.__sendCmd(b"\x1B\x5B\x32\x4A")

    def __sendCmd(self, cmd):
        msg = b"\x02\x00" + bytes([len(cmd)]) + cmd + bytes(29 - len(cmd))
        dev = open(self.path, "wb")
        dev.write(msg)
        dev.close()

class Logic(object):
    def __init__(self, display):
        # STATES:
        # 0 - Idle
        # 1 - Transaction Started
        self.state = 0
        self.display = display
        self.display.showWelcome()

    def handleScan(self, scan):
        global saldo, cart
        if scan.startswith("U-"): #User ID
            if self.state == 0:
                self.display.showTwoMsgs("Hello User", "S: {:+.2f}".format(saldo))
                self.state = 1
            else:
                self.display.clear()
                self.display.setPos(1,1)
                saldo = saldo + cart
                cart = 0
                self.display.showTwoMsgs("Transaction", "completed")
                sleep(3)
                self.display.showWelcome()
                self.state = 0
        else: # Product ID
            if self.state == 0:
                self.display.showTwoMsgs("Error", "Scan UID first")
                sleep(3)
                self.display.showWelcome()
            else:
                cart = cart - 1
                self.display.showTwoMsgs("Mate", "Cart: {:+.2f}".format(cart))



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



display = Display("/dev/hidraw1")
scanner = evdev.InputDevice("/dev/input/event17")
scanner.grab()
input_buffer = ""
logic = Logic(display)




while True:
    for event in scanner.read_loop():
        if event.type == evdev.ecodes.EV_KEY and event.value == 1:
            if event.code == 28:
                logic.handleScan(input_buffer)
                input_buffer = ""
            else:
                input_buffer += scancodes.get(event.code) or ""
