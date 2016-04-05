#!/usr/bin/env python3

import logging
from sys import exit
from signal import signal, SIGINT
from sqlalchemy import create_engine
from argparse import ArgumentParser

from foobarpay.db import Database
from foobarpay.display import HIDrawDisplay, FifoDisplay
from foobarpay.scanner import EvdevScanner, FifoScanner
from foobarpay.logic import Logic
from foobarpay.model.product import Product
from foobarpay.tokens import TokenGenerator

class FooBarPay:
    DEFAULT_SCANNER  = '/dev/input/by-id/usb-©_Symbol_Technologies__Inc__2000_Symbol_Bar_Code_Scanner_S_N:ac08a7010000_Rev:NBRXUAAQ3-event-kbd'
    DEFAULT_DISPLAY  = '/dev/hidraw1'
    DEFAULT_DATABASE = 'sqlite:///foobarpay.sqlite'

    def __init__(self, cli_arguments):
        logging.basicConfig(level=logging.DEBUG if cli_arguments.debug else logging.INFO)

        self.database = Database(cli_arguments.database, debug=cli_arguments.debug_sql)
        if cli_arguments.display_driver == "fifo":
            self.display = FifoDisplay(cli_arguments.display)
        else:
            self.display = HIDrawDisplay(cli_arguments.display)
        if cli_arguments.scanner_driver == "fifo":
            self.scanner = FifoScanner(cli_arguments.scanner)
        else:
            self.scanner = EvdevScanner(cli_arguments.scanner)
        self.initialize_products()
        self.logic = Logic(self.display, self.database)

    def initialize_products(self):
        self.database.get_or_create(Product, id=4100060009503, name="Extaler Mineralquell", price=100)
        self.database.get_or_create(Product, id=42265832, name="Werretaler Aqua to go", price=100)
        self.database.get_or_create(Product, id=4029764001807, name="Club Mate")
        self.database.get_or_create(Product, id=4260031874056, name="Flora Power")
        self.database.get_or_create(Product, id=4260401930429, name="1337 Mate")
        self.database.get_or_create(Product, id=4066600603405, name="Paulaner Spezi")
        self.database.get_or_create(Product, id=4101120006685, name="Padaborner Pilsner")
        self.database.get_or_create(Product, id=40678092, name="Vitamalz")
        self.database.get_or_create(Product, id=4260031875008, name="Rhabarbershorle")
        self.database.get_or_create(Product, id=4015533019562, name="BioZisch Zitrone")
        self.database.get_or_create(Product, id=4015533014956, name="BioZisch Natur Orange")
        self.database.get_or_create(Product, id=4260189210034, name="Wostock Dattel Granatapfel")
        self.database.get_or_create(Product, id=4260189210072, name="Wostock Birne Rosmarin")
        self.database.get_or_create(Product, id=4260107220022, name="Fritz Kola zuckerfrei")
        self.database.get_or_create(Product, id=4260107220060, name="Fritz Limo Melone")
        self.database.get_or_create(Product, id=4260107220299, name="Fritz Limo Apfel-Kirsch-Holunder")
        self.database.get_or_create(Product, id=4260107220114, name="Fritz Limo Orange")
        self.database.get_or_create(Product, id=4014472002512, name="Bionade Holunder")

    def start(self):
        logging.info("Welcome to foobarpay")
        signal(SIGINT, lambda s, f: exit(0))
        while True:
            self.logic.handle_scanned_text(self.scanner.read())

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-v', '--debug', dest='debug', action='store_true', help='general debug messages')
    parser.add_argument('--debug-sql', dest='debug_sql', action='store_true', help='sql debug messages')
    parser.add_argument('--display', dest='display', default=FooBarPay.DEFAULT_DISPLAY, help='specify display device')
    parser.add_argument('--display-driver', dest='display_driver', choices=['hidraw', 'fifo'], default='hidraw', help='specify display driver')
    parser.add_argument('--scanner', dest='scanner', default=FooBarPay.DEFAULT_SCANNER, help='specify scanner device')
    parser.add_argument('--scanner-driver', dest='scanner_driver', choices=['evdev', 'fifo'], default='evdev', help='specify scanner driver')
    parser.add_argument('--db', dest='database', default=FooBarPay.DEFAULT_DATABASE, help='specify database file')
    parser.add_argument('--gen-tokens', dest='gen_tokens', action='store_true', help='generate customer tokens')
    parser.set_defaults(debug=False, debug_sql=False)

    args = parser.parse_args()

    if args.gen_tokens:
        TokenGenerator(Database(args.database, debug=args.debug_sql)).generate()
    else:
        FooBarPay(args).start()
