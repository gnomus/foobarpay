from foobarpay.model.customer import Customer
from foobarpay.model.product import Product

import logging
from time import sleep
from enum import Enum

class Logic(object):
    class State(Enum):
        Idle = 0
        Started = 1

    USER_ID_PREFIX = 'U-'
    LOAD_PREFIX = 'L-'

    def __init__(self, display, database):
        self.display = display
        self.database = database
        self.reset()

    def reset(self):
        logging.debug("Resetting logic")
        self.state = self.State.Idle
        self.cart = 0
        self.customer = None
        self.display.show_welcome()

    def transaction_start(self, customer_id):
        logging.info("Starting transaction")
        self.customer = self.database.get_or_create(Customer, id=customer_id)
        logging.debug("Name: {}".format(self.customer.name))
        logging.debug("Saldo: {}".format(self.customer.saldo))
        self.display.show_two_messages("Hello {}".format(self.customer.name), "S: {:+.2f}".format(self.customer.saldo/100))
        self.state = self.State.Started
        self.cart = 0

    def transaction_end(self):
        logging.info("Completing transaction")
        self.display.clear()
        self.display.set_position(1,1)
        self.customer.modify_saldo(self.cart)
        self.database.commit()
        self.display.show_two_messages("Transaction", "completed")
        sleep(3)
        self.reset()

    def handle_scanned_text(self, scanned_text):
        try:
            if scanned_text.startswith(self.USER_ID_PREFIX):
                customer_id = int(scanned_text[2:])
                if self.state == self.State.Idle:
                    self.transaction_start(customer_id)
                elif customer_id != self.customer.id:
                    self.reset()
                    self.transaction_start(customer_id)
                else:
                    self.transaction_end()
            if scanned_text.startswith(self.LOAD_PREFIX):
                if self.state == self.State.Idle: # Product without active transaction
                    self.display.show_two_messages("Error", "Scan UID first")
                    sleep(3)
                    self.display.show_welcome()
                else: # Add credit loading to transaction
                    load_amount = int(scanned_text[2:])
                    self.cart += load_amount
                    self.display.show_two_messages(
                            "Credits loaded: {:.2f}".format(load_amount/100),
                            "Cart: {:+.2f}".format(self.cart/100)
                    )
            else: # Product ID
                if self.state == self.State.Idle: # Product without active transaction
                    self.display.show_two_messages("Error", "Scan UID first")
                    sleep(3)
                    self.display.show_welcome()
                else: # Add product to transaction
                    product_id = int(scanned_text)
                    product = self.database.get(Product, id=product_id)
                    if product is None:
                        self.display.show_two_messages("Error", "Unknown product")
                        sleep(2)
                        self.display.show_two_messages(
                                "Hello {}".format(self.customer.name[:12]),
                                "S: {:+.2f} / C: {:+.2f}".format(self.customer.saldo / 100, self.cart / 100)
                        )
                    else:
                        self.cart -= product.price
                        self.display.show_two_messages(
                                "{}: {:.2f}".format(product.name, product.price/100),
                                "Cart: {:+.2f}".format(self.cart/100)
                        )
        except ValueError: pass
