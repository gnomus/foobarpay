import logging


class Customer(object):
    def __init__(self, cid=42, name="", saldo=1337):
        self.cid = cid
        self.name = name
        self.saldo = saldo
        if cid == 1234:
            self.name = "Cyclopropenylidene"
        logging.info("Created customer {} ({})".format(self.cid, self.name))

    def modifySaldo(self, amount):
        self.saldo += amount

    def getName(self):
        return self.name or self.cid

