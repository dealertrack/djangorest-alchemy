'''
Model and manager test dummies
'''

from sqlalchemy import create_engine
from sqlalchemy import *
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import mapper
from sqlalchemy.orm import relationship
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


class ChildModel(Base):
    __tablename__ = 'child_model'

    child_model_id = Column(INTEGER, primary_key=True)
    parent_id = Column(INTEGER,
                       ForeignKey("test_model.id"),
                       primary_key=True,)


# Declarative style
class DeclarativeModel(Base):
    __tablename__ = 'test_model'

    # described the fields to be used as navigational
    # for serialization/deserialization purposes
    navigational_fields = ['child_model']

    id = Column(INTEGER, primary_key=True)
    field = Column(String)
    datetime = Column(DateTime, default=datetime.datetime.utcnow)
    floatfield = Column(Float)
    bigintfield = Column(BigInteger)
    child_model = relationship(ChildModel, uselist=False, primaryjoin=
                              (id == ChildModel.parent_id))


#Multiple primary keys
class CompositeKeysModel(Base):
    __tablename__ = 'composite_model'

    id = Column(INTEGER, primary_key=True)
    pk1 = Column(String, primary_key=True)
    pk2 = Column(String, primary_key=True)
    field = Column(String)


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

t.child_model = ChildModel()
t.child_model.child_model_id = 2
t.child_model.parent_id = 1

session = Session()
session.add(t)
session.commit()

c = CompositeKeysModel()
c.id = 1
c.pk1 = 'ABCD'
c.pk2 = 'WXYZ'
session.add(c)
session.commit()


class SessionMixin(object):
    def __init__(self, *args, **kwargs):
        self.session = Session()

        # This super is necessary
        # because in case of multiple inheritance
        # this calls the next __init__ in the MRO
        super(SessionMixin, self).__init__(*args, **kwargs)


