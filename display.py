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
