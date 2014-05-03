from sqlalchemy import create_engine
from sqlalchemy import *
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite://', echo=True)

Base = declarative_base()

Session = sessionmaker(bind=engine)
Session.configure(bind=engine)


class TestModel(Base):
    __tablename__ = 'test_model'

    id = Column(INTEGER, primary_key=True)
    field = Column(String)

Base.metadata.create_all(bind=engine)

t = TestModel()
t.id = 1
t.field = "test"
session = Session()
session.add(t)
session.commit()


class SessionMixin(object):
    def __init__(self, *args, **kwargs):
        self.session = Session()

        # This super is necessary
        # because in case of multiple inheritance
        # this calls the next __init__ in the MRO
        super(SessionMixin, self).__init__(*args, **kwargs)


