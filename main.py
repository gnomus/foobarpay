#!/usr/bin/env python
import os
import binascii
import logging
import evdev
from sqlalchemy import create_engine

from foobarpay.display import Display
from foobarpay.logic import Logic
from foobarpay.db import Database
from foobarpay.scanner import scancodes, Scanner

def main():
    logging.basicConfig(level=logging.DEBUG)
    db = Database('sqlite:///:memory:')
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
