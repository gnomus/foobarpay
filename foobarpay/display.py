class Display(object):
    def __init__(self, path):
        self.path = path
        self.device = open(self.path, "wb")

    def set_position(self, pos_x, pos_y):
        self.__send_command(b"\x06\x1B\x5B" + str.encode(str(pos_y)) + b"\x3B" + str.encode(str(pos_x)) + b"\x48")

    def show_raw_message(self, message):
        self.__send_command(str.encode(message))

    def show_welcome(self):
        self.clear()
        self.set_position(6, 1)
        self.show_raw_message("Welcome to")
        self.set_position(6, 2)
        self.show_raw_message("foobarpay!")

    def show_message(self, message):
        self.clear()
        self.set_position(1, 1)
        self.show_raw_message(message)

    def show_two_messages(self, message1, message2):
        self.clear()
        self.set_position(1, 1)
        self.show_raw_message(message1)
        self.set_position(1, 2)
        self.show_raw_message(message2)

    def clear(self):
        self.__send_command(b"\x1B\x5B\x32\x4A")

    def __send_command(self, command):
        message = b"\x02\x00" + bytes([len(command)]) + command + bytes(29 - len(command))
        self.device.write(message)
        self.device.flush()
