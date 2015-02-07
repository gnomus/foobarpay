from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import ClauseElement
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Database(object):
    def __init__(self, engine, debug=False):
        self.engine = create_engine(engine, echo=debug)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        Base.metadata.create_all(self.engine)

    def get(self, model, defaults=None, **kwargs):
        return self.session.query(model).filter_by(**kwargs).first()

    def get_or_create(self, model, defaults=None, **kwargs):
        instance = self.get(model, defaults, **kwargs)
        if instance:
            return instance
        params = dict((k, v) for k, v in kwargs.items() if not isinstance(v, ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        self.session.add(instance)
        return instance

    def commit(self):
        self.session.commit()

    def flush(self):
        self.session.flush()
