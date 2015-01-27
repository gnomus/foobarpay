#!/usr/bin/env python
import os
import binascii
import logging
from display import Display
from logic import Logic
from db import Database
from scanner import scancodes, Scanner
import evdev


def main():
    logging.basicConfig(level=logging.DEBUG)
    db = Database("db.sqlite")
    display = Display("/dev/hidraw1")
    scanner = Scanner("/dev/input/by-id/usb-©_Symbol_Technologies__Inc__2000_Symbol_Bar_Code_Scanner_S_N:ac08a7010000_Rev:NBRXUAAQ3-event-kbd")
    logic = Logic(display, db)
    input_buffer = ""

    logging.info("Welcome to foobarpay")
    while True:
        for event in scanner.read_loop():
            if event.type == evdev.ecodes.EV_KEY and event.value == 1:
                if event.code == 28:
                    logic.handleScan(input_buffer)
                    input_buffer = ""
                else:
                    input_buffer += scancodes.get(event.code) or ""

if __name__ == "__main__":
    main()
