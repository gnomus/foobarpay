from foobarpay.model.customer import Customer
from foobarpay.model.product import Product

import logging
from time import sleep
from enum import Enum


class Logic(object):
    def __init__(self, display, db):
        self.display = display
        self.db = db
        self.reset()

    def reset(self):
        logging.debug("Resetting logic")
        self.state = State.Idle
        self.cart = 0
        self.customer = None
        self.display.showWelcome()

    def transactionStart(self, cid):
        logging.info("Starting transaction")
        self.customer = self.db.get_or_create(Customer, cid=cid)
        logging.debug("Name: {}".format(self.customer.getName()))
        logging.debug("Saldo: {}".format(self.customer.getSaldo()))
        self.display.showTwoMsgs("Hello {}".format(self.customer.getName()), "S: {:+.2f}".format(self.customer.getSaldo()/100))
        self.state = State.Started
        self.cart = 0

    def transactionEnd(self):
        logging.info("Completing transaction")
        self.display.clear()
        self.display.setPos(1,1)
        self.customer.modifySaldo(self.cart)
        self.db.commit()
        self.display.showTwoMsgs("Transaction", "completed")
        sleep(3)
        self.reset()

    def handleScan(self, scan):
        try:
            if scan.startswith("U-"): #User ID
                cid = int(scan[2:])
                if State.Idle == self.state:
                    self.transactionStart(cid)
                elif cid != self.customer.cid:
                    self.reset()
                    self.transactionStart(cid)
                else:
                    self.transactionEnd()
            else: # Product ID
                if self.state == State.Idle: # Product without active transaction
                    self.display.showTwoMsgs("Error", "Scan UID first")
                    sleep(3)
                    self.display.showWelcome()
                else: # Add product to transaction
                    pid = int(scan)
                    product = self.db.get(Product, pid=pid)
                    if product is None:
                        self.display.showTwoMsgs("Error", "Unknown product")
                        sleep(2)
                        self.display.showTwoMsgs("Hello {}".format(self.customer.getName()), "S: {:+.2f} / C: {:+.2f}".format(self.customer.saldo/100, self.cart/100))
                    else:
                        self.cart -= product.price
                        self.display.showTwoMsgs("{}: {:.2f}".format(product.name, product.price/100), "Cart: {:+.2f}".format(self.cart/100))
        except ValueError: pass


class State(Enum):
    Idle = 0
    Started = 1
