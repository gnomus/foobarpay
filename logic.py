from time import sleep
saldo = 1000
cart = 0


class Logic(object):
    def __init__(self, display, db):
        # STATES:
        # 0 - Idle
        # 1 - Transaction Started
        self.state = 0
        self.display = display
        self.display.showWelcome()
        self.db = db

    def handleScan(self, scan):
        global saldo, cart
        if scan.startswith("U-"): #User ID
            if self.state == 0: #Start Transaction
                self.display.showTwoMsgs("Hello User", "S: {:+.2f}".format(saldo/100))
                self.state = 1
            else: #End Transaction
                self.display.clear()
                self.display.setPos(1,1)
                saldo = saldo + cart
                cart = 0
                self.display.showTwoMsgs("Transaction", "completed")
                sleep(3)
                self.display.showWelcome()
                self.state = 0
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
                    self.display.showTwoMsgs("Hello User", "S: {:+.2f} / C: {:+.2f}".format(saldo/100, cart/100))
                else:
                    cart -= product["Price"]
                    self.display.showTwoMsgs("{}: {:.2f}".format(product["Name"], product["Price"]/100), "Cart: {:+.2f}".format(cart/100))
