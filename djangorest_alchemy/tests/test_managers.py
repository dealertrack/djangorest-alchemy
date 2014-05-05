
'''
Unit test cases for AlchemyModelManager
'''
import unittest
from djangorest_alchemy.managers import AlchemyModelManager
from utils import SessionMixin, DeclarativeModel


class ModelManager(SessionMixin, AlchemyModelManager):
    model_class = DeclarativeModel


class TestAlchemyModelManager(unittest.TestCase):

    def test_init(self):
        mgr = ModelManager()
        self.assertIsNotNone(mgr)

    def test_list(self):
        mgr = ModelManager()
        self.assertTrue(type(mgr.list()) is list,
                        "Should return list of models")
