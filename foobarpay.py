#!/usr/bin/env python

import logging
from sys import exit
from evdev import ecodes
from signal import signal, SIGINT
from sqlalchemy import create_engine
from argparse import ArgumentParser

from foobarpay.db import Database
from foobarpay.display import Display
from foobarpay.scanner import scancodes, Scanner
from foobarpay.logic import Logic
from foobarpay.model.product import Product

class FooBarPay:
    DEFAULT_SCANNER  = '/dev/input/by-id/usb-©_Symbol_Technologies__Inc__2000_Symbol_Bar_Code_Scanner_S_N:ac08a7010000_Rev:NBRXUAAQ3-event-kbd'
    DEFAULT_DISPLAY  = '/dev/hidraw1'
    DEFAULT_DATABASE = 'sqlite:///foobarpay.sqlite'

    def __init__(self, cli_arguments):
        logging.basicConfig(level=logging.DEBUG if cli_arguments.debug else logging.INFO)

        self.database = Database(cli_arguments.database, debug=cli_arguments.debug_sql)
        self.display = Display(cli_arguments.display)
        self.scanner = Scanner(cli_arguments.scanner)
        self.initialize_products()
        self.logic = Logic(self.display, self.database)

    def initialize_products(self):
        self.database.get_or_create(Product, id=4100060009503, name="Wasser", price=100)
        self.database.get_or_create(Product, id=4029764001807, name="Mate")
        self.database.get_or_create(Product, id=4260031874056, name="Flora")

    def start(self):
        logging.info("Welcome to foobarpay")
        signal(SIGINT, lambda s, f: exit(0))
        input_buffer = ""
        while True:
            for event in self.scanner.read_loop():
                if event.type == ecodes.EV_KEY and event.value == 1:
                    if event.code == 28:
                        self.logic.handle_scanned_text(input_buffer)
                        input_buffer = ""
                    else:
                        input_buffer += scancodes.get(event.code) or ""

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-v', '--debug', dest='debug', action='store_true', help='general debug messages')
    parser.add_argument('--debug-sql', dest='debug_sql', action='store_true', help='sql debug messages')
    parser.add_argument('--display', dest='display', default=FooBarPay.DEFAULT_DISPLAY, help='specify display device')
    parser.add_argument('--scanner', dest='scanner', default=FooBarPay.DEFAULT_SCANNER, help='specify scanner device')
    parser.add_argument('--db', dest='database', default=FooBarPay.DEFAULT_DATABASE, help='specify database file')
    parser.set_defaults(debug=False, debug_sql=False)

    FooBarPay(parser.parse_args()).start()
