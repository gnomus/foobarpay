from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql.expression import ClauseElement
from sqlalchemy.ext.declarative import declarative_base
import logging


Base = declarative_base()

class Database(object):
    def __init__(self, engine, debug=False):
        self.engine = create_engine(engine, echo=debug)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        Base.metadata.create_all(self.engine)

    def get_or_create(self, model, defaults=None, **kwargs):
        instance = self.session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance
        params = dict((k, v) for k, v in kwargs.items() if not isinstance(v, ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        self.session.add(instance)
        return instance

    def getProduct(self, pid):
        product = None
        if pid == "4029764001807":
            product = {"Name": "Mate", "Price": 150}
        elif pid == "4260031874056":
            product = {"Name": "Flora", "Price": 150}
        logging.debug("Getting product by id {} -> {}".format(pid, product))
        return product
