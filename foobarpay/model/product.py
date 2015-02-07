from foobarpay.db import Base
from sqlalchemy import Column, Integer, String


class Product(Base):
    __tablename__ = 'product'
    pid = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, default=0, nullable=False)

    def __init__(self, pid=0, name="", price=150):
        self.pid = pid
        self.price = price
        self.name = name

    def getName(self):
        return self.name or str(self.pid)
