
import unittest
from djangorest_alchemy.managers import AlchemyModelManager
from utils import SessionMixin, TestModel


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
