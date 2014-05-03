
import unittest
from djangorest_alchemy.managers import AlchemyModelManager

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


class SessionMixin(object):
    def __init__(self, *args, **kwargs):
        self.session = Session()

        # This super is necessary
        # because in case of multiple inheritance
        # this calls the next __init__ in the MRO
        super(SessionMixin, self).__init__(*args, **kwargs)


class ModelManager(SessionMixin, AlchemyModelManager):
    model_class = TestModel


class TestAlchemyModelManager(unittest.TestCase):

    def test_init(self):
        mgr = ModelManager()
        self.assertIsNotNone(mgr)

    def test_list(self):
        mgr = ModelManager()
        self.assertTrue(type(mgr.list()) is list,
                        "Should return list of models")
