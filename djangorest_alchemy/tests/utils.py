'''
Model and manager test dummies
'''

import datetime

from sqlalchemy import Column, ForeignKey, MetaData, Table, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, relationship, sessionmaker
from sqlalchemy.types import INTEGER, BigInteger, DateTime, Float, String


engine = create_engine('sqlite://', echo=False)

Base = declarative_base()

Session = sessionmaker(bind=engine)
Session.configure(bind=engine)

metadata = MetaData()

cls_test = Table('classical_test', metadata,
                 Column(u'classicalmodel_id', INTEGER(), primary_key=True),
                 Column(u'field', String)
                 )


class ChildModel(Base):
    __tablename__ = 'child_model'

    childmodel_id = Column(INTEGER, primary_key=True)
    parent_id = Column(INTEGER,
                       ForeignKey("test_model.declarativemodel_id"),
                       primary_key=True,)


# Declarative style
class DeclarativeModel(Base):
    __tablename__ = 'test_model'

    declarativemodel_id = Column(INTEGER, primary_key=True)
    field = Column(String)
    datetime = Column(DateTime, default=datetime.datetime.utcnow)
    floatfield = Column(Float)
    bigintfield = Column(BigInteger)
    child_model = relationship(ChildModel, uselist=False,
                               primaryjoin=(declarativemodel_id == ChildModel.parent_id))  # noqa


# Multiple primary keys
class CompositeKeysModel(Base):
    __tablename__ = 'composite_model'

    # This order of PK definition is important
    pk1 = Column(String, primary_key=True)
    pk2 = Column(String, primary_key=True)
    compositekeysmodel_id = Column(INTEGER, primary_key=True)
    field = Column(String)


# Classical style
class ClassicalModel(object):
    pass


mapper(ClassicalModel, cls_test)


Base.metadata.create_all(bind=engine)
metadata.create_all(bind=engine)

t = DeclarativeModel()
t.declarativemodel_id = 1
t.field = "test"
t.floatfield = 1.2345
t.bigintfield = 1234567890123456789

t.child_model = ChildModel()
t.child_model.childmodel_id = 2
t.child_model.parent_id = 1

session = Session()
session.add(t)
session.commit()

c = CompositeKeysModel()
c.compositekeysmodel_id = 1
c.pk1 = 'ABCD'
c.pk2 = 'WXYZ'
session.add(c)
session.commit()

cl = ClassicalModel()
cl.classicalmodel_id = 1
cl.field = 'test'
session.add(cl)
session.commit()


class SessionMixin(object):
    def __init__(self, *args, **kwargs):
        self.session = Session()

        # This super is necessary
        # because in case of multiple inheritance
        # this calls the next __init__ in the MRO
        super(SessionMixin, self).__init__(*args, **kwargs)
