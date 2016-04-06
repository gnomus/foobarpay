from foobarpay.db import Base
from sqlalchemy import Column, Integer, String

class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    _name = Column("name", String)
    saldo = Column(Integer, default=0, nullable=False)

    def __init__(self, id=0, saldo=0):
        self.id = id
        self.saldo = saldo

    def modify_saldo(self, amount):
        self.saldo += amount

    @property
    def name(self):
        return self._name or (str(self.id)[:-5] + "x" * 5)

    @name.setter
    def name(self, value):
        self._name = value
