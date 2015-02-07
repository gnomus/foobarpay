#!/usr/bin/env python
import os
import binascii
import logging
import evdev
from sqlalchemy import create_engine

from foobarpay.db import Database
from foobarpay.display import Display
from foobarpay.scanner import scancodes, Scanner
from foobarpay.logic import Logic
from foobarpay.model.product import Product


def init_products(db):
    db.get_or_create(Product, pid=4100060009503, name="Wasser", price=100)
    db.get_or_create(Product, pid=4029764001807, name="Mate")
    db.get_or_create(Product, pid=4260031874056, name="Flora")
    db.commit()

def main():
    logging.basicConfig(level=logging.DEBUG)

    db = Database('sqlite:///foobarpay.sqlite')
    display = Display("/dev/hidraw1")
    scanner = Scanner("/dev/input/by-id/usb-©_Symbol_Technologies__Inc__2000_Symbol_Bar_Code_Scanner_S_N:ac08a7010000_Rev:NBRXUAAQ3-event-kbd")
    logic = Logic(display, db)

    init_products(db);

    logging.info("Welcome to foobarpay")
    input_buffer = ""
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
