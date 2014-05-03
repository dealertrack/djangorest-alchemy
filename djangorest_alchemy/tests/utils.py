from sqlalchemy import create_engine
from sqlalchemy import *
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import mapper
import datetime

engine = create_engine('sqlite://', echo=True)

Base = declarative_base()

Session = sessionmaker(bind=engine)
Session.configure(bind=engine)

metadata = MetaData()

cls_test = Table('classical_test', metadata,
                 Column(u'id', INTEGER(), primary_key=True),
                 Column(u'field', String)
                 )


# Declarative style
class DeclarativeModel(Base):
    __tablename__ = 'test_model'

    id = Column(INTEGER, primary_key=True)
    field = Column(String)
    datetime = Column(DateTime, default=datetime.datetime.utcnow)
    floatfield = Column(Float)
    bigintfield = Column(BigInteger)


# Classical style
class ClassicalModel(object):
    pass


mapper(ClassicalModel, cls_test)


Base.metadata.create_all(bind=engine)

t = DeclarativeModel()
t.id = 1
t.field = "test"
t.floatfield = 1.2345
t.bigintfield = 1234567890123456789
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


