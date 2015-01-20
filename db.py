import sqlite3

class Database(object):
    def __init__(self, path):
        return

    def getProduct(self, pid):
        if pid == "4029764001807":
            return {"Name": "Mate", "Price": 150}
        else:
            return None
