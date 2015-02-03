import logging


class Customer(object):
    def __init__(self, cid=42, name="", saldo=42):
        self.cid = cid
        self.name = name
        self.saldo = saldo
        if cid == 1234:
            self.name = "Cyclopropenylidene"
            self.saldo = 1337
        logging.info("Created customer {} ({})".format(self.cid, self.name))

    def modifySaldo(self, amount):
        self.saldo += amount

    def getName(self):
        return self.name or str(self.cid)

