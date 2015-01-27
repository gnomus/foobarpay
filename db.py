import sqlite3
import logging


class Database(object):
    def __init__(self, path):
        return

    def getProduct(self, pid):
        product = None
        if pid == "4029764001807":
            product = {"Name": "Mate", "Price": 150}
        elif pid == "4260031874056":
            product = {"Name": "Flora", "Price": 150}
        else:
            product = None
        logging.debug("Getting product by id {} -> {}".format(pid, product))
        return product
