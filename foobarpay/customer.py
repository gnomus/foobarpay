from .db import Base
from sqlalchemy import Column, Integer, String


class Customer(Base):
    __tablename__ = 'customer'
    cid = Column(Integer, primary_key=True)
    name = Column(String)
    saldo = Column(Integer, default=0)

    def __init__(self, cid=0, saldo=0):
        self.cid = cid
        self.saldo = saldo

    def modifySaldo(self, amount):
        self.saldo += amount

    def getName(self):
        return self.name or str(self.cid)

    def getSaldo(self):
        return self.saldo
