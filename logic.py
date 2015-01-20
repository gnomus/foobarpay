from time import sleep
from customer import Customer


class Logic(object):
    def __init__(self, display, db):
        # STATES:
        # 0 - Idle
        # 1 - Transaction Started
        self.state = 0
        self.display = display
        self.display.showWelcome()
        self.db = db
        self.customer = None
        self.cart = 0

    def transactionStart(self, cid):
        self.customer = Customer(int(cid[2:]))
        self.display.showTwoMsgs("Hello {}".format(self.customer.getName()), "S: {:+.2f}".format(self.customer.saldo/100))
        self.state = 1
        self.cart = 0

    def transactionEnd(self):
        self.display.clear()
        self.display.setPos(1,1)
        self.customer.saldo = self.customer.saldo + self.cart
        self.display.showTwoMsgs("Transaction", "completed")
        sleep(3)
        self.display.showWelcome()
        self.state = 0
        self.customer = None

    def handleScan(self, scan):
        if scan.startswith("U-"): #User ID
            if self.state == 0: #Start Transaction
                self.transactionStart(scan)
            else: #End Transaction
                self.transactionEnd()
        else: # Product ID
            if self.state == 0: # Product without active transaction
                self.display.showTwoMsgs("Error", "Scan UID first")
                sleep(3)
                self.display.showWelcome()
            else: # Add product to transaction
                product = self.db.getProduct(scan)
                if product is None:
                    self.display.showTwoMsgs("Error", "Unknown product")
                    sleep(2)
                    self.display.showTwoMsgs("Hello User", "S: {:+.2f} / C: {:+.2f}".format(self.customer.saldo/100, self.cart/100))
                else:
                    self.cart -= product["Price"]
                    self.display.showTwoMsgs("{}: {:.2f}".format(product["Name"], product["Price"]/100), "Cart: {:+.2f}".format(self.cart/100))
