from foobarpay.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    _name = Column("name", String, nullable=False)
    price = Column(Integer, default=0, nullable=False)

    def __init__(self, id=0, name="", price=150):
        self.id = id
        self.price = price
        self._name = name

    @hybrid_property
    def name(self):
        return self._name or str(self.id)

    @name.setter
    def name(self, value):
        self._name = value
